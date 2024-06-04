---
tags:
    - standard-project-files
    - python
    - nox
---

# Nox

I am still deciding between [`tox`](https://tox.wiki/en/stable/) and [`nox`](https://nox.thea.codes/en/stable/) as my preferred task runner, but I've been leaning more towards `nox` for the simple reason that it's nice to be able to write Python code for things like `try/except` and creating directories that don't exist yet.

## noxfile.py base

The basis for most/all of my projects' `noxfile.py`. 

!!!note

    The following are commented because they require additional setup, or may not be used in every project:
    
    - `INIT_COPY_FILES`
      - A list of dicts defining a file `src` and a `dest` to copy it to
      - This is useful for copying files like `config/.secrets.example.toml` -> `config/.secrets.toml`
    - The `init-setup` Nox session
      - Leave this session commented unless/until you've modified the default `INIT_COPY_FILES` variable

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

import nox

## Detect container env, or default to False
if "CONTAINER_ENV" in os.environ:
    CONTAINER_ENV: bool = os.environ["CONTAINER_ENV"]
else:
    CONTAINER_ENV: bool = False


def setup_nox_logging(
    level_name: str = "DEBUG", disable_loggers: list[str] | None = []
) -> None:
    """Configure a logger for the Nox module.

    Params:
        level_name (str): The uppercase string repesenting a logging logLevel.
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


setup_nox_logging()

## Create logger for this module
log: logging.Logger = logging.getLogger("nox")

log.info(f"[container_env:{CONTAINER_ENV}]")

## Set nox options
nox.options.default_venv_backend = "venv"
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False
nox.options.error_on_missing_interpreters = False
# nox.options.report = True

## Define sessions to run when no session is specified
nox.sessions = ["lint", "export", "tests"]

## Define versions to test
PY_VERSIONS: list[str] = ["3.12", "3.11"]
## Set PDM version to install throughout
PDM_VER: str = "2.15.4"
## Set paths to lint with the lint session
LINT_PATHS: list[str] = ["src", "tests"]

## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE: tuple[str, str, str] = platform.python_version_tuple()
## Dynamically set Python version
DEFAULT_PYTHON: str = f"{PY_VER_TUPLE[0]}.{PY_VER_TUPLE[1]}"

## Set directory for requirements.txt file output
REQUIREMENTS_OUTPUT_DIR: Path = Path("./requirements")

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

# INIT_COPY_FILES: list[dict[str, str]] = [
#     {"src": "config/.secrets.example.toml", "dest": "config/.secrets.toml"},
#     {"src": "config/settings.toml", "dest": "config/settings.local.toml"},
# ]


@nox.session(python=PY_VERSIONS, name="build-env")
@nox.parametrize("pdm_ver", [PDM_VER])
def setup_base_testenv(session: nox.Session, pdm_ver: str):
    log.debug(f"Default Python: {DEFAULT_PYTHON}")
    session.install(f"pdm>={pdm_ver}")

    log.info("Installing dependencies with PDM")
    session.run("pdm", "sync")
    session.run("pdm", "install")


@nox.session(python=[DEFAULT_PYTHON], name="lint")
def run_linter(session: nox.Session):
    session.install("ruff")
    # session.install("black")

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
                "--select",
                "I",
                "--fix",
                lint_path,
            )

            # log.info(f"Formatting '{d}' with Black")
            # session.run(
            #     "black",
            #     lint_path,
            # )

            log.info(f"Running ruff checks on '{d}' with --fix")
            session.run(
                "ruff",
                "check",
                # "--config",
                # "ruff.ci.toml",
                lint_path,
                "--fix",
            )

    log.info("Linting noxfile.py")
    session.run(
        "ruff",
        "check",
        # "--config",
        # "ruff.ci.toml",
        f"{Path('./noxfile.py')}",
        "--fix",
    )


@nox.session(python=[DEFAULT_PYTHON], name="export")
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

    # log.info("Exporting CI requirements")
    # session.run(
    #     "pdm",
    #     "export",
    #     "--group",
    #     "ci",
    #     "-o",
    #     f"{REQUIREMENTS_OUTPUT_DIR}/requirements.ci.txt",
    #     "--without-hashes",
    # )


@nox.session(python=PY_VERSIONS, name="tests")
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


@nox.session(python=PY_VERSIONS, name="pre-commit-all")
def run_pre_commit_all(session: nox.Session):
    session.install("pre-commit")
    session.run("pre-commit")

    log.info("Running all pre-commit hooks")
    session.run("pre-commit", "run")


@nox.session(python=PY_VERSIONS, name="pre-commit-update")
def run_pre_commit_autoupdate(session: nox.Session):
    session.install(f"pre-commit")

    log.info("Running pre-commit autoupdate")
    session.run("pre-commit", "autoupdate")


@nox.session(python=PY_VERSIONS, name="pre-commit-nbstripout")
def run_pre_commit_nbstripout(session: nox.Session):
    session.install(f"pre-commit")

    log.info("Running nbstripout pre-commit hook")
    session.run("pre-commit", "run", "nbstripout")


# @nox.session(python=[PY_VER_TUPLE], name="init-setup")
# def run_initial_setup(session: nox.Session):
#     log.info(f"Running initial setup.")
#     if INIT_COPY_FILES is None:
#         log.warning(f"INIT_COPY_FILES is empty. Skipping")
#         pass

#     else:

#         for pair_dict in INIT_COPY_FILES:
#             src = Path(pair_dict["src"])
#             dest = Path(pair_dict["dest"])
#             if not dest.exists():
#                 log.info(f"Copying {src} to {dest}")
#                 try:
#                     shutil.copy(src, dest)
#                 except Exception as exc:
#                     msg = Exception(
#                         f"Unhandled exception copying file from '{src}' to '{dest}'. Details: {exc}"
#                     )
#                     log.error(msg)

```
