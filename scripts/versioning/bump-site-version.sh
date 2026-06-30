#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

last_version_commit="$(git log --format=%H -- .version | tail -n 1 || true)"
if [[ -z "$last_version_commit" ]]; then
  last_version_commit="$(git rev-list --max-parents=0 HEAD | tail -n 1)"
fi

commits="$(git log --format=%s "${last_version_commit}..HEAD" -- \
  archetypes content data i18n static hugo.yml go.mod go.sum || true)"

bump="patch"
if echo "$commits" | grep -Eq 'BREAKING CHANGE|!:'; then
  bump="major"
elif echo "$commits" | grep -Eq '^feat(\(.+\))?:'; then
  bump="minor"
fi

bump-my-version bump "$bump" --config-file .bumpversion.toml
