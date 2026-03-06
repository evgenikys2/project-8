#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

TARGET_BRANCH="${TARGET_BRANCH:-main}"
DRY_RUN="${DRY_RUN:-0}"

SYNC_PATHS=(
  "app"
  "ops"
  ".env.example"
  ".gitignore"
  "README.md"
  "requirements.txt"
)

log() {
  printf '%s %s\n' "[$(date '+%Y-%m-%d %H:%M:%S')]" "$*"
}

contains_stdin_pattern() {
  local pattern="$1"
  if command -v rg >/dev/null 2>&1; then
    rg -q -e "$pattern"
  else
    grep -E -q "$pattern"
  fi
}

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  log "skip: not a git repository"
  exit 0
fi

current_branch="$(git branch --show-current 2>/dev/null || true)"
if [[ "$current_branch" != "$TARGET_BRANCH" ]]; then
  log "skip: current branch '$current_branch' is not target '$TARGET_BRANCH'"
  exit 0
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  log "skip: remote origin is not configured"
  exit 0
fi

git add -- "${SYNC_PATHS[@]}"

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

commit_message="chore(sync): auto update $(date '+%Y-%m-%d %H:%M:%S %z')"

if [[ "$DRY_RUN" == "1" ]]; then
  log "dry-run: would commit and push"
  git diff --cached --name-status | sed -n '1,120p'
  git reset >/dev/null
  exit 0
fi

git commit -m "$commit_message" --no-verify
git push origin "$TARGET_BRANCH"

log "sync complete"
