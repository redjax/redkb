---
title: "gh CLI"
date: 2026-07-04T03:09:01-04:00
draft: true
weight: 10
toc: true
keywords: []
tags: []
---

**TODO**:

- Flesh out description
- Break into more logical sections
- Create commands cheatsheet

The [Github CLI](https://cli.github.com) is a terminal interface for interacting with Github repositories.

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
