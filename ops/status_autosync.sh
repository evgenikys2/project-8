#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PID_FILE="$REPO_ROOT/state/git_autosync.pid"
SESSION_NAME="whoop_git_autosync"

list_sessions() {
  screen -ls 2>/dev/null || true
}

if list_sessions | grep -E -q "[0-9]+[.]${SESSION_NAME}[[:space:]]"; then
  if [[ -f "$PID_FILE" ]]; then
    echo "running session=${SESSION_NAME} pid=$(cat "$PID_FILE")"
  else
    echo "running session=${SESSION_NAME}"
  fi
else
  echo "stopped"
fi
