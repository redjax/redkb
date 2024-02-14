---
tags:
    - standard-project-files
    - python
    - nox
---

# pre-commit nox sessions

Code snippets for `nox` sessions

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

## Run pytests with xdist

`pytest-xdist` runs tests concurrently, significantly improving test execution speed.

```py title="noxfile.py" linenums="1"
## Run pytest with xdist, allowing concurrent tests
@nox.session(python=PY_VERSIONS, name="tests")
@nox.parametrize("pdm_ver", [PDM_VER])
def run_tests(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")
    session.run("pdm", "install")

    print("Running Pytest tests")
    session.run(
        "pdm",
        "run",
        "pytest",
        "-n",
        "auto",
        "--tb=auto",
        "-v",
        "-rsXxfP",
    )
```

## Run pytests

```py title="noxfile.py" linenums="1"
## Run pytest
@nox.session(python=PY_VERSIONS, name="tests")
@nox.parametrize("pdm_ver", [PDM_VER])
def run_tests(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")
    session.run("pdm", "install")

    print("Running Pytest tests")
    session.run(
        "pdm",
        "run",
        "pytest",
        "--tb=auto",
        "-v",
        "-rsXxfP",
    )
```
