---
title: Scripts
date: 2024-10-23T00:00:00-00:00
draft: false
weight: 0
tags:
  - snippets
  - bash
  - scripts
lastmod: "2026-04-13T04:15:27Z"
---

Re-usable Bash scripts. Copy/paste the contents of a script below into a `.sh` file and run `chmod +x <name-of-file>.sh` to make it executable.

## Prune git branches

After deleting a git branch from a remote, the local copy will still exist. Delete/"prune" all local git branches that do not exist on the remote:

```bash title="prune-git-branches.sh" linenums="1"
#!/bin/bash

git fetch -p && for branch in $(git for-each-ref --format '%(refname) %(upstream:track)' refs/heads | awk '$2 == "[gone]" {sub("refs/heads/", "", $1); print $1}'); do git branch -D $branch; done

exit $?
```
