#!/usr/bin/env bash
set -euo pipefail

if ! command -v uv &>/dev/null; then
  echo "[ERROR] uv is not installed." 2>&1
  exit 1
fi

echo "Upgrading uv lockfile"
if ! uv lock --upgrade 2>&1; then
  echo "[ERROR] Failed updating lockfile" 2>&1
  exit 1
fi

echo "Synching packages"
if ! uv sync --all-groups &>/dev/null; then
  echo "[ERROR] Failed running uv sync" 2>&1
  exit 1
fi

echo "Finished upgrading packages"
