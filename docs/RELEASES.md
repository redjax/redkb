# RedKB - Release Documentation <!-- omit in toc -->

The repository uses a [workflow defined in my PipelineTemplates repository](https://github.com/redjax/PipelineTemplates/blob/main/.github/workflows/hugo-publish.yml) to build and publish the Hugo site. The pipelines in this repository are meant to be "stubs" that call functionality centralized in the PipelineTemplates repository.

## Table of Contents <!-- omit in toc -->

- [Overview](#overview)
- [Diagrams](#diagrams)
  - [General pipeline flow](#general-pipeline-flow)
  - [Manual Trigger](#manual-trigger)
  - [Merge to main Trigger](#merge-to-main-trigger)
  - [Publish Only](#publish-only)

## Overview

When a pull request is merged into the `main` branch, the [`hugo-version-bump.yml` pipeline](../.github/workflows/hugo-version-bump.yml) will trigger if any files related to the Hugo site have changed. The detect rules are listed at the top of the pipeline and may change over time, but generally the patterns it searches for are:

- `archetypes/**`
- `content/**`
- `data/**`
- `i18n/**`
- `static/**`
- `hugo.yml`
- `go.mod`
- `go.sum`

If it detects changes, it bumps the [`.version` file](../.version) at the repository root, opens a pull request to the `main` branch with the bumped version, and automatically merges it.

Merges to `main` where `.version` (or `.bumpversion.toml`) have changed trigger the [`hugo-tag.yml` pipeline](../.github/workflows/hugo-tag.yml), which creates a [tag in the repository](https://github.com/redjax/redkb/tags) for the new version.

When a new tag is created, the [`hugo-build.yml` pipeline](../.github/workflows/hugo-build.yml) triggers, building the site with Hugo and uploading them as artifacts to the pipeline When the build finishes, it triggers the [`hugo-release.yml` pipeline](../.github/workflows/hugo-release.yml).

The release pipeline checks inputs to see which releases to do (Github Pages, Cloudflare Pages (not used currently), or a Github release). If the pipeline determines a release should occur, it calls the [`hugo-publish.yml` pipeline](../.github/workflows/hugo-publish.yml). By default the pipeline will create a Github release and publish to Github Pages.

The first thing to publish is a [Github release](https://github.com/redjax/redkb/releases). This will upload any archives created by the build pipeline to a release matching the current version, i.e. `site-v1.2.3`, or if the pipeline was triggered manually, a release that has the current commit hash appended, i.e. `site-b6fdbad`.

Finally, the pipeline will download the latest release asset and deploy it to Github Pages.

## Diagrams

### General pipeline flow

```mermaid
flowchart LR
  A[hugo-version-bump.yml] --> B[hugo-tag.yml]
  B --> C[hugo-build.yml]
  C --> D[hugo-release.yml]
  D --> E[GitHub Release]
  D --> F[GitHub Pages]
```

### Manual Trigger

```mermaid
flowchart TD
  A[Manual trigger: Hugo build] --> B[Build site]
  B --> C{Create release?}
  C -- No --> D[Stop]
  C -- Yes --> E[Name release site-<commit-hash>]
  E --> F{Deploy Pages?}
  F -- No --> G[Stop]
  F -- Yes --> H[Release workflow]
  H --> I[Download build artifact by run ID]
  I --> J[Create GitHub Release]
  J --> K[Deploy GitHub Pages]
```

### Merge to main Trigger

```mermaid
flowchart TD
  A[Change on main] --> B[Version bump PR created]
  B --> C[Auto-merge PR]
  C --> D[Tag workflow runs]
  D --> E[Create tag site-vX.Y.Z]
  E --> F[Build workflow runs]
  F --> G[Build site]
  G --> H[Name release site-vX.Y.Z]
  H --> I[Release workflow]
  I --> J[Download build artifact by run ID]
  J --> K[Create GitHub Release]
  K --> L[Deploy GitHub Pages]
```

### Publish Only

```mermaid
flowchart TD
  A[Manual publish trigger] --> B[Select build run ID]
  B --> C{Target}
  C -- branch --> D[Deploy branch]
  C -- github-pages --> E[Deploy GitHub Pages]
  C -- cloudflare-pages --> F[Deploy Cloudflare Pages]
  C -- github-release --> G[Create GitHub Release]
```
