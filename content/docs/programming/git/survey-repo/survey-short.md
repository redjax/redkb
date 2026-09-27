---
title: "Survey Short"
date: 2026-09-27T13:29:46-04:00
draft: true
weight: 10
toc: true
keywords: []
tags:
  - programming
  - software-development
  - coding
  - git
  - version-control
---

A quick, language-agnostic first pass over an unfamiliar Git repository. This guide inventories the current checkout, Git history, contributors, and repository size. It does not scan for secrets or vulnerabilities, build the application, or change Git history.

## Requirements

- Bash
- Git
- Standard GNU command-line utilities: `find`, `sort`, `uniq`, `awk`, `sed`, `head`, `wc`, and `du`.
- Code counter: [`tokei`](https://github.com/XAMPPRocky/tokei) or [`scc`](https://github.com/boyter/scc).
- Optional history tools
  - [`git-fame`](https://pypi.org/project/git-fame/)
  - [`git-sizer`](https://github.com/github/git-sizer)
  - [`git-filter-repo`](https://github.com/newren/git-filter-repo)

> [!NOTE]
> These commands assume a Linux/GNU shell. Run them from the repository root. History results are incomplete in a shallow clone or a clone missing relevant branches or tags.

## Survey Guide

The commands in the following sections can help you get a better understanding of what's in the repository you're surveying.

### Checkout Context

Confirm where you are and what you are surveying:

```shell
git rev-parse --show-toplevel
git rev-parse HEAD
git status --short --branch
git remote -v
git rev-parse --is-shallow-repository
```

### Repository Makeup

Show the top of the directory tree:

```shell
find . -maxdepth 2 \
  -path './.git' -prune -o \
  -path './node_modules' -prune -o \
  -path './.venv' -prune -o \
  -print |
  sort
```

List tracked files and count them:

```shell
git ls-files
git ls-files | wc -l
```

Find common project, dependency, CI, deployment, and policy files:

```shell
git ls-files \
  'README*' '**/README*' \
  'CONTRIBUTING*' '**/CONTRIBUTING*' \
  'CODEOWNERS' '**/CODEOWNERS' \
  'LICENSE*' '**/LICENSE*' \
  'Makefile' '**/Makefile' \
  'Dockerfile*' '**/Dockerfile*' \
  '*compose*.yml' '**/*compose*.yml' \
  '*compose*.yaml' '**/*compose*.yaml' \
  '*.tf' '**/*.tf' \
  'azure-pipelines*.yml' '**/azure-pipelines*.yml' \
  '.github/workflows/*' \
  '.gitlab-ci.yml' \
  'package.json' '**/package.json' \
  'pnpm-lock.yaml' '**/pnpm-lock.yaml' \
  'package-lock.json' '**/package-lock.json' \
  'pyproject.toml' '**/pyproject.toml' \
  'requirements*.txt' '**/requirements*.txt' \
  'go.mod' '**/go.mod' \
  'pom.xml' '**/pom.xml' \
  'build.gradle*' '**/build.gradle*'
```

Count tracked files by extension:

```shell
git ls-files |
  awk -F/ '
    {
      name = $NF
      if (name !~ /\./ || name ~ /^\.[^.]+$/) next
      sub(/^.*\./, "", name)
      print tolower(name)
    }
  ' |
  sort |
  uniq -c |
  sort -nr
```

Count lines with `scc .` or `tokei .`. These tools analyze the checkout, so their counts can differ from the tracked-file inventory. Tokei reports counts grouped by language; scc also includes a rough complexity figure.

### Current Size and Artifacts

Compare total checkout size with the Git directory:

```shell
du -sh .
du -sh "$(git rev-parse --absolute-git-dir)"
du -h --max-depth=2 . 2>/dev/null | sort -h
```

Find the largest current files, excluding `.git`:

```shell
find . \
  -path './.git' -prune -o \
  -type f -printf '%s\t%p\n' |
  sort -nr |
  head -100
```

Identify tracked files that might be generated output, dependencies, databases, or large assets:

```shell
git ls-files \
  'node_modules/**' '**/node_modules/**' \
  '.venv/**' '**/.venv/**' \
  'dist/**' '**/dist/**' \
  'build/**' '**/build/**' \
  '*.zip' '*.tar.gz' '*.db' '*.sqlite' \
  '*.mp4' '*.mov' '*.onnx' '*.pt'
```

> [!NOTE]
> Some repositories track data or binary assets intentionally. Do not assume that just because you found an archive, binary, or modules path that you should delete it from history.

### Contributores and Activity

Show contributors by commit count:

```shell
git shortlog -sne --all
```

Inspect recent commits:

```shell
git log -50 \
  --date=short \
  --format='%h %ad %an %s'
```

See activity by month:

```shell
git log --all --format='%ad' --date=format:'%Y-%m' |
  sort |
  uniq -c
```

Find paths that appear most often in commit changes:

```shell
git log --all --format= --name-only |
  sed '/^$/d' |
  sort |
  uniq -c |
  sort -nr |
  head -100
```

> [!NOTE]
> Commit counts do not establish ownership. Contributors may have used multiple names or email addresses, and the last person to change a file may not be its maintainer.

### Git History and Storage

Inspect Git's object database:

```shell
git count-objects -vH
```

Find the largest blobs reachable from locally available history, including files no longer present in the current checkout:

```shell
git rev-list --objects --all |
  git cat-file \
    --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' |
  awk '$1 == "blob" { print $3 "\t" $2 "\t" $4 }' |
  sort -nr |
  head -100
```

> [!NOTE]
> The output shows blob size in bytes, object ID, and an associated path. A blob may have had other paths in history; treat this as a starting point for investigation, not a definitive path history. Git’s rev-list --objects and cat-file --batch-check expose reachable objects and their sizes.

If installed, run git-sizer for broader Git structure and size metrics:

```shell
git sizer --verbose
```

Optional: Deeper history analysis with `git-filter-repo`:

```shell
REPORT_DIR="$(mktemp -d "${TMPDIR:-/tmp}/git-filter-repo-analysis.XXXXXX")"

git filter-repo \
  --analyze \
  --report-dir "$REPORT_DIR"

printf 'Analysis reports: %s\n' "$REPORT_DIR"
```

## Scripted Survey

This script chains the commands in the sections above into a single Bash script you can execute against a target repository:

```shell
#!/usr/bin/env bash
set -uo pipefail

###########################################################################
# Survey a Git repository to understand what's contained within.          #
#                                                                         #
# Usage:                                                                  #
#   repo-survey-short.sh --repo /path/to/repository                       #
#                                                                         #
#   repo-survey-short.sh --repo /path/to/repository \                     #
#     --output-path /path/to/surveys                                      #
#                                                                         #
# The script can be launched from any directory. It does not build, test, #
# install project dependencies, or rewrite Git history.                   #
###########################################################################

usage() {
  cat <<EOF
Usage:
  ${0##*/} --repo PATH [--output-path PATH]

Options:
  --repo             <PATH>  Git repository to survey. Required.
  -o, --output-path  <PATH>  Parent directory for reports. Default: a unique directory under /tmp/
  -h, --help                 Show this help.

Examples:
  ${0##*/} --repo "$HOME/git/example-app"
  ${0##*/} --repo ../example-app --output-path "$HOME/git-surveys"
EOF
}

error() {
  printf '[ERROR] %s\n' "$*" >&2
}

info() {
  printf '[INFO] %s\n' "$*"
}

REPO_INPUT=""
OUTPUT_PARENT_INPUT=""

while (($#)); do
  case "$1" in
    --repo)
      (($# >= 2)) || {
        error "--repo requires a path."
        exit 2
      }
      REPO_INPUT="$2"
      shift 2
      ;;
    -o|--output-path)
      (($# >= 2)) || {
        error "--output-path requires a path."
        exit 2
      }
      OUTPUT_PARENT_INPUT="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      error "Unknown argument: $1"
      usage >&2

      exit 2
      ;;
  esac
done

[[ -n "$REPO_INPUT" ]] || {
  error "--repo is required."
  usage >&2
  exit 2
}

command -v git >/dev/null 2>&1 || {
  error "Git is required."
  exit 1
}

[[ -d "$REPO_INPUT" ]] || {
  error "Repository path does not exist: $REPO_INPUT"
  exit 1
}

REPO="$(cd -- "$REPO_INPUT" && pwd -P)" || exit 1

GIT_ROOT="$(git -C "$REPO" rev-parse --show-toplevel 2>/dev/null)" || {
  error "Not a Git working tree: $REPO"
  exit 1
}

GIT_ROOT="$(cd -- "$GIT_ROOT" && pwd -P)" || exit 1

if [[ "$REPO" != "$GIT_ROOT" ]]; then
  error "--repo must point to the repository root."
  error "Repository root: $GIT_ROOT"
  exit 1
fi

REPO_NAME="$(basename "$REPO")"
STAMP="$(date +%y%m%d%H%M%S)"

if [[ -n "$OUTPUT_PARENT_INPUT" ]]; then
  mkdir -p -- "$OUTPUT_PARENT_INPUT" || {
    error "Cannot create output parent: $OUTPUT_PARENT_INPUT"
    exit 1
  }

  OUTPUT_PARENT="$(cd -- "$OUTPUT_PARENT_INPUT" && pwd -P)" || exit 1

  ## Check the parent before creating any survey output under it.
  case "$OUTPUT_PARENT/" in
    "$REPO/"*)
      error "Output parent must be outside the target repository: $OUTPUT_PARENT"
      exit 1
      ;;
  esac

  OUT="$OUTPUT_PARENT/${REPO_NAME}--survey-${STAMP}"

  mkdir -- "$OUT" || {
    error "Cannot create report directory: $OUT"
    exit 1
  }
else
  OUTPUT_PARENT="/tmp"

  ## Check the parent before creating any survey output under it.
  case "$OUTPUT_PARENT/" in
    "$REPO/"*)
      error "Output parent must be outside the target repository: $OUTPUT_PARENT"
      exit 1
      ;;
  esac

  OUT="$(mktemp -d "/tmp/${REPO_NAME}-survey-${STAMP}-XXXXXX")" || {
    error "Cannot create temporary report directory under /tmp."
    exit 1
  }
fi

mkdir -p "$OUT"/{inventory,history} || exit 1

declare -a FAILED_CHECKS=()
declare -a SKIPPED_CHECKS=()

run_report() {
  local name="$1"
  local path="$2"
  shift 2

  info "Running: $name"

  if "$@" >"$path" 2>&1; then
    return 0
  fi

  local result=$?
  FAILED_CHECKS+=("$name (exit $result)")
  return 0
}

has_git_extension() {
  local name="$1"

  if command -v "git-${name}" >/dev/null 2>&1; then
    return 0
  fi

  [[ -x "$(git --exec-path)/git-${name}" ]]
}

####################
# Checkout context #
####################

echo "[ Surveying Git Repository: ${REPO} ]"
echo

{
  printf 'Repository: %s\n' "$REPO"
  printf 'Surveyed: %s\n' "$(date -Is)"

  printf 'HEAD: '
  git -C "$REPO" rev-parse HEAD

  printf 'Branch: '
  git -C "$REPO" branch --show-current

  printf 'Shallow clone: '
  git -C "$REPO" rev-parse --is-shallow-repository

  printf '\nStatus:\n'
  git -C "$REPO" status --short --branch

  printf '\nRemotes:\n'
  git -C "$REPO" remote -v
} >"$OUT/inventory/context.txt" 2>&1

#############################
# Current repository makeup #
#############################

info "Running: Directory structure"

find "$REPO" -maxdepth 2 \
  -path "$REPO/.git" -prune -o \
  -path "$REPO/node_modules" -prune -o \
  -path "$REPO/.venv" -prune -o \
  -print |
  sort \
  >"$OUT/inventory/structure.txt"

result=$?
if ((result != 0)); then
  FAILED_CHECKS+=("Directory structure (exit $result)")
fi

run_report \
  "Tracked files" \
  "$OUT/inventory/tracked-files.txt" \
  git -C "$REPO" ls-files

wc -l <"$OUT/inventory/tracked-files.txt" \
  >"$OUT/inventory/tracked-file-count.txt"

run_report \
  "Project and operational files" \
  "$OUT/inventory/project-files.txt" \
  git -C "$REPO" ls-files \
    'README*' '**/README*' \
    'CONTRIBUTING*' '**/CONTRIBUTING*' \
    'CODEOWNERS' '**/CODEOWNERS' \
    'LICENSE*' '**/LICENSE*' \
    'Makefile' '**/Makefile' \
    'Dockerfile*' '**/Dockerfile*' \
    '*compose*.yml' '**/*compose*.yml' \
    '*compose*.yaml' '**/*compose*.yaml' \
    '*.tf' '**/*.tf' \
    'azure-pipelines*.yml' '**/azure-pipelines*.yml' \
    '.github/workflows/*' \
    '.gitlab-ci.yml' \
    'package.json' '**/package.json' \
    'pnpm-lock.yaml' '**/pnpm-lock.yaml' \
    'package-lock.json' '**/package-lock.json' \
    'pyproject.toml' '**/pyproject.toml' \
    'requirements*.txt' '**/requirements*.txt' \
    'go.mod' '**/go.mod' \
    'pom.xml' '**/pom.xml' \
    'build.gradle*' '**/build.gradle*'

info "Running: Tracked file extensions"

awk -F/ '
  {
    name = $NF
    if (name !~ /\./ || name ~ /^\.[^.]+$/) next
    sub(/^.*\./, "", name)
    print tolower(name)
  }
' "$OUT/inventory/tracked-files.txt" |
  sort |
  uniq -c |
  sort -nr \
  >"$OUT/inventory/file-extensions.txt"

result=$?
if ((result != 0)); then
  FAILED_CHECKS+=("Tracked file extensions (exit $result)")
fi

if command -v scc >/dev/null 2>&1; then
  run_report \
    "Language and code counts (scc)" \
    "$OUT/inventory/code-counts.txt" \
    scc "$REPO"
elif command -v tokei >/dev/null 2>&1; then
  run_report \
    "Language and code counts (tokei)" \
    "$OUT/inventory/code-counts.txt" \
    tokei "$REPO"
else
  echo "[WARNING] Skipping code count checks, missing Tokei or SCC."
  SKIPPED_CHECKS+=("Code counts: install scc or tokei")
fi

################################################
# Current size and tracked artifact candidates #
################################################

info "Running: Repository sizes"

{
  printf 'Total checkout size:\n'
  du -sh "$REPO"

  printf '\nGit directory size:\n'
  GIT_DIR="$(git -C "$REPO" rev-parse --absolute-git-dir)"
  du -sh "$GIT_DIR"

  printf '\nDirectory sizes, depth 2:\n'
  du -h --max-depth=2 "$REPO" 2>/dev/null | sort -hr
} >"$OUT/inventory/sizes.txt" 2>&1

result=$?
if ((result != 0)); then
  FAILED_CHECKS+=("Repository sizes (exit $result)")
fi

info "Running: Largest current files"

find "$REPO" \
  -path "$REPO/.git" -prune -o \
  -type f -printf '%s\t%p\n' |
  sort -nr |
  sed -n '1,100p' \
  >"$OUT/inventory/largest-current-files.txt"

result=$?
if ((result != 0)); then
  FAILED_CHECKS+=("Largest current files (exit $result)")
fi

info "Running: Tracked artifact candidates"

awk '
  /(^|\/)(node_modules|\.venv|venv|\.next|\.nuxt|dist|build|coverage|__pycache__)\// ||
  /\.(zip|tar|gz|7z|db|sqlite|sqlite3|parquet|csv|xlsx|pdf|mp4|mov|onnx|pt|pkl)$/ {
    print
  }
' "$OUT/inventory/tracked-files.txt" \
  >"$OUT/inventory/tracked-artifact-candidates.txt"

result=$?
if ((result != 0)); then
  FAILED_CHECKS+=("Tracked artifact candidates (exit $result)")
fi

############################
# Contributors and history #
############################

run_report \
  "Contributors" \
  "$OUT/history/contributors.txt" \
  git -C "$REPO" shortlog -sne --all

run_report \
  "Recent commits" \
  "$OUT/history/recent-commits.txt" \
  git -C "$REPO" log -50 --date=short --format='%h %ad %an %s'

info "Running: Commit activity by month"

git -C "$REPO" log --all --format='%ad' --date=format:'%Y-%m' |
  sort |
  uniq -c \
  >"$OUT/history/commits-by-month.txt"

result=$?
if ((result != 0)); then
  FAILED_CHECKS+=("Commit activity by month (exit $result)")
fi

info "Running: Frequently changed paths"

git -C "$REPO" log --all --format= --name-only |
  sed '/^$/d' |
  sort |
  uniq -c |
  sort -nr |
  sed -n '1,100p' \
  >"$OUT/history/frequently-changed-paths.txt"

result=$?
if ((result != 0)); then
  FAILED_CHECKS+=("Frequently changed paths (exit $result)")
fi

###########################################
# Git object storage and historical blobs #
###########################################

run_report \
  "Git object database" \
  "$OUT/history/git-object-database.txt" \
  git -C "$REPO" count-objects -vH

info "Running: Largest historical blobs"

git -C "$REPO" rev-list --objects --all |
  git -C "$REPO" cat-file \
    --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' |
  awk '$1 == "blob" { print $3 "\t" $2 "\t" $4 }' |
  sort -nr |
  sed -n '1,100p' \
  >"$OUT/history/largest-historical-blobs.txt"

result=$?
if ((result != 0)); then
  FAILED_CHECKS+=("Largest historical blobs (exit $result)")
fi

if has_git_extension sizer; then
  run_report \
    "git-sizer" \
    "$OUT/history/git-sizer.txt" \
    git -C "$REPO" sizer --verbose
else
  echo "[WARNING] Skipping git-sizer checks, the plugin is not installed."
  SKIPPED_CHECKS+=("git-sizer: not installed")
fi

if has_git_extension filter-repo; then
  run_report \
    "git-filter-repo analysis" \
    "$OUT/history/git-filter-repo.txt" \
    git -C "$REPO" filter-repo \
      --analyze \
      --report-dir "$OUT/history/filter-repo-analysis"
else
  echo "[WARNING] Skipping git-filter-repo checks, the plugin is not installed."
  SKIPPED_CHECKS+=("git-filter-repo: not installed")
fi

#######################################
# Review guide and completion summary #
#######################################

cat >"$OUT/REVIEW.md" <<'EOF'
# Short repository survey

## Repository makeup

- `inventory/context.txt`: Which checkout and commit were surveyed?
- `inventory/structure.txt`: What does the top of the checkout contain?
- `inventory/project-files.txt`: What defines dependencies and operations?
- `inventory/code-counts.txt`, if generated: Which languages and how much code?
- `inventory/file-extensions.txt`: What types of files are tracked?

## Size

- `inventory/sizes.txt`: Is the checkout large, the Git directory large, or both?
- `inventory/largest-current-files.txt`: Which current files take the most space?
- `inventory/tracked-artifact-candidates.txt`: Are generated files or assets tracked?
- `history/largest-historical-blobs.txt`: Which large files remain in history?
- `history/git-sizer.txt` and `history/filter-repo-analysis/`: Optional deeper analysis.

## People and activity

- `history/contributors.txt`: Who has committed?
- `history/recent-commits.txt`: What changed recently?
- `history/commits-by-month.txt`: When has work been active?
- `history/frequently-changed-paths.txt`: Which paths change most often?

Use the full survey guide if this inventory suggests security, supply-chain,
language-specific maintainability, or Git cleanup work.
EOF

{
  echo

  echo "------------------------------------------"
  echo "[ Survey finished ]"
  echo

  printf 'Repository: %s\n' "$REPO"
  printf 'Reports: %s\n' "$OUT"

  if ((${#SKIPPED_CHECKS[@]} > 0)); then
    printf '\nSkipped optional checks:\n'
    printf '  - %s\n' "${SKIPPED_CHECKS[@]}"
  fi

  if ((${#FAILED_CHECKS[@]} > 0)); then
    printf '\nChecks that returned errors:\n'
    printf '  - %s\n' "${FAILED_CHECKS[@]}"
  fi

  printf '\nReview guide:\n'
  printf '  less %q\n' "$OUT/REVIEW.md"

  printf '\nRepository makeup:\n'
  printf '  less %q\n' "$OUT/inventory/context.txt"
  printf '  less %q\n' "$OUT/inventory/structure.txt"
  printf '  less %q\n' "$OUT/inventory/project-files.txt"

  if [[ -f "$OUT/inventory/code-counts.txt" ]]; then
    printf '  less %q\n' "$OUT/inventory/code-counts.txt"
  fi

  printf '\nSize and tracked artifacts:\n'
  printf '  less %q\n' "$OUT/inventory/sizes.txt"
  printf '  less %q\n' "$OUT/inventory/largest-current-files.txt"
  printf '  less %q\n' "$OUT/inventory/tracked-artifact-candidates.txt"

  printf '\nContributors and activity:\n'
  printf '  less %q\n' "$OUT/history/contributors.txt"
  printf '  less %q\n' "$OUT/history/recent-commits.txt"
  printf '  less %q\n' "$OUT/history/frequently-changed-paths.txt"

  printf '\nGit history and storage:\n'
  printf '  less %q\n' "$OUT/history/git-object-database.txt"
  printf '  less %q\n' "$OUT/history/largest-historical-blobs.txt"

  if [[ -f "$OUT/history/git-sizer.txt" ]]; then
    printf '  less %q\n' "$OUT/history/git-sizer.txt"
  fi

  if [[ -d "$OUT/history/filter-repo-analysis" ]]; then
    printf '  ls %q\n' "$OUT/history/filter-repo-analysis"
  fi

} | tee "$OUT/SUMMARY.txt"

exit 0

```
