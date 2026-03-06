#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
STATE_DIR="$REPO_ROOT/state"
PID_FILE="$STATE_DIR/git_autosync.pid"
OUT_LOG="$STATE_DIR/git_autosync.out.log"
SESSION_NAME="whoop_git_autosync"

mkdir -p "$STATE_DIR"

list_sessions() {
  screen -ls 2>/dev/null || true
}

if list_sessions | grep -E -q "[0-9]+[.]${SESSION_NAME}[[:space:]]"; then
  echo "autosync already running session=${SESSION_NAME}"
  exit 0
fi

screen -dmS "$SESSION_NAME" /bin/bash "$REPO_ROOT/ops/git_autosync_loop.sh"
screen_pid="$(list_sessions | awk '/[0-9]+[.]'"${SESSION_NAME}"'[[:space:]]/ {split($1, parts, "."); print parts[1]; exit}')"
echo "${screen_pid:-unknown}" > "$PID_FILE"
echo "autosync started session=${SESSION_NAME} pid=$(cat "$PID_FILE")"
