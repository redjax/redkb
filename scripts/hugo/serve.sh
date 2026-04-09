#!/usr/bin/env bash
set -euo pipefail

if ! command -v hugo &>/dev/null; then
  echo "[ERROR] hugo is not installed." >&2
  exit 1
fi

HUGO_BASEURL=${HUGO_BASEURL:-http://localhost:1313}
HUGO_HOST=${HUGO_HOST:-0.0.0.0}
HUGO_PORT=${HUGO_PORT:-1313}

## Build hugo server command
HUGO_CMD="hugo server"
HUGO_CMD="$HUGO_CMD --bind ${HUGO_HOST:-0.0.0.0}"
HUGO_CMD="$HUGO_CMD --port ${HUGO_PORT:-1313}"
HUGO_CMD="$HUGO_CMD --baseURL ${HUGO_BASEURL:-http://localhost:1313}"
HUGO_CMD="$HUGO_CMD --appendPort=false"

## Add dev flags if --dev passed
if [[ "$1" == "--dev" ]]; then
    HUGO_CMD="$HUGO_CMD -D"

    ## Remove --dev from args
    shift
fi

## Pass any remaining args
HUGO_CMD="$HUGO_CMD $@"

echo "Starting Hugo server: $HUGO_CMD"
if ! eval $HUGO_CMD 2>&1; then
  echo "[ERROR] Failed to serve Hugo site." >&2
  exit 1
fi
