#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$REPO_ROOT/state/git_autosync.pid"
SESSION_NAME="whoop_git_autosync"

list_sessions() {
  screen -ls 2>/dev/null || true
}

while read -r screen_id; do
  [[ -n "$screen_id" ]] || continue
  screen -S "$screen_id" -X quit || true
done < <(list_sessions | awk '/[0-9]+[.]'"${SESSION_NAME}"'[[:space:]]/ {print $1}')

rm -f "$PID_FILE"
echo "autosync stopped"
