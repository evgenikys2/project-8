#!/usr/bin/env bash
set -euo pipefail

PLIST_NAME="com.project8.whoop_ai_assistant.autosync"
PLIST_PATH="${HOME}/Library/LaunchAgents/${PLIST_NAME}.plist"
RUNNER_PATH="${HOME}/.local/bin/whoop_ai_assistant_git_autosync.sh"

launchctl bootout "gui/$(id -u)" "$PLIST_PATH" >/dev/null 2>&1 || true
rm -f "$PLIST_PATH"
rm -f "$RUNNER_PATH"

echo "removed ${PLIST_PATH}"
