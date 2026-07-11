# RedKB - Release Documentation <!-- omit in toc -->

This repository's [main release pipeline](../.github/workflows/hugo-main.yml) calls an [orchestrator pipeline in my centralized `PipelineTemplates` repository](https://github.com/redjax/PipelineTemplates/blob/topic/hugo-consolidated-pipelines/.github/workflows/hugo-site-main.yml). The pipeline(s) in this repository are simple "stubs" that pass the inputs required in the central repository's pipeline.

## Table of Contents <!-- omit in toc -->

- [Overview](#overview)
- [Diagrams](#diagrams)
  - [General pipeline flow](#general-pipeline-flow)
- [Using the Github CLI to trigger releases](#using-the-github-cli-to-trigger-releases)
  - [Authenticating with Github CLI](#authenticating-with-github-cli)
- [Test trigger with empty commit](#test-trigger-with-empty-commit)

## Overview

When a pull request is merged into the `main` branch, the pipeline will trigger if any files related to the Hugo site have changed. The detect rules are listed at the top of the pipeline and may change over time, but generally the patterns it searches for are:

- `archetypes/**`
- `content/**`
- `data/**`
- `i18n/**`
- `static/**`
- `hugo.yml`
- `go.mod`
- `go.sum`

If it detects changes, it bumps the [`.version` file](../.version) at the repository root, opens a pull request to the `main` branch with the bumped version, and automatically merges it.

Merges to `main` where `.version` (or `.bumpversion.toml`) have changed trigger the build, tag, release, and optionally publish stages of the pipeline. When a version bump occurs, the pipeline builds the site, then creates a [tag in the repository](https://github.com/redjax/redkb/tags) for the new version, and a [Github release](https://github.com/redjax/redkb/releases) with archived versions of the static site attached.

Finally, the pipeline will download the latest release asset and deploy it to Github Pages.

## Diagrams

### General pipeline flow

```mermaid
flowchart LR
  A[Hugo site file changes] --> B[Version bump]
  B --> C[Auto-merge bump PR to main]
  C --> D[Detect bumped version]
  D --> E[Build site, upload pipeline artifact]
  E --> F[Create Git tag site-vX.Y.Z or site-&ltcommit-hash&gt]
  F --> G[Create GitHub Release with static site archive]
  G --> H[Publish to github-pages]
```

## Using the Github CLI to trigger releases

When developing a pipeline, you may need to trigger it in a way the Github webUI doesn't allow. For example, if you create a brand new pipeline, or if you add a `workflow_dispatch` and have not merged the branch with this change yet.

You can use the [Github CLI](https://cli.github.com) to trigger a pipeline from a specific branch, in ways that the Github webUI doesn't allow. For example, if the [`hugo-main.yml` pipeline](../.github/workflows/hugo-main.yml) did not have a `workflow_dispatch` on the `main` branch, but you added one in a branch named `feat/manual-trigger-release`, you can test that trigger before merging the changes into `main`. If you went to this pipeline in the webUI, you would see there is no manual trigger button. This is because the `workflow_dispatch` change does not exist on the `main` branch.

You can trigger the pipeline manually with the `gh` CLI like:

```shell
gh workflow run hugo-main.yml --ref feat/manual-trigger-release
```

If a `workflow_dispatch` has inputs, you can pass them with `-f`, like:

```shell
gh workflow run pipeline-filename.yml \
  --ref feat/manual-trigger-release \
  -f input-one=false \
  -f input-two=some-value
```

### Authenticating with Github CLI

If you try to run a pipeline manually using the `gh` CLI, but you are not signed in or do not have admin privileges, you will see an error like:

```shell
could not create workflow dispatch event: HTTP 403: Must have admin rights to Repository.
```

To fix this, use a [Personal Access Token (PAT)](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) with the following permissions:

- Actions: Read and write
- Contents: Read and write
- Workflows: Read and write

You can also optionally add the below to enable more functionality via the `gh` CLI:

- Code scanning alerts: Read only
- Deployments: Read and write (to manage Github Pages deployments)
- Issues: Read and write (to manage issues from the CLI)
- Pages: Read and write (for managing Pages deployments)
- Pull requests: Read and write (to manage PRs from the CLI)

Then, run `gh auth login` to start the interactive login process. If you are not able to do the interactive method, export your token with:

```shell
export GH_TOKEN="<your-gh-PAT>"
```

Then, run your `gh` commands; they will use the `$GH_TOKEN` environment variable automatically. For example:

```shell
gh workflow run Some\ pipeline\ name --ref feat/branch-to-run-on
```

## Test trigger with empty commit

For fully automatic pipelines, i.e. ones that run on PR open or merge, you can trigger the behavior by adding a `push` to your branch, then pushing an empty commit.

For example, in the [`hugo-main.yml` pipeline](../.github/workflows/hugo-main.yml), the pipeline watches for changes to `.version` and `.bumpversion.toml` on pull requests that are merged to the `main` branch:

```yaml
---
name: Hugo Site Main

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
name: Hugo Site Main

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
