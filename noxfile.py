from __future__ import annotations

from contextlib import contextmanager
import importlib.util
import logging
import os
from pathlib import Path
import platform
import shutil
import socket
import sys
import typing as t

log = logging.getLogger(__name__)

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

## Detect container env, or default to False
if "CONTAINER_ENV" in os.environ:
    CONTAINER_ENV: bool = os.environ["CONTAINER_ENV"]
else:
    CONTAINER_ENV: bool = False

## Define versions to test
PY_VERSIONS: list[str] = ["3.12", "3.11"]
## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE: tuple[str, str, str] = platform.python_version_tuple()
## Dynamically set Python version
DEFAULT_PYTHON: str = f"{PY_VER_TUPLE[0]}.{PY_VER_TUPLE[1]}"

# this VENV_DIR constant specifies the name of the dir that the `dev`
# session will create, containing the virtualenv;
# the `resolve()` makes it portable
VENV_DIR = Path("./.venv").resolve()

## At minimum, these paths will be checked by your linters
#  Add new paths with nox_utils.append_lint_paths(extra_paths=["..."],)
DEFAULT_LINT_PATHS: list[str] = [
    "src",
]
## Set directory for requirements.txt file output
REQUIREMENTS_OUTPUT_DIR: Path = Path("./")

## Configure logging
logging.basicConfig(
    level="DEBUG",
    format="%(name)s | [%(levelname)s] > %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

## Add logger names to the list to 'silence' them, reducing log noise from 3rd party packages
for _logger in []:
    logging.getLogger(_logger).setLevel("WARNING")


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


def install_uv_project(session: nox.Session, external: bool = False) -> None:
    """Method to install uv and the current project in a nox session."""
    log.info("Installing uv in session")
    session.install("uv")
    log.info("Syncing uv project")
    session.run("uv", "sync", external=external)
    log.info("Installing project")
    session.run("uv", "pip", "install", ".", external=external)


def _find_free_port(start_port=8000):
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

def run_docker_cmd(session: nox.Session, compose_file: str, operation: str):
    if compose_file is None:
        raise ValueError("Missing a compose_file value.")

    if operation is None:
        raise ValueError("operation should not be None")

    if not check_path_exists(p=compose_file):
        raise FileNotFoundError(f"Could not find compose file: {compose_file}")

    valid_operations: list[str] = [
        "build",
        "build-no-cache",
        "up",
        "up-build",
        "up-recreate",
        "down",
    ]

    match operation:
        case "build":
            session.run(
                "docker",
                "compose",
                "-f",
                compose_file,
                "build",
                external=True,
            )
        case "build-no-cache":
            session.run(
                "docker",
                "compose",
                "-f",
                compose_file,
                "build",
                "--no-cache",
                external=True,
            )
        case "up":
            session.run(
                "docker",
                "compose",
                "-f",
                compose_file,
                "up",
                "-d",
                external=True,
            )
        case "up-build":
            session.run(
                "docker",
                "compose",
                "-f",
                compose_file,
                "up",
                "-d",
                "--build",
                external=True,
            )
        case "up-recreate":
            session.run(
                "docker",
                "compose",
                "-f",
                compose_file,
                "up",
                "-d",
                "--force-recreate",
                external=True,
            )
        case "down" | "stop":
            session.run(
                "docker",
                "compose",
                "-f",
                compose_file,
                "down",
                external=True,
            )
        case _:
            raise ValueError(
                f"Invalid Docker compose operation: {operation}. Must be one of {valid_operations}"
            )


def run_podman_cmd(session: nox.Session, compose_file: str, operation: str):
    if compose_file is None:
        raise ValueError("Missing a compose_file value.")

    if operation is None:
        raise ValueError("operation should not be None")

    if not check_path_exists(p=compose_file):
        raise FileNotFoundError(f"Could not find compose file: {compose_file}")

    valid_operations: list[str] = [
        "build",
        "build-no-cache",
        "up",
        "up-build",
        "up-recreate",
        "down",
    ]

    match operation:
        case "build":
            session.run(
                "podman-compose",
                "-f",
                compose_file,
                "build",
                external=True,
            )
        case "build-no-cache":
            session.run(
                "podman-compose",
                "-f",
                compose_file,
                "build",
                "--no-cache",
                external=True,
            )
        case "up":
            session.run(
                "podman-compose",
                "-f",
                compose_file,
                "up",
                "-d",
                external=True,
            )
        case "up-build":
            session.run(
                "podman-compose",
                "-f",
                compose_file,
                "up",
                "-d",
                "--build",
                external=True,
            )
        case "up-recreate":
            session.run(
                "podman-compose", "-f", compose_file, "down", "&&",
                "podman-compose",
                "-f",
                compose_file,
                "up",
                "-d",
                "--force-recreate",
                external=True,
            )
        case "down" | "stop":
            session.run(
                "podman-compose",
                "-f",
                compose_file,
                "down",
                external=True,
            )
        case _:
            raise ValueError(
                f"Invalid podman-compose operation: {operation}. Must be one of {valid_operations}"
            )


#######################
# Repository Sessions #
#######################


@nox.session(python=[DEFAULT_PYTHON], name="dev-env")
def dev(session: nox.Session) -> None:
    """Sets up a python development environment for the project.

    Run this on a fresh clone of the repository to automate building the project with uv.
    """
    install_uv_project(session, external=True)
    
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
    
@nox.session(name="vulture-check", tags=["coverage", "quality"])
def vulture_check(session: nox.Session):
    install_uv_project(session)

    log.info("Installing vulture for dead code checking")
    session.install("vulture")

    log.info("Running vulture")
    session.run("vulture")
    
##############
# Pre-commit #
##############

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

##########
# MKDocs #
##########

@nox.session(python=[DEFAULT_PYTHON], name="publish-mkdocs", tags=["mkdocs", "publish"])
def publish_mkdocs(session: nox.Session):
    install_uv_project(session)

    log.info("Publishing MKDocs site to Github Pages")

    session.run("mkdocs", "gh-deploy")
    
@nox.session(python=[DEFAULT_PYTHON], name="serve-mkdocs-check-links", tags=["mkdocs", "lint"])
def check_mkdocs_links(session: nox.Session):
    install_uv_project(session)
    
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
    install_uv_project(session)
    
    free_port = _find_free_port(start_port=8000)
    
    log.info(f"Serving MKDocs site on port {free_port}")
    
    try:
        session.run("mkdocs", "serve", "--dev-addr", f"0.0.0.0:{free_port}")
    except Exception as exc:
        msg = f"({type(exc)}) Unhandled exception serving MKDocs site. Details: {exc}"
        log.error(msg)


################
# Cookiecutter #
################

@nox.session(python=DEFAULT_PYTHON, name="new-docker-template-page", tags=["mkdocs", "cookiecutter", "template"])
def new_docker_template_page(session: nox.Session):
    from cookiecutter.main import cookiecutter
    
    session.install("cookiecutter")
    
    log.info("Answer the prompts to create a new page in docs/programming/docker/my_containers")
    
    COOKIECUTTER_TEMPLATE_FILE: Path = Path("./templates/docs/containers/docker_template_page")
    DOCKER_CONTAINER_DOCS_ROOT: Path = Path("./docs/template/docker")
    
    if not COOKIECUTTER_TEMPLATE_FILE.exists():
        log.warning(f"Could not find cookiecutter template at path '{COOKIECUTTER_TEMPLATE_FILE}'.")
    
    while True:
        docs_section_choice = input("Which section directory will the template be exported to (i.e. automation, databases): ")
        
        if docs_section_choice is None or docs_section_choice == "":
            log.warning("You must type a directory name that exists in ./docs/programming/docker/my_containers")
            
        CONTAINER_SECTION = DOCKER_CONTAINER_DOCS_ROOT / docs_section_choice
        
        if not CONTAINER_SECTION.exists():
            # mkdir_choice = input(f"[WARNING] Container directory section '{CONTAINER_SECTION}' does not exist. Create directory now? (Y/N): ")
            log.warning(f"Could not find section '{CONTAINER_SECTION}'. Creating path '{CONTAINER_SECTION}'")
            try:
                CONTAINER_SECTION.mkdir(parents=True, exist_ok=True)
            except Exception as exc:
                msg = f"({type(exc)}) Error creating section '{CONTAINER_SECTION}'. Details: {exc}"
                log.error(msg)
                
                raise exc
            
        break
    
    log.info(f"Rendering template [{COOKIECUTTER_TEMPLATE_FILE}] to [{CONTAINER_SECTION}]")
    
    try:
        cookiecutter(template=str(COOKIECUTTER_TEMPLATE_FILE), output_dir=str(CONTAINER_SECTION), no_input=False)
    except Exception as exc:
        msg = f"({type(exc)}) Error rendering template. Details: {exc}"
        log.error(msg)
