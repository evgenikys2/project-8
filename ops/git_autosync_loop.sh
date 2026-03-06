#!/usr/bin/env bash
set -euo pipefail

INTERVAL_SEC="${INTERVAL_SEC:-300}"
RUNNER="${RUNNER:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/git_autosync.sh}"
LOG_FILE="${LOG_FILE:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/state/git_autosync.loop.log}"

mkdir -p "$(dirname "$LOG_FILE")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] autosync loop started interval=${INTERVAL_SEC}s runner=${RUNNER}" >> "$LOG_FILE"

while true; do
  /bin/bash "$RUNNER" >> "$LOG_FILE" 2>&1 || true
  sleep "$INTERVAL_SEC"
done
