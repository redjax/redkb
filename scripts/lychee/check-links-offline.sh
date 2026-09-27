#!/usr/bin/env bash
set -euo pipefail

THIS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT=$(realpath -m "${THIS_DIR}/../..")
PUBLIC_DIR="${PROJECT_ROOT}/public"
BUILD_FIRST="false"
CWD=$(pwd)
trap 'cd "${CWD}"' EXIT

usage() {
  cat <<EOF
Usage:
  ${0##*/} [OPTIONS]

Options:
  -h, --help    Print this help menu
EOF
}

while [[ $# -gt 0 ]]; do
  case $1 in
  -b | --build)
    BUILD_FIRST="true"
    shift
    ;;
  -o | --output-dir)
    PUBLIC_DIR="$2"
    shift 2
    ;;
  -h | --help)
    usage
    exit 0
    ;;
  *)
    echo "[ERROR] Invalid option: $1" >&2
    usage
    exit 1
    ;;
  esac
done

cd "${PROJECT_ROOT}"

if [[ "${BUILD_FIRST}" == "true" ]]; then
  echo "Building site with Hugo before checking links"

  if ! "${PROJECT_ROOT}/scripts/hugo/build.sh" 2>&1; then
    echo "[ERROR] Failed to build Hugo site" >&2
    exit 1
  fi

fi

echo
echo "Running Lychee in offline mode against Hugo static files"

if ! lychee \
  --offline \
  --root-dir "${PUBLIC_DIR}" \
  --index-files index.html \
  --fallback-extensions html 'public/**/*.html' \
  --include-fragments \
  "${PUBLIC_DIR}/**/*.html" \
  2>&1; then
  echo "[ERROR] Lychee encountered failures while running" >&2
  exit 1
fi
