from __future__ import annotations

import logging
import logging.config
import logging.handlers
import os
from pathlib import Path
import platform
import shutil
import socket

import nox

## Create logger for this module
log: logging.Logger = logging.getLogger("nox")

## Detect container env, or default to False
if "CONTAINER_ENV" in os.environ:
    CONTAINER_ENV: bool = os.environ["CONTAINER_ENV"]
else:
    CONTAINER_ENV: bool = False

## Set nox options
nox.options.default_venv_backend = "uv|virtualenv"
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False
nox.options.error_on_missing_interpreters = False
# nox.options.report = True

## Define sessions to run when no session is specified
nox.sessions = ["lint", "export", "tests"]

## Define versions to test
PY_VERSIONS: list[str] = ["3.12", "3.11"]
## Set PDM version to install throughout
PDM_VER: str = "2.18.1"

## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE = platform.python_version_tuple()
## Dynamically set Python version
DEFAULT_PYTHON: str = f"{PY_VER_TUPLE[0]}.{PY_VER_TUPLE[1]}"

## Set paths to lint with the lint session
LINT_PATHS: list[str] = ["src", "tests"]

## Set directory for requirements.txt file output
REQUIREMENTS_OUTPUT_DIR: Path = Path("./requirements")

## Set file src/dest pairs for copying in init-setup session.
#  Leave empty to skip.
#  Example: {"src": "config/settings.toml", "dest": "config/settings.local.toml"}
INIT_COPY_FILES: list[dict[str, str]] = []


def _find_free_port(start_port=8000):
    """Find a free port starting from a specific port number"""
    port = start_port
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("0.0.0.0", port))
                return port
            except socket.error:
                log.info(f"Port {port} is in use, trying the next port.")
                port += 1


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

log.info(f"[container_env:{CONTAINER_ENV}]")

## Ensure REQUIREMENTS_OUTPUT_DIR path exists
if not REQUIREMENTS_OUTPUT_DIR.exists():
    try:
        REQUIREMENTS_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        msg = Exception(
            f"Unable to create requirements export directory: '{REQUIREMENTS_OUTPUT_DIR}'. Details: {exc}"
        )
        print(msg)

        REQUIREMENTS_OUTPUT_DIR: Path = Path(".")


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

    # log.info("Formatting code with black")
    # session.run("black", "noxfile.py")

    log.info("Linting noxfile.py with ruff")
    session.run(
        "ruff",
        "check",
        "./noxfile.py",
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


@nox.session(python=PY_VERSIONS, name="pre-commit-all")
def run_pre_commit_all(session: nox.Session):
    session.install("pre-commit")
    session.run("pre-commit")

    log.info("Running all pre-commit hooks")
    session.run("pre-commit", "run")


@nox.session(python=PY_VERSIONS, name="pre-commit-update")
def run_pre_commit_autoupdate(session: nox.Session):
    session.install("pre-commit")

    log.info("Running pre-commit autoupdate")
    session.run("pre-commit", "autoupdate")


@nox.session(python=PY_VERSIONS, name="pre-commit-nbstripout")
def run_pre_commit_nbstripout(session: nox.Session):
    session.install("pre-commit")

    log.info("Running nbstripout pre-commit hook")
    session.run("pre-commit", "run", "nbstripout")


@nox.session(python=[DEFAULT_PYTHON], name="prune-local-branches", tags=["git"])
def clean_branches(session: nox.Session):
    log.info("Cleaning local branches that have been deleted from the remote.")
    PROTECTED_BRANCHES: list[str] = ["main", "master", "dev", "rc", "gh-pages"]

    options = session.posargs or session.default_args
    force = "force" in options

    ## Install GitPython
    session.install("gitpython")

    ## Import gitpython
    import git

    ## Initialize repository
    repo = git.Repo(".")

    ## Fetch latest changes & prune deleted branches
    repo.git.fetch("--prune")

    ## Get a list of local branches
    local_branches: list[str] = [head.name for head in repo.heads]
    log.info(f"Found [{len(local_branches)}] local branch(es).")
    if len(local_branches) < 15:
        log.debug(f"Local branches: {local_branches}")

    ## Get a list of remote branches
    remote_branches: list[str] = [
        ref.name.replace("origin/", "") for ref in repo.remotes.origin.refs
    ]
    log.info(f"Found [{len(remote_branches)}] remote branch(es).")
    if len(remote_branches) < 15:
        log.debug(f"Remote branches: {remote_branches}")

    ## Find local branches that are not present in remote branches
    branches_to_delete: list[str] = [
        branch for branch in local_branches if branch not in remote_branches
    ]
    log.info(f"Prepared [{len(branches_to_delete)}] branch(es) for deletion.")
    if len(branches_to_delete) < 15:
        log.debug(f"Deleting branches: {branches_to_delete}")

    for branch in branches_to_delete:
        if branch not in PROTECTED_BRANCHES:  ## Avoid deleting specified branches
            try:
                repo.git.branch("-d", branch)
                log.info(f"Deleted branch '{branch}'")
            except git.GitError as git_err:
                msg = Exception(
                    f"Git error while deleting branch '{branch}'. Details: {git_err}"
                )

                if force:
                    log.warning("Force=True, attempting to delete with -D")
                    try:
                        repo.git.branch("-D", branch)
                        log.info(f"Force-deleted branch '{branch}'")
                    except git.GitError as git_err2:
                        msg2 = Exception(
                            f"Git error while force deleting branch '{branch}'. Details: {git_err2}"
                        )
                        log.warning(
                            f"Branch '{branch}' was not deleted. Reason: {msg2}"
                        )

                        ## Retry with subprocess
                        try:
                            log.info("Retrying using subprocess.")
                            session.run(["git", "branch", "-D", branch], external=True)
                            log.info(
                                f"Force-deleted branch '{branch}'. Required fallback to subprocess."
                            )
                        except git.GitError as git_err3:
                            msg3 = Exception(
                                f"Git error while force deleting branch '{branch}'. Details: {git_err3}"
                            )
                            log.warning(
                                f"Branch '{branch}' was not deleted. Reason: {msg3}"
                            )
                        except Exception as exc:
                            msg = Exception(
                                f"Unhandled exception attempting to delete git branch '{branch}' using subprocess.run(). Details: {exc}"
                            )
                            log.error(msg)

                else:
                    log.warning(f"Branch '{branch}' was not deleted. Reason: {msg}")

                continue


@nox.session(python=[DEFAULT_PYTHON], name="publish-mkdocs", tags=["mkdocs", "publish"])
def publish_mkdocs(session: nox.Session):
    session.install("-r", f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt")

    log.info("Publishing MKDocs site")

    session.run("mkdocs", "gh-deploy")
    
@nox.session(python=[DEFAULT_PYTHON], name="serve-mkdocs-check-links", tags=["mkdocs", "lint"])
def check_mkdocs_links(session: nox.Session):
    session.install("-r", f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt")
    
    free_port = _find_free_port(start_port=8000)
    
    log.info(f"Serving MKDocs site with link checking enabled on port {free_port}")
    try:
        os.environ["ENABLED_HTMLPROOFER"] = "true"
        session.run("mkdocs", "serve", "--dev-addr", f"0.0.0.0:{free_port}")
    except Exception as exc:
        msg = f"({type(exc)}) Unhandled exception checking mkdocs site links. Details: {exc}"
        log.error(msg)
        
        raise exc


@nox.session(python=DEFAULT_PYTHON, name="serve-mkdocs", tags=["mkdocs", "serve"])
def serve_mkdocs(session: nox.Session):
    session.install("-r", f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt")
    
    free_port = _find_free_port(start_port=8000)
    
    log.info(f"Serving MKDocs site on port {free_port}")
    
    try:
        session.run("mkdocs", "serve", "--dev-addr", f"0.0.0.0:{free_port}")
    except Exception as exc:
        msg = f"({type(exc)}) Unhandled exception serving MKDocs site. Details: {exc}"
        log.error(msg)


@nox.session(python=[PY_VER_TUPLE], name="init-setup")
def run_initial_setup(session: nox.Session):
    log.info("Running initial setup.")
    if INIT_COPY_FILES is None:
        log.warning("INIT_COPY_FILES is empty. Skipping")
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
