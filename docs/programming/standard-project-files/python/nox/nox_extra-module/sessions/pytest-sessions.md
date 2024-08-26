---
tags:
    - standard-project-files
    - python
    - nox
    - pytest
---

# pytest

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
