#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv &>/dev/null; then
  echo "[ERROR] uv is not installed" >&2
  exit 1
fi

THIS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT=$(realpath -m "${THIS_DIR}/..")
REQUIREMENTS_DIR="${REPO_ROOT}/requirements"
PROD_REQUIREMENTS="${REQUIREMENTS_DIR}/requirements.txt"
DEV_REQUIREMENTS="${REQUIREMENTS_DIR}/requirements.dev.txt"

echo "Exporting production requirements to $PROD_REQUIREMENTS"
if ! uv pip compile pyproject.toml -o ${PROD_REQUIREMENTS}; then
  echo "[ERROR] Failed compiling pyproject dependencies into ${PROD_REQUIREMENTS}" >&2
fi

echo "Exporting dev requirements to $DEV_REQUIREMENTS"
if ! uv pip compile pyproject.toml --group dev -o ${DEV_REQUIREMENTS}; then
  echo "[ERROR] Failed compiling pyproject dev dependencies to ${DEV_REQUIREMENTS}" >&2
fi
