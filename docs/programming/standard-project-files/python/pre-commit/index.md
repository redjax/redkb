# pre-commit hooks

Some [`pre-commit`](pre-commit.com/) hooks I use frequently.

## autoupdate pre-commit hooks

This hook will update the revisions for all installed hooks each time `pre-commit` runs.

```yaml title=".pre-commit-config.yaml" linenums="1"
- repo: https://gitlab.com/vojko.pribudic/pre-commit-update
  rev: v0.1.1
  hooks:
    - id: pre-commit-update
      args: [--dry-run --exclude black --keep isort]
```
