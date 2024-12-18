---
tags:
    - standard-project-files
    - python
    - nox
---

# Nox

[`nox`](https://nox.thea.codes/en/stable/) is a very useful utility for running tasks in a project. By creating a `noxfile.py` and adding `nox` sessions to it, you can automate tasks like building the project, exporting `requirements.txt`, and linting code (and more).

`nox` is versatile. If you can run a command in your shell, you should be able to automate it with `nox`. The idea is that `nox` sessions can run the same way in any environment (local, CI/CD pipelines, and cross-platform). For example, my [`Ansible homelab` repository](https://github.com/redjax/ansible_homelab) uses a [`noxfile.py`](https://github.com/redjax/ansible_homelab/blob/main/noxfile.py) to automate running Ansible playbooks.

!!! note
    Check the documentation for [making your `noxfile.py` modular](nox_extra-module/index.md) to keep your `noxfile.py` short & clean by import sessions from a `nox_extra/` directory in your project.


## noxfile.py base

The basis for most/all of my projects' `noxfile.py`. 

!!!note

    If running all sessions with `$ nox`, only the sessions defined in `nox.sessions` will be executed. The list of sessions is conservative to start in order to maintain as generic a `nox` environment as possible.

    Enabled sessions:

    - lint
    - export
    - tests

```py title="noxfile.py" linenums="1"
from __future__ import annotations

import logging
import logging.config
import logging.handlers
import os
from pathlib import Path
import platform
import shutil
import importlib.util

import nox

## Set nox options
if importlib.util.find_spec("uv"):
    nox.options.default_venv_backend = "uv|virtualenv"
else:
    nox.options.default_venv_backend = "virtualenv"
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False
nox.options.error_on_missing_interpreters = False
# nox.options.report = True

## Define sessions to run when no session is specified
nox.sessions = ["lint", "export", "tests"]

## Detect container env, or default to False
if "CONTAINER_ENV" in os.environ:
    CONTAINER_ENV: bool = os.environ["CONTAINER_ENV"]
else:
    CONTAINER_ENV: bool = False

## Create logger for this module
log: logging.Logger = logging.getLogger("nox")

## Define versions to test
PY_VERSIONS: list[str] = ["3.12", "3.11"]
## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE: tuple[str, str, str] = platform.python_version_tuple()
## Dynamically set Python version
DEFAULT_PYTHON: str = f"{PY_VER_TUPLE[0]}.{PY_VER_TUPLE[1]}"

## Set PDM version to install throughout
PDM_VER: str = "2.15.4"
## Set paths to lint with the lint session
LINT_PATHS: list[str] = ["src", "tests"]

## Set directory for requirements.txt file output
REQUIREMENTS_OUTPUT_DIR: Path = Path("./requirements")


def setup_nox_logging(
    level_name: str = "DEBUG", disable_loggers: list[str] | None = []
) -> None:
    """Configure a logger for the Nox module.

    Params:
        level_name (str): The uppercase string representing a logging logLevel.
        disable_loggers (list[str] | None): A list of logger names to disable, i.e. for 3rd party apps.
            Note: Disabling means setting the logLevel to `WARNING`, so you can still see errors.

    """
    ## If container environment detected, default to logging.DEBUG
    if CONTAINER_ENV:
        level_name: str = "DEBUG"

    logging_config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "nox": {
                "level": level_name.upper(),
                "handlers": ["console"],
                "propagate": False,
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "nox",
                "level": "DEBUG",
                "stream": "ext://sys.stdout",
            }
        },
        "formatters": {
            "nox": {
                "format": "[NOX] [%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
                "datefmt": "%Y-%m-%D %H:%M:%S",
            }
        },
    }

    ## Configure logging. Only run this once in an application
    logging.config.dictConfig(config=logging_config)

    ## Disable loggers by name. Sets logLevel to logging.WARNING to suppress all but warnings & errors
    for _logger in disable_loggers:
        logging.getLogger(_logger).setLevel(logging.WARNING)


def append_lint_paths(search_patterns: str | list[str] = None, lint_paths: list[str] = None):
    if lint_paths is None:
        lint_paths = []

    if search_patterns is None:
        return lint_paths

    if isinstance(search_patterns, str):
        search_patterns = [search_patterns]

    for pattern in search_patterns:
        for path in Path('.').rglob(pattern):
            relative_path = Path('.').joinpath(path).resolve().relative_to(Path('.').resolve())
            
            if f"{relative_path}" not in lint_paths:
                lint_paths.append(f"./{relative_path}")

    log.debug(f"Lint paths: {lint_paths}")
    return lint_paths


setup_nox_logging()

log.info(f"[container_env:{CONTAINER_ENV}]")

## Ensure REQUIREMENTS_OUTPUT_DIR path exists
if not REQUIREMENTS_OUTPUT_DIR.exists():
    try:
        REQUIREMENTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        msg = Exception(
            f"Unable to create requirements export directory: '{REQUIREMENTS_OUTPUT_DIR}'. Details: {exc}"
        )
        log.error(msg)

        REQUIREMENTS_OUTPUT_DIR: Path = Path(".")

## List of dicts describing a src file to copy to a specified destination file
#  Ex: {"src": "config/.secrets.example.toml", "dest": "config/.secrets.toml"}
INIT_COPY_FILES: list[dict[str, str]] = []


@nox.session(python=PY_VERSIONS, name="build-env", tags=["env", "build", "setup"])
@nox.parametrize("pdm_ver", [PDM_VER])
def setup_base_testenv(session: nox.Session, pdm_ver: str):
    log.debug(f"Default Python: {DEFAULT_PYTHON}")
    session.install(f"pdm>={pdm_ver}")

    log.info("Installing dependencies with PDM")
    session.run("pdm", "sync")
    session.run("pdm", "install")


@nox.session(python=[DEFAULT_PYTHON], name="lint", tags=["quality"])
def run_linter(session: nox.Session):
    session.install("ruff")
    session.install("black")

    log.info("Linting code")
    for d in LINT_PATHS:
        if not Path(d).exists():
            log.warning(f"Skipping lint path '{d}', could not find path")
            pass
        else:
            lint_path: Path = Path(d)
            log.info(f"Running ruff imports sort on '{d}'")
            session.run(
                "ruff",
                "check",
                lint_path,
                "--select",
                "I",
                "--fix",
            )

            log.info(f"Formatting '{d}' with Black")
            session.run(
                "black",
                lint_path,
            )

            log.info(f"Running ruff checks on '{d}' with --fix")
            session.run(
                "ruff",
                "check",
                lint_path,
                "--fix",
            )

    log.info("Linting noxfile.py")
    session.run(
        "ruff",
        "check",
        f"{Path('./noxfile.py')}",
        "--fix",
    )


@nox.session(python=[DEFAULT_PYTHON], name="export", tags=["requirements"])
@nox.parametrize("pdm_ver", [PDM_VER])
def export_requirements(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")

    log.info("Exporting production requirements")
    session.run(
        "pdm",
        "export",
        "--prod",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt",
        "--without-hashes",
    )

    log.info("Exporting development requirements")
    session.run(
        "pdm",
        "export",
        "-d",
        "-o",
        f"{REQUIREMENTS_OUTPUT_DIR}/requirements.dev.txt",
        "--without-hashes",
    )


@nox.session(python=PY_VERSIONS, name="tests", tags=["test"])
@nox.parametrize("pdm_ver", [PDM_VER])
def run_tests(session: nox.Session, pdm_ver: str):
    session.install(f"pdm>={pdm_ver}")
    session.run("pdm", "install")

    log.info("Running Pytest tests")
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


@nox.session(python=PY_VERSIONS, name="pre-commit-all", tags=["repo", "pre-commit"])
def run_pre_commit_all(session: nox.Session):
    session.install("pre-commit")
    session.run("pre-commit")

    log.info("Running all pre-commit hooks")
    session.run("pre-commit", "run")


@nox.session(python=PY_VERSIONS, name="pre-commit-update", tags=["repo", "pre-commit"])
def run_pre_commit_autoupdate(session: nox.Session):
    session.install(f"pre-commit")

    log.info("Running pre-commit autoupdate")
    session.run("pre-commit", "autoupdate")


@nox.session(python=PY_VERSIONS, name="pre-commit-nbstripout", tags=["repo", "pre-commit"])
def run_pre_commit_nbstripout(session: nox.Session):
    session.install(f"pre-commit")

    log.info("Running nbstripout pre-commit hook")
    session.run("pre-commit", "run", "nbstripout")


@nox.session(python=[PY_VER_TUPLE], name="init-setup", tags=["setup"])
def run_initial_setup(session: nox.Session):
    log.info(f"Running initial setup.")
    if INIT_COPY_FILES is None:
        log.warning(f"INIT_COPY_FILES is empty. Skipping")
        pass

    else:

        for pair_dict in INIT_COPY_FILES:
            src = Path(pair_dict["src"])
            dest = Path(pair_dict["dest"])
            if not dest.exists():
                log.info(f"Copying {src} to {dest}")
                try:
                    shutil.copy(src, dest)
                except Exception as exc:
                    msg = Exception(
                        f"Unhandled exception copying file from '{src}' to '{dest}'. Details: {exc}"
                    )
                    log.error(msg)

```

## Extending the noxfile

Check the [`nox_extra` module](nox_extra-module/index.md) for information on extending `nox` with custom sessions.

## noxfile.py helper functions

### Install UV project

You can install your UV project in the `noxfile.py` with function. Copy/paste this somewhere towards the top of your code, then add to any sessions where you want to install the whole project.

```python title="Install UV in session" linenums="1"
import nox

from pathlib import Path


# this VENV_DIR constant specifies the name of the dir that the `dev`
# session will create, containing the virtualenv;
# the `resolve()` makes it portable
VENV_DIR = Path("./.venv").resolve()


def install_uv_project(session: nox.Session, external: bool = False) -> None:
    """Method to install uv and the current project in a nox session."""
    log.info("Installing uv in session")
    session.install("uv")
    log.info("Syncing uv project")
    session.run("uv", "sync", external=external)
    log.info("Installing project")
    session.run("uv", "pip", "install", ".", external=external)

```

Example session using `install_uv_project()`:

```python title="Session that uses install_uv_project()" linenums="1"
@nox.session(name="dev-env", tags=["setup"])
def dev(session: nox.Session) -> None:
    """Sets up a python development environment for the project.

    Run this on a fresh clone of the repository to automate building the project with uv.
    """
    install_uv_project(session, external=True)

```

### @cd context manager

This context manager allows you to change the directory a command is run from.

```python title="@cd context manager" linenums="1"
import nox

from contextlib import contextmanager
import os
import importlib.util
import typing as t


@contextmanager
def cd(new_dir) -> t.Generator[None, importlib.util.Any, None]: # type: ignore
    """Context manager to change a directory before executing command."""
    prev_dir: str = os.getcwd()
    os.chdir(os.path.expanduser(new_dir))
    try:
        yield
    finally:
        os.chdir(prev_dir)

```

### find_free_port()

This function can find a free port using the `socket` library. This is useful for sessions that run a service, like `mkdocs-serve`. Instead of hard-coding the port and risking an in-use port, this function can find a free port to pass to the function.

```python title="find_free_port()" linenums="1"
import nox
import socket


def find_free_port(start_port=8000) -> int:
    """Find a free port starting from a specific port number."""
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except socket.error:
                log.info(f"Port {port} is in use, trying the next port.")
                port += 1

```

Example usage:

```python title="Example usage for find_free_port()" linenums="1"
import nox


@nox.session(name="serve-mkdocs", tags=["mkdocs", "serve"])
def serve_mkdocs(session: nox.Session) -> None:
    install_uv_project(session)
    
    free_port = find_free_port(start_port=8000)
    
    log.info(f"Serving MKDocs site on port {free_port}")
    
    try:
        session.run("mkdocs", "serve", "--dev-addr", f"0.0.0.0:{free_port}")
    except Exception as exc:
        msg = f"({type(exc)}) Unhandled exception serving MKDocs site. Details: {exc}"
        log.error(msg)

```
