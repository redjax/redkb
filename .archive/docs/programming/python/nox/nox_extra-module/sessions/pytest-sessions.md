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
def run_tests(session: nox.Session):
    ## Install your project
    session.install("-r", "requirements.txt")
    ## Ensure pytest is installed
    session.install("pyest-xdist")

    print("Running Pytest tests")
    session.run(
        "pytest",
        "-n",
        "auto",
        "--tb=auto",
        "-v",
        "-rsXxfP",
    )
```
