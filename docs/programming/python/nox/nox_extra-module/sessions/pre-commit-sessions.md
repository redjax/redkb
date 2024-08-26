---
tags:
    - standard-project-files
    - python
    - nox
    - pre-commit
---

# pre-commit

## Run all pre-commit hooks

```py title="noxfile.py" linenums="1"
## Run all pre-commit hooks
@nox.session(python=PY_VERSIONS, name="pre-commit-all")
def run_pre_commit_all(session: nox.Session):
    session.install("pre-commit")
    session.run("pre-commit")

    print("Running all pre-commit hooks")
    session.run("pre-commit", "run")

```

## Automatically update pre-commit hooks on new revisions

```py title="noxfile.py" linenums="1"
## Automatically update pre-commit hooks on new revisions
@nox.session(python=PY_VERSIONS, name="pre-commit-update")
def run_pre_commit_autoupdate(session: nox.Session):
    session.install(f"pre-commit")

    print("Running pre-commit update hook")
    session.run("pre-commit", "run", "pre-commit-update")
```
