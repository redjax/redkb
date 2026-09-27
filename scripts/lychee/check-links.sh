#!/usr/bin/env bash
set -euo pipefail

shopt -s globstar nullglob

THIS_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_ROOT="$(realpath -m "${THIS_DIR}/../..")"

PUBLIC_DIR="${PROJECT_ROOT}/public"
BUILD_FIRST="false"
CHECK_MODE="offline"
SITE_HOST=""
GITHUB_TOKEN_VALUE="${GITHUB_TOKEN:-}"

CWD="$(pwd)"
TEMP_FILES=()

usage() {
  cat <<EOF
Usage:
  ${0##*/} [OPTIONS]

Build a Hugo site optionally, then check links in its rendered HTML.

Modes:
  --offline
      Validate local links, routes, assets, and fragments in generated HTML.
      This is the default.

  --online
      Validate external HTTP(S) URLs. Runs a general external scan and a
      separate GitHub-only scan.

Options:
  -b, --build                  Build the Hugo site before checking links
  -o, --output-dir DIRECTORY   Hugo output directory
      --offline                Check local site links only (default)
      --online                 Check external HTTP(S) links only
      --site-host HOST         First-party hostname to exclude in online mode
      --github-token TOKEN     GitHub API token for GitHub URL validation
  -h, --help                   Print this help menu

Environment:
  GITHUB_TOKEN                 Used when --github-token is not provided

Examples:
  ${0##*/} --build
  ${0##*/} --build --online --site-host example.com
  GITHUB_TOKEN="\$GITHUB_TOKEN" ${0##*/} --build --online --site-host example.com
EOF
}

error() {
  echo "[ERROR] $*" >&2
  exit 1
}

cleanup() {
  local file

  for file in "${TEMP_FILES[@]}"; do
    [[ -e "${file}" ]] && rm -f -- "${file}"
  done

  cd "${CWD}"
}

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

escape_ere() {
  sed 's/[][(){}.^$*+?|\\/]/\\&/g' <<<"$1"
}

collect_github_urls() {
  local html_file

  while IFS= read -r -d '' html_file; do
    grep -Eo 'https?://github\.com/[^"[:space:]<>]+' "${html_file}" || true
  done < <(find "${PUBLIC_DIR}" -type f -name '*.html' -print0) |
    sed \
      -e 's/&amp;/\&/g' \
      -e 's/[),.;:!?]*$//' |
    sort -u
}

write_github_url_file() {
  local url_file

  url_file="$(mktemp "${TMPDIR:-/tmp}/lychee-github-urls.XXXXXX.txt")"
  TEMP_FILES+=("${url_file}")

  printf '%s\n' "${GITHUB_URLS[@]}" >"${url_file}"

  printf '%s\n' "${url_file}"
}

trap cleanup EXIT

while [[ $# -gt 0 ]]; do
  case "$1" in
  -b | --build)
    BUILD_FIRST="true"
    shift
    ;;
  -o | --output-dir)
    [[ $# -ge 2 ]] || error "$1 requires a directory argument"
    [[ -n "$2" ]] || error "$1 requires a non-empty directory argument"

    PUBLIC_DIR="$(realpath -m "$2")"
    shift 2
    ;;
  --offline)
    CHECK_MODE="offline"
    shift
    ;;
  --online)
    CHECK_MODE="online"
    shift
    ;;
  --site-host)
    [[ $# -ge 2 ]] || error "$1 requires a hostname argument"
    [[ -n "$2" ]] || error "$1 requires a non-empty hostname argument"

    SITE_HOST="$2"
    shift 2
    ;;
  --github-token)
    [[ $# -ge 2 ]] || error "$1 requires a token argument"
    [[ -n "$2" ]] || error "$1 requires a non-empty token argument"

    GITHUB_TOKEN_VALUE="$2"
    shift 2
    ;;
  -h | --help)
    usage
    exit 0
    ;;
  *)
    error "Invalid option: $1"
    ;;
  esac
done

command_exists lychee || error "lychee is required but was not found in PATH"

cd "${PROJECT_ROOT}"

if [[ "${BUILD_FIRST}" == "true" ]]; then
  echo "Building site with Hugo before checking links"

  if ! "${PROJECT_ROOT}/scripts/hugo/build.sh" 2>&1; then
    error "Failed to build Hugo site"
  fi
fi

if [[ ! -d "${PUBLIC_DIR}" ]]; then
  error "Hugo output directory does not exist: ${PUBLIC_DIR}. Run with --build or specify --output-dir."
fi

HTML_FILES=("${PUBLIC_DIR}"/**/*.html)

if [[ "${#HTML_FILES[@]}" -eq 0 ]]; then
  error "No HTML files found under Hugo output directory: ${PUBLIC_DIR}"
fi

if [[ "${CHECK_MODE}" == "online" && -z "${SITE_HOST}" ]]; then
  error "--online requires --site-host HOST. Example: ${0##*/} --build --online --site-host example.com"
fi

case "${CHECK_MODE}" in
offline)
  echo
  echo "[ Running Lychee in offline mode against Hugo static files ]"
  echo

  if ! lychee \
    --offline \
    --root-dir "${PUBLIC_DIR}" \
    --index-files index.html \
    --fallback-extensions html \
    --include-fragments \
    "${HTML_FILES[@]}" \
    2>&1; then
    error "Lychee found broken local links"
  fi
  ;;

online)
  SITE_HOST_REGEX="$(escape_ere "${SITE_HOST}")"
  GENERAL_LINK_CHECK_EXIT_CODE=0
  GITHUB_LINK_CHECK_EXIT_CODE=0

  echo
  echo "[ Running Lychee against external HTTP(S) links ]"
  echo "Excluding first-party host: ${SITE_HOST}"

  echo
  echo "[+] Checking non-GitHub external links"

  lychee \
    --scheme http \
    --scheme https \
    --exclude-link-local \
    --root-dir "${PUBLIC_DIR}" \
    --index-files index.html \
    --fallback-extensions html \
    --exclude "^https?://([[:alnum:]-]+\\.)?${SITE_HOST_REGEX}(:[0-9]+)?(/|$)" \
    --exclude '^https?://github\.com/' \
    --exclude '^https?://localhost(:[0-9]+)?(/|$)' \
    --exclude '^https?://127\.0\.0\.1(:[0-9]+)?(/|$)' \
    --user-agent 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36' \
    --timeout 30 \
    --max-retries 1 \
    --max-concurrency 4 \
    --max-redirects 10 \
    --accept '200..=299,301,302,303,307,308,403,429' \
    --cache \
    --max-cache-age 7d \
    "${HTML_FILES[@]}" \
    2>&1 || GENERAL_LINK_CHECK_EXIT_CODE=$?

  echo
  echo "[+] Collecting GitHub URLs from generated HTML"
  echo

  GITHUB_URLS=()

  while IFS= read -r url; do
    [[ -n "${url}" ]] && GITHUB_URLS+=("${url}")
  done < <(collect_github_urls)

  if [[ "${#GITHUB_URLS[@]}" -eq 0 ]]; then
    echo "No GitHub URLs found"
  else
    GITHUB_URL_FILE="$(write_github_url_file)"

    echo "[+] Checking ${#GITHUB_URLS[@]} GitHub URL(s) serially"

    if [[ -n "${GITHUB_TOKEN_VALUE}" ]]; then
      echo "Passing GitHub token to Lychee for github.com link checks"

      lychee \
        --github-token "${GITHUB_TOKEN_VALUE}" \
        --scheme http \
        --scheme https \
        --timeout 30 \
        --max-retries 0 \
        --max-concurrency 1 \
        --max-redirects 10 \
        --accept '200..=299,429' \
        --cache \
        --max-cache-age 30d \
        "${GITHUB_URL_FILE}" \
        2>&1 || GITHUB_LINK_CHECK_EXIT_CODE=$?
    else
      echo "[WARN] No GitHub token provided; checking GitHub links without authentication" >&2

      lychee \
        --scheme http \
        --scheme https \
        --timeout 30 \
        --max-retries 0 \
        --max-concurrency 1 \
        --max-redirects 10 \
        --accept '200..=299,429' \
        --cache \
        --max-cache-age 30d \
        "${GITHUB_URL_FILE}" \
        2>&1 || GITHUB_LINK_CHECK_EXIT_CODE=$?
    fi
  fi

  if [[ "${GENERAL_LINK_CHECK_EXIT_CODE}" -ne 0 ]]; then
    echo "[ERROR] Lychee found broken non-GitHub external links" >&2
  fi

  if [[ "${GITHUB_LINK_CHECK_EXIT_CODE}" -ne 0 ]]; then
    echo "[ERROR] Lychee found broken GitHub links" >&2
  fi

  if [[ "${GENERAL_LINK_CHECK_EXIT_CODE}" -ne 0 || "${GITHUB_LINK_CHECK_EXIT_CODE}" -ne 0 ]]; then
    exit 1
  fi
  ;;

*)
  error "Unsupported check mode: ${CHECK_MODE}"
  ;;
esac
