#!/usr/bin/env bash
set -euo pipefail

if ! command -v hugo &> /dev/null; then
  echo "[ERROR] hugo is not installed."
  exit 1
fi

function usage() {
  echo ""
  echo "Usage: $0 path/to/page-name.md"
  echo ""
  echo "Examples:"
  echo "  $0 posts/example.md"
  echo "  $0 posts/2026/post-name/index.md"
  echo ""
}

if [[ $# -eq 0 ]]; then
  usage
  exit 1
fi

if ! hugo new "$@" 2>&1; then
  echo "[ERROR] Failed creating page: $@" >&2
  exit 1
else
  echo "Created new page: $@"
fi
