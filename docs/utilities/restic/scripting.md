---
tags:
  - linux
  - windows
  - mac
  - utilities
  - backup
  - restic
---

# Scripts & Schedules

`restic` can be used as a CLI utility that you run manually when you want to create backups, but you can also script its usage, making it great for scheduled backups. The documentation in this section is not complete, but the Restic docs have [an entry for scripting `restic`](https://restic.readthedocs.io/en/latest/075_scripting.html) that is worth reading.

The documentation on this page assumes you are using [my Restic setup docs](setup.md). If not, you should be able to adapt the scripts for your own setup.

!!! WARNING

    This documentation is not complete. I am starting by providing example scripts, and will fill in details/write more generic scripts over time. This page is incomplete until this message is gone.

## Examples

### Generic backup script

If you did not [follow my Restic setup guide](setup.md), or you want to create a more 'self contained' script that does not rely on it, you can use something like the script below.

```shell title="restic_backup.sh" linenums="1"
#!/bin/bash

## Set default vars
SRC_DIR=""
RESTIC_REPO_FILE=""
RESTIC_PW_FILE=""
DRY_RUN=""

## Create array of exclude files to pass to restic
EXCLUDE_FILES=()
## Create array of exclude patternss to pass to restic
EXCLUDE_PATTERNS=()

## Define -h/--help function
function print_help() {
  cat <<EOF
Usage: $(basename "$0") [OPTIONS]

Restic backup script with support for multiple exclude files and patterns.

OPTIONS:
  -s, --backup-src DIR           Source directory to back up (required)
  -r, --repo-file PATH           Path to file with restic repository path (required)
  -p, --password-file PATH       Path to restic password file (required)
  --exclude-file PATH            Path to a file containing exclude patterns (can be used multiple times)
  --exclude-pattern PATTERN      Single exclude pattern (can be used multiple times)
  --dry-run                      Print the restic command that would be run, but do not execute
  -h, --help                     Display this help and exit

EXAMPLES:
  $(basename "$0") -s /home/username -r /etc/restic/repo -p /etc/restic/pw \
      --exclude-file ~/.restic/ignores/default --exclude-pattern "*.cache" --dry-run

NOTES:
  - You can specify --exclude-file and --exclude-pattern multiple times to pass multiple values.
  - Run with --dry-run to see command without running it.
EOF
}

## Parse CLI args
while [[ $# -gt 0 ]]; do
  case "$1" in
    -s|--backup-src)
      if [[ -z $2 ]]; then
        echo "[ERROR] --backup-src provided but no path given."

        print_help
        exit 1
      fi

      SRC_DIR="$2"
      shift 2
      ;;
    -r|--repo-file)
      if [[ -z $2 ]]; then
        echo "[ERROR] --repo-file provided but no path given."

        print_help
        exit 1
      fi

      RESTIC_REPO_FILE="$2"
      shift 2
      ;;
    -p|--password-file)
      if [[ -z $2 ]]; then
        echo "[ERROR] --password-file provided but no path given."

        print_help
        exit 1
      fi

      RESTIC_PW_FILE="$2"
      shift 2
      ;;
    --exclude-file)
      if [[ -n "$2" && "$2" != --* ]]; then
          EXCLUDE_FILES+=("$2")
          shift 2
      else
          echo "[ERROR] --exclude-file provided but no path given."

          print_help
          exit 1
      fi
      ;;
    --exclude-pattern)
      if [[ -n "$2" && "$2" != --* ]]; then
          EXCLUDE_PATTERNS+=("$2")
          shift 2
      else
          echo "[ERROR] --exclude-pattern provided but no path given."

          print_help
          exit 1
      fi
      ;;
    --dry-run)
      DRY_RUN="true"
      shift
      ;;
    -h|--help)
      print_help
      exit 0
      ;;
    *)
      echo "[ERROR] Unrecognized flag: $1"

      print_help
      exit 1
      ;;
  esac
done

## Export env vars for script
export RESTIC_REPOSITORY_FILE="$RESTIC_REPO_FILE"
export RESTIC_PASSWORD_FILE="$RESTIC_PW_FILE"

## Build command
cmd=(restic backup "$SRC_DIR")

## Append all exclude files
for excl_file in "${EXCLUDE_FILES[@]}"; do
  cmd+=(--exclude-file "$excl_file")
done

## Append all exclude patterns
for excl_pattern in "${EXCLUDE_PATTERNS[@]}"; do
  cmd+=(--exclude "$excl_pattern")
done

## Print or run command
if [[ -z "$DRY_RUN" ]] || [[ "$DRY_RUN" == "" ]]; then
  echo "Running restic cleanup command: $cmd"

  ## Run the command
  "$cmd[@]"

  if [[ $? -ne 0 ]]; then
    echo "[ERROR] Failed to run restic cleanup command."
    exit 1
  else
    echo "Restic cleanup performed successfully"
    exit 0
  fi
else
  echo "[DRY RUN] Would run restic cleanup command: $cmd[@]"
  exit 0
fi

```

### Backup Home
```shell title="backup_home_dir.sh" linenums="1"
#!/bin/bash

DOT_RESTIC="$HOME/.restic"
DOT_RESTICRC="$DOT_RESTIC/.resticrc"
RESTIC_IGNORES_DIR="$DOT_RESTIC/ignores"
RESTIC_PASSWORDS_DIR="$DOT_RESTIC/passwords"

if [[ ! -d "${DOT_RESTIC}" ]]; then
  echo "[ERROR] Could not find restic directory at '${DOT_RESTIC}'"
  exit 1
fi

if [[ ! -d "${RESTIC_IGNORES_DIR}" ]]; then
  echo "[ERROR] Could not find restic exclude files directory at path '${RESTIC_IGNORES_DIR}'"
  exit 1
fi

if [[ ! -d "${RESTIC_PASSWORDS_DIR}" ]]; then
  echo "[ERROR] Could not find restic password files directory at path '${RESTIC_PASSWORDS_DIR}'"
  exit 1
fi

## Source ~/.restic/.resticrc
if [[ ! -f "${DOT_RESTICRC}" ]]; then
  echo "[ERROR] Could not find ~/.restic/.resticrc"
  exit 1
fi
. "${DOT_RESTICRC}"

## Ensure ~/.restic/.resticrc values loaded correctly
if [[ -z "${RESTIC_REPOSITORY_FILE}" ]] || [[ "${RESTIC_REPOSITORY_FILE}" == "" ]]; then
  echo "[ERROR] RESTIC_REPOSITORY_FILE should not be empty. Ensure ~/.restic/.resticrc defines this variable"
  exit 1
fi

if [[ -z "${RESTIC_PASSWORD_FILE}" ]] || [[ "${RESTIC_PASSWORD_FILE}" == "" ]]; then
  echo "[ERROR] RESTIC_PASSWORD_FILE should not be empty. Ensure ~/.restic/.resticrc defines this variable"
  exit 1
fi

## Ensure restic files exist
if [[ ! -f "${RESTIC_REPOSITORY_FILE}" ]]; then
  echo "[ERROR] Could not find Restic repository file at path '$RESTIC_REPOSITORY_FILE'"
  exit 1
fi

if [[ ! -f "${RESTIC_PASSWORD_FILE}" ]]; then
  echo "[ERROR] Could not find Restic password file at path '$RESTIC_PASSWORD_FILE'"
  exit 1
fi

## Set default vars
DRY_RUN=""

## Parse script inputs
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN="true"
      shift 1
      ;;
    *)
      echo "[ERROR] Unknown argument: $1"
      shift 1
      ;;
  esac
done

## Build restic command
cmd="restic backup /home/username --exclude-file \"${RESTIC_IGNORES_DIR}/default\""

## Run or print command
if [[ -z "$DRY_RUN" ]] || [[ "$DRY_RUN" == "" ]]; then
  echo "Running restic backup command: $cmd"
  eval "${cmd}"

  if [[ $? -ne 0 ]]; then
    echo "[ERROR] Failed to create restic backup."
    exit 1
  else
    echo "Created restic snapshot of /home/jack"
    exit 0
  fi
else
  echo "[DRY RUN] Would run restic backup command: $cmd"
  exit 0
fi

```
