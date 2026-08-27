#!/usr/bin/env bash
set -euo pipefail

function usage() {
  cat <<EOF
Description:
  Create a new page in the content/ directory. Provide 1 input, the path to the new page
  relative to the root of content/.

  For example, to start a new page in content/docs/bash/new_page.md, you would run:
    ${0} docs/bash/new_page.md.

Usage:
  $0 path/to/page.md

Options:
  -h, --help    Show this help message and exit

Examples:
  $0 docs/windows/wsl/example.md
  $0 docs/devops/example.md
  $0 docs/devops/github/example.md
  $0 snippets/bash/example.md

EOF
}

## Handle options
case "${1:-}" in
-h | --help)
  usage
  exit 0
  ;;
esac

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

if ! command -v hugo >/dev/null 2>&1; then
  echo "[ERROR] hugo is not installed."
  exit 1
fi

## Determine archetype from file path
function get_kind() {
  case "$1" in
  docs/unifi/*)
    echo "unifi"
    ;;
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

page="$1"
kind="$(get_kind "$page")"

echo "Using archetype: $kind"

if hugo new --kind "$kind" "$page"; then
  echo "Created new page: $page"
else
  echo "[ERROR] Failed creating page: $page" >&2
  exit 1
fi
