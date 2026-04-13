---
title: "Pre-commit Hooks"
date: 2024-02-12T00:00:00-00:00
draft: false
weight: 10
keywords: []
tags:
  - pre-commit
  - reference
lastmod: "2026-04-13T04:15:27Z"
---

Some [`pre-commit`](https://pre-commit.com/) hooks I use frequently.

## Example .pre-commit-config.yaml file

```yaml title=".pre-commit-config.yaml" linenums="1"

repos:

- repo: https://gitlab.com/vojko.pribudic.foss/pre-commit-update
  rev: v0.1.1
  hooks:
    - id: pre-commit-update

- repo: https://github.com/kynan/nbstripout
  rev: 0.6.1
  hooks:
    - id: nbstripout

```

## Auto-update pre-commit hooks

This hook will update the revisions for all installed hooks each time `pre-commit` runs.

```yaml title=".pre-commit-config.yaml" linenums="1"

- repo: https://gitlab.com/vojko.pribudic.foss/pre-commit-update
  rev: v0.1.1
  hooks:
    - id: pre-commit-update
      args: [--dry-run --exclude black --keep isort]
```

## Automatically strip Jupyter notebooks on commit

This hook will scan for jupyter notebooks (`.ipynb`) and clear any cell output before committing.

```yaml title=".pre-commit-config.yaml" linenums="1"

- repo: https://github.com/kynan/nbstripout
  rev: 0.6.1
  hooks:
    - id: nbstripout

```
