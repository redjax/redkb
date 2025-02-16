---
tags:
    - git
---

# Rewrite Git History

If you have multiple `git` profiles, you will eventually mistakenly push a commit from the wrong author. For example, if you have a work and personal git account, and you write a quick patch for a personal project and commit the code from your work account, your "collaborators" on Github will show your work account.

If you wish to fix this, you can use the steps below to rewrite Git history, replacing any reference to your work profile with your personal one.

## Requirements

- [Python](https://www.python.org) (if you're on Linux or Mac, you do not need to install this).
- The [`git-filter-repo` package](https://pypi.org/project/git-filter-repo/)
    - Install with `pip install git-filter-repo`

## Steps

Clone the repository in a new directory using the `--bare` flag, i.e.: `git clone --bare git@github.com:user/repo.git`. This will create a local copy of your repository's HEAD refs; you will not see your code, but instead will see directories like `branches/`, `tags/`, etc. This is essentially the metadata for your repository, as well as the git history.

Run a command like the following, replacing the `Old Name`, `old.email@example.com`, `New Name`, and `new.email@example.com` with your old/new author:

```shell title="Replace git author in history" linenums="1"
git filter-branch --env-filter '
if [ "$GIT_COMMITTER_NAME" = "Old Name" ] && [ "$GIT_COMMITTER_EMAIL" = "old.email@example.com" ]; then
    GIT_COMMITTER_NAME="New Name"
    GIT_COMMITTER_EMAIL="new.email@example.com"
    GIT_AUTHOR_NAME="New Name"
    GIT_AUTHOR_EMAIL="new.email@example.com"
fi
' --tag-name-filter cat -- --branches --tags

```

Clean your refs and ensure proper pruning:

```shell title="Clean git refs" linenums="1"
git reflog expire --expire=now --all
git gc --prune=now

```

Finally, force-push your changes:

```shell title="Force push git changes" linenums="1"
git push --force --all
git push --force --tags

```

Re-clone the repository, this time without `--bare`, and use `git log --author="Old Name"` to ensure all refs have been removed.
