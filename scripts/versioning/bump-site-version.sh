#!/usr/bin/env bash
set -euo pipefail

if ! command -v bump-my-version >/dev/null 2>&1; then
  echo "[ERROR] bump-my-version is not installed." >&2
  exit 1
fi

cd "$(git rev-parse --show-toplevel)"

## When these paths change, a version bump occurs
paths=(
  archetypes
  content
  data
  i18n
  static
  hugo.yml
  go.mod
  go.sum
)

function debug() {
  printf '[version-bump] %s\n' "$*"
}

## Find commits where files in the $paths array changed
function collect_commits() {
  git log --format=%s%n%b "$@" -- "${paths[@]}" || true
}

debug "HEAD=$(git rev-parse --short HEAD)"

## Determie if commit was a branch merge, or a squash merge
if git rev-parse -q --verify HEAD^2 >/dev/null 2>&1; then
  debug "mode=merge"
  debug "parent1=$(git rev-parse --short HEAD^1)"
  debug "parent2=$(git rev-parse --short HEAD^2)"
  debug "range=HEAD^1..HEAD^2"

  commits="$(collect_commits HEAD^1..HEAD^2)"
else
  debug "mode=squash-or-linear"
  debug "range=HEAD"

  commits="$(git show -s --format=%s%n%b HEAD)"
fi

## Print discovered commits
debug "messages:"
while IFS= read -r line; do
  [[ -n "$line" ]] && debug "  $line"
done <<<"$commits"

bump="patch"
reason="default patch"

## Determine bump type
if grep -Eq 'BREAKING CHANGES|^feat!:' <<<"${commits}"; then
  bump="major"
  reason="breaking change"
elif grep -Eq '^feat(\(.+\))?:' <<<"${commits}"; then
  bump="minor"
  reason="feat detected"
elif grep -Eq '^fix(\(.+\))?:' <<<"${commits}"; then
  bump="patch"
  reason="fix detected"
fi

debug "decision=bump:${bump}"
debug "reason=${reason}"

## Do version bump
bump-my-version bump "${bump}" --config-file .bumpversion.toml
