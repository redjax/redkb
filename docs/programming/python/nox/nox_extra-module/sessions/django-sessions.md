---
tags:
    - standard-project-files
    - python
    - nox
    - django
---

# Django

## nox_extra/nox_django_sessions.py

Helpers & `nox` sessions for `Django` projects. Expects the existence of a [`nox_extra/nox_utils.py`](#nox_extranox_utilspy) file to exist, this script imports some values from the common utils file.

### nox_django_sessions.py

Copy and paste the contents below into `nox_extra/nox_django_sessions.py`.

```python title="nox_extra/nox_django_sessions.py" linenums="1"
"""Django `nox` sessions.

Description:
    Helpers and defaults for Django `nox` sessions. Includes sessions like generate-django-secret, which
    creates a secure string that can be used for your Django apps' `SECRET_KEY`.
    

"""

from __future__ import annotations

from contextlib import contextmanager
import logging
import os
import platform
import secrets
import socket
from pathlib import Path

log: logging.Logger = logging.getLogger(__name__)

import nox_extra.nox_utils as nox_utils

import nox

__all__: list[str] = [
    "_find_free_port",
    "_django_makemigrations",
    "_django_migrate",
    "generate_secure_secret",
    "generate_django_secret",
    "run_django_devserver",
    "django_make_migrations",
    "django_migrate",
    "django_do_migrations",
]

## Path to output requirements.txt file(s)
REQUIREMENTS_OUTPUT_DIR: Path = nox_utils.REQUIREMENTS_OUTPUT_DIR

## Define versions to test
PY_VERSIONS: list[str] = nox_utils.PY_VERSIONS
## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE: tuple[str, str, str] = nox_utils.PY_VER_TUPLE
## Dynamically set Python version
DEFAULT_PYTHON: str = nox_utils.DEFAULT_PYTHON

## UPDATE THIS VALUE FOR EACH NEW DJANGO PROJECT
DJANGO_PROJECT_DIR = "./weatherdaily/"


def _find_free_port(host_addr: str = "0.0.0.0", start_port=8000) -> int:
    """Find a free port starting from a specific port number.

    Params:
        host_addr (str): The host address to bind to. Default is '0.0.0.0', which can be dangerous.
        start_port (int): Attempt to bind to this port, and increment 1 each time port binding fails.

    Returns:
        (int): An open port number, i.e. 8000 if 8001 is in use.
    """

    port: int = start_port

    ## Loop open port check until one is bound
    while True:
        ## Create a socked
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                ## Try binding port to host address
                sock.bind((host_addr, port))
                return port

            except socket.error:
                ## Port in use, increment & retry
                log.info(f"Port {port} is in use, trying the next port.")
                port += 1


def _django_makemigrations(session: nox.Session) -> None:
    """Run Django's manage.py makemigrations.

    Description:
        Creates migrations for all Django apps in your project. Use with caution,
        this will create migrations for all models.

    """

    ## Set script path to path with Django's manage.py
    with nox_utils.cd(newdir=DJANGO_PROJECT_DIR):
        try:
            session.run("python", "manage.py", "makemigrations")
        except Exception as exc:
            msg = f"({type(exc)}) Unhandled exception running manage.py makemigrations. Details: {exc}"
            log.error(msg)

            raise exc


def _django_migrate(session: nox.Session) -> None:
    """Do all database migrations.

    Description:
        Performs migrations for all Django apps in your project. Use with caution,
        this will migrate models for all apps.
    """
    ## Set script path to path with Django's manage.py
    with nox_utils.cd(newdir=DJANGO_PROJECT_DIR):
        try:
            session.run("python", "manage.py", "migrate")
        except Exception as exc:
            msg = f"({type(exc)}) Unhandled exception running manage.py migrate. Details: {exc}"
            log.error(msg)

            raise exc


def generate_secure_secret(
    random_char_seed: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
    print_secret: bool = False,
) -> str:
    """Generate a secure string.

    Description:
        Combines the functionality of some code lovingly lifted from
        django.core.management.utils.get_random_secret_key(). In their words,
        "return a securely generated random string."

        This can be used to generate secrets, like Django's `SECRET_KEY` setting.

    """

    def get_random_string(length, allowed_chars=random_char_seed):
        """Return a securely generated random string.

        The bit length of the returned value can be calculated with the formula:
            log_2(len(allowed_chars)^length)

        For example, with default `allowed_chars` (26+26+10), this gives:
        * length: 12, bit length =~ 71 bits
        * length: 22, bit length =~ 131 bits
        """
        return "".join(secrets.choice(allowed_chars) for i in range(length))

    ## Generate a secret
    _secret: str = get_random_string(50, random_char_seed)

    if print_secret:
        ## Print (instead of log, which could leak), the secret.
        print(f"Generated secure string:\n\n{_secret}\n")

    return _secret


@nox.session(
    python=DEFAULT_PYTHON, name="generate-django-secret", tags=["django", "init"]
)
def generate_django_secret(session: nox.Session) -> None:
    """Securely generate a Django secret key.

    Description:
        Calls the generate_secure_secret() function, which returns an encrypted key made from randomized input.
        Optionally prints the secret. This uses the print() function, instead of a logger, to prevent secrets from
        leaking.
    """

    ## Generate & print a Django secret
    generate_secure_secret(print_secret=True)


@nox.session(python=DEFAULT_PYTHON, name="run-django-devserver", tags=["django"])
def run_django_devserver(session: nox.Session) -> None:
    """Call Django's manage.py runserver with args.

    Description:
        Uses the _find_free_port() function to test binding ports to a socket,
        returning an open/available port if the desired port is in use.

        Uses the cd() context manager to set the script's path to the Django project
        path for the duration of the script; while inside the Django project directory,
        calls python manage.py runserver 0.0.0.0:$free_port.
    """
    session.install("-r", f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt")

    ## Find an open port
    free_port: int = _find_free_port(start_port=8000)

    log.info(f"Running local Django development server on port {free_port}")
    ## Temporarily set script path to Django's project path
    with nox_utils.cd(newdir=DJANGO_PROJECT_DIR):
        try:
            session.run("python", "manage.py", "runserver", f"0.0.0.0:{free_port}")
        except Exception as exc:
            msg = f"({type(exc)}) Unhandled exception running Django development server. Details: {exc}"
            log.error(msg)

            raise exc


@nox.session(python=DEFAULT_PYTHON, name="django-makemigrations", tags=["django", "db"])
def django_make_migrations(session: nox.Session) -> None:
    """Run Django's manage.py makemigrations on all app models.

    Description:
        Creates migrations for all Django apps in your project. Use with caution,
        this will create migrations for all models.

    """
    session.install("-r", f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt")

    log.info("Running manage.py makemigrations")

    try:
        _django_makemigrations(session=session)
    except Exception as exc:
        msg = f"({type(exc)}) Error running manage.py makemigrations. Details: {exc}"
        log.error(msg)


@nox.session(python=DEFAULT_PYTHON, name="django-migrate", tags=["django", "db"])
def django_migrate(session: nox.Session) -> None:
    """Run Django's manage.py migrate for all app models.

    Description:
        Performs migrations for all Django apps in your project. Use with caution,
        this will migrate models for all apps.
    """
    session.install("-r", f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt")

    log.info("Running manage.py migrate")

    _django_migrate(session=session)


@nox.session(
    python=DEFAULT_PYTHON,
    name="django-migrate-all",
    tags=["django", "db", "migrations"],
)
def django_do_migrations(session: nox.Session) -> None:
    """Create & perform Django database migrations.

    Description:
        Calls Django's manage.py makemigrations to create migration files for
        all app models, then do the migrations with manage.py migrate. Use with
        caution, combining both of these steps can cause problems if there are
        errors in your migrations.
    """
    session.install("-r", f"{REQUIREMENTS_OUTPUT_DIR}/requirements.txt")

    log.info("Running manage.py makemigrations and manage.py migrate")

    ## Determine whether migrations should be performed.
    #  Only flips to True if makemigrations is successful
    DO_MIGRATION: bool = False

    try:
        _django_makemigrations(session=session)
        ## Enable migration if makemigrations is successful
        DO_MIGRATION = True
    except Exception as exc:
        msg: str = f"({type(exc)}) Error create database migrations. Details: {exc}"
        log.error(msg)

        DO_MIGRATION = False

    if DO_MIGRATION:
        log.info("Doing all Django database migrations.")
        _django_migrate(session=session)
    else:
        log.warning("Error during makemigrations. Skipping manage.py migrate.")

```
