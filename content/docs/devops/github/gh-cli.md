---
title: "gh CLI"
date: 2026-07-04T03:09:01-04:00
draft: true
weight: 10
toc: true
keywords: []
tags:
  - github
  - ci-cd
  - devops
---

The [Github CLI](https://cli.github.com) is a terminal interface for interacting with Github repositories. You can use it within a pipeline/action to simplify interactions with your repositories, such as creating and merging pull requests, triggering pipelines, etc.

## Authenticating with Github CLI

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
