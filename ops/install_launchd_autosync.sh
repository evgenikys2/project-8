#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$REPO_ROOT/state"
PLIST_NAME="com.project8.whoop_ai_assistant.autosync"
PLIST_PATH="${HOME}/Library/LaunchAgents/${PLIST_NAME}.plist"
RUNNER_PATH="${HOME}/.local/bin/whoop_ai_assistant_git_autosync.sh"

mkdir -p "$STATE_DIR" "${HOME}/Library/LaunchAgents" "${HOME}/.local/bin"

cat > "$RUNNER_PATH" <<EOF
#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${REPO_ROOT}"
cd "\$REPO_ROOT"

TARGET_BRANCH="\${TARGET_BRANCH:-main}"
DRY_RUN="\${DRY_RUN:-0}"

SYNC_PATHS=(
  "app"
  "ops"
  ".env.example"
  ".gitignore"
  "README.md"
  "requirements.txt"
)

log() {
  printf '%s %s\n' "[\$(date '+%Y-%m-%d %H:%M:%S')]" "\$*" >> "${STATE_DIR}/git_autosync.launchd.log"
}

contains_stdin_pattern() {
  local pattern="\$1"
  if command -v rg >/dev/null 2>&1; then
    rg -q -e "\$pattern"
  else
    grep -E -q "\$pattern"
  fi
}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  log "skip: not a git repository"
  exit 0
fi

current_branch="\$(git branch --show-current 2>/dev/null || true)"
if [[ "\$current_branch" != "\$TARGET_BRANCH" ]]; then
  log "skip: current branch '\$current_branch' is not target '\$TARGET_BRANCH'"
  exit 0
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  log "skip: remote origin is not configured"
  exit 0
fi

git add -- "\${SYNC_PATHS[@]}"

if git diff --cached --quiet; then
  log "no changes to sync"
  exit 0
fi

if git diff --cached --name-only | contains_stdin_pattern '(^|/)\.env($|\.)|(^|/)data/whoop_tokens\.json$'; then
  log "blocked: staged sensitive env/token file detected; unstaging"
  git reset >/dev/null
  exit 1
fi

if git diff --cached | contains_stdin_pattern '(sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN (RSA|EC|OPENSSH|PRIVATE) KEY-----|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|refresh_token|access_token)'; then
  log "blocked: potential secret pattern detected; unstaging"
  git reset >/dev/null
  exit 1
fi

commit_message="chore(sync): auto update \$(date '+%Y-%m-%d %H:%M:%S %z')"

if [[ "\$DRY_RUN" == "1" ]]; then
  log "dry-run: would commit and push"
  git reset >/dev/null
  exit 0
fi

git commit -m "\$commit_message" --no-verify
git push origin "\$TARGET_BRANCH"
log "sync complete"
EOF

chmod +x "$RUNNER_PATH"

cat > "$PLIST_PATH" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>${PLIST_NAME}</string>
    <key>ProgramArguments</key>
    <array>
      <string>/bin/bash</string>
      <string>${RUNNER_PATH}</string>
    </array>
    <key>EnvironmentVariables</key>
    <dict>
      <key>TARGET_BRANCH</key>
      <string>main</string>
    </dict>
    <key>RunAtLoad</key>
    <true/>
    <key>StartInterval</key>
    <integer>300</integer>
    <key>StandardOutPath</key>
    <string>${STATE_DIR}/launchd.autosync.out.log</string>
    <key>StandardErrorPath</key>
    <string>${STATE_DIR}/launchd.autosync.err.log</string>
  </dict>
</plist>
EOF

launchctl bootout "gui/$(id -u)" "$PLIST_PATH" >/dev/null 2>&1 || true
launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH"
launchctl kickstart -k "gui/$(id -u)/${PLIST_NAME}"

echo "$PLIST_PATH"
