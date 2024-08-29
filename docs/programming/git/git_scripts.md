# Git Scripts

Snippets and scripts for `git`, for Bash and PowerShell.

## Git prune

When synching a Git repository to a remote like [GitHub](https://github.com) or [GitLab](https://gitlab.com), if you delete a branch on the remote, that branch is not deleted locally. If you create and delete branches frequently and don't regularly run `git branch -D <branch-name>`, you will end up with a very large local version of the repository, and a messy tree that's difficult to work with.

The scripts below list the branches on your remote, compare them to the local branches, and remove any that exist locally but not on the remote.

!!!warning

    Because these scripts work by comparison, if you have a local branch that has not been pushed to the remote yet, this script would delete that branch locally.

### Bash version

```bash title="prune_local_branches.sh" linenums="1"
#!/bin/bash

git fetch -p && for branch in $(git for-each-ref --format '%(refname) %(upstream:track)' refs/heads | awk '$2 == "[gone]" {sub("refs/heads/", "", $1); print $1}'); do git branch -D $branch; done

exit $?

```

## PowerShell version

```powershell title="prune_local_branches.ps1" linenums="1"
<#
    Description:
        This script checks out the main branch, fetches from the remote, then
        deletes (prunes) any local branches that still exist after being deleted
        on the remote.

        WARNING: This is a desctructive script. Make sure you don't need the local
        copy of your branch before pruning.
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
        git branch -d $_ 
    }
        
    Write-Host "Local branches pruned." -ForegroundColor Green

    exit 0
}
catch {
    Write-Warning "Error pruning local branches. Details: $($_.Exception.Message)"
    exit 1
}

```
