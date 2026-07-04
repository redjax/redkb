---
title: "Tips & Tricks"
date: 2026-07-04T03:08:07-04:00
draft: true
weight: 10
toc: true
keywords: []
tags: []
---

**TODO**:

- Write introductory paragraph.

## Test trigger with empty commit

For fully automatic pipelines, i.e. ones that run on PR open or merge, you can trigger the behavior by adding a `push` to your branch, then pushing an empty commit.

For example, in the [`hugo-release.yml` pipeline](../.github/workflows/hugo-release.yml), the pipeline watches for changes to `.version` and `.bumpversion.toml` on pull requests that are merged to the `main` branch:

```yaml
---
name: Hugo release

on:
  push:
    branches:
      - main
    paths:
      - ".version"
      - ".bumpversion.toml"
```

To test this automatic trigger from your branch, you can add the current branch name, i.e. `feat/something-automatic`, disable path filtering, and push an empty commit:

```shell
---
name: Hugo release

on:
  push:
    branches:
      - main
      ## Watch the current branch, in addition to main.
      #  Remove this when you're done testing, before
      #  merging back into main
      - feat/something-automatic

    ## Temporarily disable path watching
    # paths:
    #   - ".version"
    #   - ".bumpversion.toml"
```

Commit these changes, push them, then create and push an empty commit to trigger it:

```yaml
git commit --allow-empty -m "chore: test workflow trigger"
git push
```

> [!IMPORTANT]
> Don't forget to put your triggers back to normal after a successful test. Remove the branch and uncomment any filtering rules that should run on `main`.
