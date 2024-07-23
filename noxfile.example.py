from __future__ import annotations

import logging
import logging.config
import logging.handlers
import os
from pathlib import Path
import platform
import shutil
import typing as t

import nox

## Set nox options
nox.options.default_venv_backend = "uv|virtualenv"
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

## Create logger for this module
log: logging.Logger = logging.getLogger("nox")

log.info(f"[container_env:{CONTAINER_ENV}]")

## Define versions to test
PY_VERSIONS: list[str] = ["3.12", "3.11"]
## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE: tuple[str, str, str] = platform.python_version_tuple()
## Dynamically set Python version
DEFAULT_PYTHON: str = f"{PY_VER_TUPLE[0]}.{PY_VER_TUPLE[1]}"

## Set PDM version to install throughout
PDM_VER: str = "2.15.4"
## Set paths to lint with the lint session
LINT_PATHS: list[str] = ["./src", "./tests", "./noxfile.py"]
## Use search patterns to add more files to list of paths to lint.
LINT_PATHS:list[str] = append_lint_paths(search_patterns="*.ipynb", lint_paths=LINT_PATHS)

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

## Set file src/dest pairs for copying in init-setup session.
#  Leave empty to skip.
#  Example: {"src": "config/settings.toml", "dest": "config/settings.local.toml"}
INIT_COPY_FILES: list[dict[str, str]] = []


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
                "check",
                lint_path,
                "--select",
                "I",
                "--fix",
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


@nox.session(python=[PY_VER_TUPLE], name="init-setup")
def run_initial_setup(session: nox.Session):
    log.info(f"Running initial setup.")
    if INIT_COPY_FILES is None or isinstance(INIT_COPY_FILES, list) and len(INIT_COPY_FILES) == 0:
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

@nox.session(
    python=[DEFAULT_PYTHON], name="nb-strip", tags=["jupyter", "cleanup"]
)
def clear_notebook_output(session: nox.Session):
    session.install("nbstripout")

    log.info("Gathering all Jupyter .ipynb files")
    ## Find all Jupyter notebooks in the project
    notebooks: t.Generator[Path, None, None] = Path(".").rglob("*.ipynb")

    ## Clear the output of each notebook
    for notebook in notebooks:
        log.info(f"Stripping output from notebook '{notebook}'")
        session.run("nbstripout", str(notebook))