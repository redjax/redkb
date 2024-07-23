---
tags:
    - standard-project-files
    - pre-commit
---

# pre-commit hooks

Some [`pre-commit`](https://pre-commit.com/) hooks I use frequently.

## Example .pre-commit-config.yaml file

```yaml title=".pre-commit-config.yaml" linenums="1"

repos:

- repo: https://gitlab.com/vojko.pribudic/pre-commit-update
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

- repo: https://gitlab.com/vojko.pribudic/pre-commit-update
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