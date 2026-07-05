#!/usr/bin/env bash
set -euo pipefail

if ! command -v hugo >/dev/null 2>&1; then
  echo "[ERROR] hugo is not installed."
  exit 1
fi

function usage() {
  cat <<EOF

Usage: $0 path/to/page.md

Examples:
  $0 docs/windows/wsl/example.md
  $0 docs/devops/example.md
  $0 docs/devops/github/example.md
  $0 snippets/bash/example.md

EOF
}

## Determine archetype from file path
function get_kind() {
  case "$1" in
  docs/devops/github/*)
    echo "github"
    ;;
  docs/devops/*)
    echo "devops"
    ;;
  docs/*)
    echo "docs"
    ;;
  snippets/*)
    echo "snippets"
    ;;
  *)
    echo "default"
    ;;
  esac
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

page="$1"
kind="$(get_kind "$page")"

echo "Using archetype: $kind"

if hugo new --kind "$kind" "$page"; then
  echo "Created new page: $page"
else
  echo "[ERROR] Failed creating page: $page" >&2
  exit 1
fi
