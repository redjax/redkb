#!/usr/bin/env bash
set -euo pipefail

if ! command -v hugo &>/dev/null; then
  echo "[ERROR] hugo is not installed." >&2
  exit 1
fi

THIS_DIR="$(dirname "$0")"
REPO_ROOT=$(realpath -m "${THIS_DIR}/../..")
ORIGINAL_PATH=$(pwd)

function cleanup() {
  cd "$ORIGINAL_PATH"
}
trap cleanup EXIT

HUGO_BASEURL=${HUGO_BASEURL:-http://localhost:1313}

cd "${REPO_ROOT}"

echo "Building Hugo site using base URL: ${HUGO_BASEURL}"
if ! hugo --minify --gc --baseURL "$HUGO_BASEURL" 2>&1; then
  echo "[ERROR] Failed building Hugo site." >&2
  exit 1
fi
