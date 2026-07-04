#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

last_version_commit="$(git log --format=%H -- .version | tail -n 1 || true)"
if [[ -z "${last_version_commit}" ]]; then
  last_version_commit="$(git rev-list --max-parents=0 HEAD | tail -n 1)"
fi

commits="$(git log --format=%B "${last_version_commit}..HEAD" -- \
  archetypes content data i18n static hugo.yml go.mod go.sum || true)"

bump="patch"
if grep -Eq 'BREAKING CHANGES|^feat!:' <<<"${commits}"; then
  bump="major"
elif grep -Eq '^feat(\(.+\))?:' <<<"${commits}"; then
  bump="minor"
elif grep -Eq '^fix(\(.+\))?:' <<<"${commits}"; then
  bump="patch"
fi

bump-my-version bump "${bump}" --config-file .bumpversion.toml
