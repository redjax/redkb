---
tags:
    - standard-project-files
    - python
    - nox
    - nox_extra
---

# Add a nox_extra module to your project

As you add more sessions to your `noxfile.py`, it can start to get difficult to navigate. You can break your code into modules for your `noxfile.py` by creating a directory in the root of your project (in the same path as your `noxfile.py`), and moving your code into scripts within that path.

!!! warning
    This guide assumes you're using the default `nox_extra/` path; if you choose to name this folder something else, make sure to update any code that references the old `nox_extra` module.

## Setup

- Create a `nox_extra/` directory
  - This is the module where you will add scripts to modularize your `noxfile.py`.
  - You can name this anything you want, but this guide assumes you stick with the default `nox_extra/`.
    If you use another name, make sure to update the code where it references the old "nox_extra" value, i.e. in `import` statements.
- Create the following files:
  - `nox_extra/__init__.py`: Denote the `nox_extra/` directory as a module.
    - You can leave this file empty. Anything you import in this file will be available from the top-level `nox_extra` module.
  - [`nox_extra/nox_utils.py`](#nox_utilspy)
    - Offload all common variables, functions, etc to a single file.
    - Script contents can be imported into the `noxfile.py` using `import nox_extra.<script_name> as <script_name>`.
    - Other modules in `nox_extra` can also import files and variables from this script. For example, the [`nox_django_sessions.py`](#nox_django_sessionspy) script imports variables like `DEFAULT_PYTHON` and the `cd()` context manager.
- Write your `noxfile.py`.
    - Reference the [Example noxfile.py](#example-noxfilepy) section below

## Usage

!!! note

    Check the [`nox_extra/nox_utils.py`](#nox_extranox_utilspy) and [`nox_extra/nox_django_sessions.py`](#nox_django_sessionspy) sections for more detailed information about each script in the `nox_extra` module. You can use these files as a reference to create your own custom `nox` scripts.


## Example noxfile.py

This `noxfile.py` imports from the `nox_extra` module. This saves some space at the top of the script doing things like configuring the default Python version.

```python title="noxfile.py" linenums="1"
from __future__ import annotations

from contextlib import contextmanager
import importlib.util
import logging
import logging.config
import os
import sys
from pathlib import Path
import platform
import secrets
import socket
import typing as t

log: logging.Logger = logging.getLogger("nox")

import nox

sys.path.append(os.path.abspath("nox_extra"))

## Set nox options
if importlib.util.find_spec("uv"):
    nox.options.default_venv_backend = "uv|virtualenv"
else:
    nox.options.default_venv_backend = "virtualenv"
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False
nox.options.error_on_missing_interpreters = False
# nox.options.report = True


try:
    ## Import extra nox modules from a "nox_extra/" directory.
    import nox_utils

    nox_utils.setup_nox_logging()

    log.info(
        "nox_extra module detected, enhancements from nox_extra.nox_utils are now available."
    )
except ImportError:
    log.error(f"Unable to import nox_utils.")

## Define versions to test
PY_VERSIONS: list[str] = nox_utils.PY_VERSIONS
## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE: tuple[str, str, str] = nox_utils.PY_VER_TUPLE
## Dynamically set Python version
DEFAULT_PYTHON: str = nox_utils.DEFAULT_PYTHON

DEFAULT_LINT_PATHS: list[str] = nox_utils.DEFAULT_LINT_PATHS
## Set directory for requirements.txt file output
REQUIREMENTS_OUTPUT_DIR: Path = nox_utils.REQUIREMENTS_OUTPUT_DIR

nox_utils.append_lint_paths(extra_paths=["nox_extra"], lint_paths=DEFAULT_LINT_PATHS)

```

## nox_extra/nox_utils.py

The `nox_utils.py` module contains variables, helper functions, & more that I commonly re-use in my projects. For example, a `DEFAULT_PYTHON` string variable that contains the version of Python used to launch `nox`. This becomes the default Python version to pass into `@nox.session(python=DEFAULT_PYTHON)` declarations.

### nox_utils.py

Copy and paste the contents below into `nox_extra/nox_utils.py`.

```python title="nox_extra/nox_utils.py" linenums="1"
"""Extra `nox` utilities.

Description:
    Add some `nox` helpers like a `DEFAULT_PY_VER` variable, which detects the version of Python used to call `nox` and
    can be the default Python version for custom sessions.
    
    Import in your `noxfile.py` with: `import nox_extra.nox_utils as nox_utils`.
    
    Get a list of sessions with `nox -s --list`.

Usage:
    In your `noxfile.py`, add a line `import nox_extra.nox_utils as nox_utils`. Now, variables & functions in this script are available in your
    main `noxfile.py`.
    
    For example, to add additional paths to the `DEFAULT_LINT_PATHS` variable in this file, you could call:
    

        ## noxfile.py

        import nox_extra.nox_utils as nox_utils

        ## Add the `nox_extra/` path to the list of paths to lint with ruff/black/etc.
        nox_utils.append_lint_paths(
            extra_paths=["nox_extra"], lint_paths=DEFAULT_LINT_PATHS
        )
 

    Now, any session that uses the `DEFAULT_LINT_PATHS` variable will also scan the `nox_extra/` path.

"""

from __future__ import annotations

from contextlib import contextmanager
import logging
import os
from pathlib import Path
import platform
import typing as t

import nox

## Define list of variables & functions to export from this app
__all__: list[str] = [
    "PY_VERSIONS",
    "PY_VER_TUPLE",
    "DEFAULT_PYTHON",
    "DEFAULT_LINT_PATHS",
    "REQUIREMENTS_OUTPUT_DIR",
    "DJANGO_PROJECT_DIR",
    "CONTAINER_ENV",
    "cd",
    "check_path_exists",
    "append_lint_paths",
    "detect_container_env",
    "setup_nox_logging",
]

log: logging.Logger = logging.getLogger(__name__)

## Define versions to test
PY_VERSIONS: list[str] = ["3.12", "3.11"]
## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE: tuple[str, str, str] = platform.python_version_tuple()
## Dynamically set Python version
DEFAULT_PYTHON: str = f"{PY_VER_TUPLE[0]}.{PY_VER_TUPLE[1]}"

## PDM version for sessions that use it
PDM_VER: str = "2.18.1"

## At minimum, these paths will be checked by your linters
#  Add new paths with nox_utils.append_lint_paths(extra_paths=["..."],)
DEFAULT_LINT_PATHS: list[str] = ["src", "tests"]
## Set directory for requirements.txt file output
REQUIREMENTS_OUTPUT_DIR: Path = Path("./requirements")


@contextmanager
def cd(newdir):
    """Context manager to change a directory before executing command."""
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


def check_path_exists(p: t.Union[str, Path] = None) -> bool:
    """Check the existence of a path.

    Params:
        p (str | Path): The path to the directory/file to check.

    Returns:
        (True): If Path defined in `p` exists.
        (False): If Path defined in `p` does not exist.

    """
    p: Path = Path(f"{p}")
    if "~" in f"{p}":
        p = p.expanduser()

    _exists: bool = p.exists()

    if not _exists:
        log.error(FileNotFoundError(f"Could not find path '{p}'."))

    return _exists


def append_lint_paths(
    extra_paths: str | list[str] = None, lint_paths: list[str] = DEFAULT_LINT_PATHS
) -> list[str]:
    """Adds more paths to the `DEFAULT_LINT_PATHS` variable.

    Description:
        Some `nox` sessions, like a `ruff` or `black` linter, require a path/directory input. Some defaults
        are provided in `DEFAULT_LINT_PATHS`, such as `src/` and `tests/`.

        If your project has scripts in additional directories, like `nox_extra`, or a `Django` app at the project's root path (where your `noxfile.py` should be),
        like `./django-app/manage.py`, you can add the `./django-app` directory to the `DEFAULT_LINT_PATHS` list using this function.

    Params:
        extra_paths (str | list[str]): A string or list of strings representing directories a session calling this function should iterate over.
            For example, a session that lints paths with `ruff` will scan over any additional paths in `extra_paths`.
        lint_paths (list[str]): A list of strings representing paths to iterate over. This is the "starting" list.
    """
    if lint_paths is None:
        lint_paths = []

    if extra_paths is None:
        return lint_paths

    if isinstance(extra_paths, str):
        extra_paths = [extra_paths]

    for pattern in extra_paths:
        for path in Path(".").rglob(pattern):
            relative_path = (
                Path(".").joinpath(path).resolve().relative_to(Path(".").resolve())
            )

            if f"{relative_path}" not in lint_paths:
                if relative_path.exists():
                    lint_paths.append(f"./{relative_path}")
                else:
                    log.warning(
                        f"Could not append path '{relative_path}' to list of lint paths. File/directory does not exist."
                    )
                    continue

    log.debug(f"Lint paths: {lint_paths}")
    return lint_paths


def detect_container_env(container_env_varname: str = "CONTAINER_ENV") -> bool:
    """Detect the presence of an env variable denoting a container environment.

    Params:
        container_env_varname (str): The name of the environment variable to search for.

    Returns:
        (True): If the environment variable is detected and it is set to `True`.
        (False): If the environment variable is not detected, or if it is detected and it is set to `False`.

    """
    ## Detect container env, or default to False
    if container_env_varname in os.environ:
        CONTAINER_ENV: bool = os.environ[container_env_varname]
    else:
        CONTAINER_ENV: bool = False

    return CONTAINER_ENV


CONTAINER_ENV: bool = detect_container_env()


def setup_nox_logging(
    nox_logger_name: str = "nox",
    level_name: str = "DEBUG",
    disable_loggers: list[str] | None = [],
) -> None:
    """Configure a stdlib logger for the Nox module.

    Description:
        This module hijacks the default `nox` logger

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
            str(nox_logger_name): {
                "level": level_name.upper(),
                "handlers": ["console"],
                "propagate": False,
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": f"{nox_logger_name}_fmt",
                "level": "DEBUG",
                "stream": "ext://sys.stdout",
            }
        },
        "formatters": {
            f"{nox_logger_name}_fmt": {
                "format": f"[{nox_logger_name.upper()}] "
                + "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
                "datefmt": "%Y-%m-%D %H:%M:%S",
            }
        },
    }

    ## Configure logging. Only run this once in an application
    logging.config.dictConfig(config=logging_config)

    if disable_loggers:
        ## Disable loggers by name. Sets logLevel to logging.WARNING to suppress all but warnings & errors
        for _logger in disable_loggers:
            logging.getLogger(_logger).setLevel(logging.WARNING)


@nox.session(python=[DEFAULT_PYTHON], name="ruff-lint", tags=["ruff", "clean", "lint"])
def run_linter(session: nox.Session, lint_paths: list[str] = DEFAULT_LINT_PATHS):
    """Nox session to run Ruff code linting."""
    if not check_path_exists(p="ruff.toml"):
        if not Path("pyproject.toml").exists():
            log.warning(
                """No ruff.toml file found. Make sure your pyproject.toml has a [tool.ruff] section!
                    
If your pyproject.toml does not have a [tool.ruff] section, ruff's defaults will be used.
Double check imports in __init__.py files, ruff removes unused imports by default.
"""
            )

    session.install("ruff")

    log.info("Linting code")
    for d in lint_paths:
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


@nox.session(
    python=[DEFAULT_PYTHON], name="black-lint", tags=["black", "clean", "lint"]
)
def run_linter(session: nox.Session, lint_paths: list[str] = DEFAULT_LINT_PATHS):
    """Nox session to run Ruff code linting."""
    session.install("black")

    log.info("Linting code")
    for d in lint_paths:
        if not Path(d).exists():
            log.warning(f"Skipping lint path '{d}', could not find path")
            pass
        else:
            lint_path: Path = Path(d)
            log.info(f"Linting path '{d}' with black")
            session.run(
                "black",
                lint_path,
            )

    log.info("Linting noxfile.py")
    session.run(
        "black",
        Path("./noxfile.py"),
    )


@nox.session(python=[DEFAULT_PYTHON], name="uv-export")
@nox.parametrize("requirements_output_dir", REQUIREMENTS_OUTPUT_DIR)
def export_requirements(session: nox.Session, requirements_output_dir: Path):
    ## Ensure REQUIREMENTS_OUTPUT_DIR path exists
    if not requirements_output_dir.exists():
        try:
            requirements_output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            msg = Exception(
                f"Unable to create requirements export directory: '{requirements_output_dir}'. Details: {exc}"
            )
            log.error(msg)

            requirements_output_dir: Path = Path("./")

    session.install(f"uv")

    log.info("Exporting production requirements")
    session.run(
        "uv",
        "pip",
        "compile",
        "pyproject.toml",
        "-o",
        str(REQUIREMENTS_OUTPUT_DIR / "requirements.txt"),
    )


@nox.session(python=[DEFAULT_PYTHON], name="pdm-export")
@nox.parametrize("pdm_ver", [PDM_VER])
@nox.parametrize("requirements_output_dir", REQUIREMENTS_OUTPUT_DIR)
def export_requirements(
    session: nox.Session, pdm_ver: str, requirements_output_dir: Path
):
    ## Ensure REQUIREMENTS_OUTPUT_DIR path exists
    if not requirements_output_dir.exists():
        try:
            requirements_output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            msg = Exception(
                f"Unable to create requirements export directory: '{requirements_output_dir}'. Details: {exc}"
            )
            log.error(msg)

            requirements_output_dir: Path = Path("./")

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

```
