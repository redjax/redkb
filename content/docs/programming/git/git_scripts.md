---
title: "Git Scripts"
date: 2024-08-28T00:00:00-00:00
draft: false
weight: 10
keywords: []
tags:
  - source-control
  - git
---

Snippets and scripts for `git`, for Bash and PowerShell.

## Git prune

When syncing a Git repository to a remote like [GitHub](https://github.com) or [GitLab](https://gitlab.com), if you delete a branch on the remote, that branch is not deleted locally. If you create and delete branches frequently and don't regularly run `git branch -D <branch-name>`, you will end up with a very large local version of the repository, and a messy tree that's difficult to work with.

The scripts below list the branches on your remote, compare them to the local branches, and remove any that exist locally but not on the remote.

> [!WARNING]
> Because these scripts work by comparison, if you have a local branch that has not been pushed to the remote yet, this script would delete that branch locally.

### Bash version

```bash title="prune_local_branches.sh" linenums="1"
#!/bin/bash

git fetch -p && for branch in $(git for-each-ref --format '%(refname) %(upstream:track)' refs/heads | awk '$2 == "[gone]" {sub("refs/heads/", "", $1); print $1}'); do git branch -D $branch; done

exit $?

```

If you are using Git worktrees, you might see an error like:

```plaintext
error: cannot delete branch 'example/branch-name; use by worktree at '/path/to/worktree-name'
```

This version skips any branches checked out by a worktree:

```shell title="prune_local_branches.sh" linenums="1"

#!/usr/bin/env bash

set -e

## Prune remote-tracking references that no longer exist.
git fetch --prune

## Check whether a branch is checked out in any worktree.
is_branch_in_worktree() {
  local branch="$1"

  git worktree list --porcelain |
    grep -Fqx "branch refs/heads/$branch"
}

## Find local branches whose upstream has been deleted.
git for-each-ref \
  --format='%(refname:short)%09%(upstream:track)' \
  refs/heads |
  awk -F '\t' '$2 == "[gone]" { print $1 }' |
  while IFS= read -r branch; do
    if is_branch_in_worktree "$branch"; then
      echo "Skipping '$branch' (checked out in a worktree)"
    else
      ## Use git branch -d for extra protection, but you will
      #  need to manually delete some branches.
      git branch -D "$branch"
    fi
  done

```

As an alternative, you can use this one-liner:

```shell
git fetch --prune && git for-each-ref --format='%(refname:short)%09%(upstream:track)' refs/heads | awk -F '\t' '$2 == "[gone]" {print $1}' | while IFS= read -r branch; do if git worktree list --porcelain | grep -Fqx "branch refs/heads/$branch"; then echo "Skipping '$branch' (checked out in a worktree)"; else git branch -D "$branch"; fi; done
```

### PowerShell version

```powershell title="Run-GitBranchPrune.ps1" linenums="1"
<#
    .SYNOPSIS
    Clean up local branches that have been deleted on the remote

    .DESCRIPTION
        This script checks out the main branch, fetches from the remote, then
        deletes (prunes) any local branches that still exist after being deleted
        on the remote.

        WARNING: This is a destructive script. Make sure you don't need the local
        copy of your branch before pruning.
    
    .PARAMETER MainBranch
        The name of the main branch.

    .EXAMPLE
        .\scripts\Prune-GitBranches.ps1
#>
param(
    [String]$MainBranch = "main"
)

Write-Host "Pruning local branches that have been deleted on the remote." -ForegroundColor Green

try {
    git checkout $($MainBranch); `
        git remote update origin --prune; `
        git branch -vv `
    | Select-String -Pattern ": gone]" `
    | ForEach-Object {
        $_.toString().Trim().Split(" ")[0]
    } `
    | ForEach-Object {
        git branch -D $_ 
    }

    Write-Host "Local branches pruned." -ForegroundColor Green

    exit 0
}
catch {
    Write-Warning "Error pruning local branches. Details: $($_.Exception.Message)"
    exit 1
}

```
