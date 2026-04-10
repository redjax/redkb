#!/usr/bin/env bash
set -uo pipefail

if ! command -v hugo &>/dev/null; then
  echo "[ERROR] hugo is not installed." >&2
  exit 1
fi

HUGO_BASEURL=${HUGO_BASEURL:-http://localhost:1313}
HUGO_HOST=${HUGO_HOST:-0.0.0.0}
HUGO_PORT=${HUGO_PORT:-1313}
SERVE_DRAFTS=${HUGO_SERVE_DRAFTS:-false}

function usage() {
  echo ""
  echo "Usage: ${0} [OPTIONS]"
  echo ""
  echo "Options:"
  echo "  -h, --help      Show this help menu"
  echo "  -H, --host      (default: 0.0.0.0) Host interface to serve Hugo on"
  echo "  -p, --port      (default: 1313) Port to serve Hugo on"
  echo "  -b, --base-url  (default: http://localhost:1313) Hugo site URL"
  echo "  --append-port   (default: false) Append port in URL/links"
  echo "  -d, --drafts    Serve draft files"
  echo ""
}

while [[ $# -gt 0 ]]; do
  case $1 in
    -H|--host)
      HUGO_HOST="${2}"
      shift 2
      ;;
    -p|--port)
      HUGO_PORT="${2}"
      shift 2
      ;;
    -b|--base-url)
      HUGO_BASEURL="${2}"
      shift 2
      ;;
    -d|--drafts)
      SERVE_DRAFTS=true
      shift
      ;;
    -h|--help)
      usage
      exit 1
      ;;
    *)
      echo "[ERROR] Invalid arg: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "${HUGO_BASEURL}" ]]; then
  echo "[ERROR] Missing value for Hugo base URL" >&2
  usage
  exit 1  
fi

if [[ -z "${HUGO_HOST}" ]]; then
  echo "[ERROR] Missing value for Hugo host address" >&2
  usage
  exit 1
fi

if [[ -z "${HUGO_PORT}" ]]; then
  echo "[ERROR] Missing value for Hugo port" >&2
  usage
  exit 1
fi

## Build hugo server command
HUGO_CMD="hugo server"
HUGO_CMD="$HUGO_CMD --bind ${HUGO_HOST:-0.0.0.0}"
HUGO_CMD="$HUGO_CMD --port ${HUGO_PORT:-1313}"
HUGO_CMD="$HUGO_CMD --baseURL ${HUGO_BASEURL:-http://localhost:1313}"
HUGO_CMD="$HUGO_CMD --appendPort=false"

if [[ "${SERVE_DRAFTS}" == "true" ]]; then
    HUGO_CMD="$HUGO_CMD -D"

    ## Remove --dev from args
    shift
fi

## Pass any remaining args
HUGO_CMD="$HUGO_CMD $@"

echo "Starting Hugo server: ${HUGO_CMD[*]}"
if ! eval $HUGO_CMD 2>&1; then
  echo "[ERROR] Failed to serve Hugo site." >&2
  exit 1
fi
