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

## Using the Github CLI to trigger releases

When developing a pipeline, you may need to trigger it in a way the Github webUI doesn't allow. For example, if you create a brand new pipeline, or if you add a `workflow_dispatch` and have not merged the branch with this change yet.

You can use the [Github CLI](https://cli.github.com) to trigger a pipeline from a specific branch, in ways that the Github webUI doesn't allow. For example, if the [`hugo-release.yml` pipeline](../.github/workflows/hugo-release.yml) did not have a `workflow_dispatch` on the `main` branch, but you added one in a branch named `feat/manual-trigger-release`, you can test that trigger before merging the changes into `main`. If you went to this pipeline in the webUI, you would see there is no manual trigger button. This is because the `workflow_dispatch` change does not exist on the `main` branch.

You can trigger the pipeline manually with the `gh` CLI like:

```shell
gh workflow run hugo-release.yml --ref feat/manual-trigger-release
```

If a `workflow_dispatch` has inputs, you can pass them with `-f`, like:

```shell
gh workflow run pipeline-filename.yml \
  --ref feat/manual-trigger-release \
  -f input-one=false \
  -f input-two=some-value
```

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
