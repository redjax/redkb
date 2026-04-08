---
tags:
    - python
    - sqlalchemy
---

# SQLAlchemy dependency methods

Dependencies for your database code. These can be context manager classes/functions, initialized objects, and other things to assist you interacting with the database.

```python title="_depends.py" linenums="1"
"""Dependencies for database.

Includes functions like `get_db()`, which is a context manager that yields a database session.
"""

from __future__ import annotations

import logging

from contextlib import contextmanager
import typing as t

log = logging.getLogger(__name__)

from .db_config import DBSettings

import sqlalchemy as sa
import sqlalchemy.orm as so


def get_db_uri(
    drivername: str = None,
    username: str = None,
    password: str = None,
    host: str = None,
    port: t.Union[int, str] = None,
    database: str = None,
) -> sa.URL:
    """Construct a SQLAlchemy `URL` from params.

    Returns:
        (sqlalchemy.URL): An initialized database connection URL.

    """
    try:
        _uri: sa.URL = sa.URL.create(
            drivername=drivername,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )

        return _uri

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception getting SQLAlchemy database URL. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_engine(db_uri: sa.URL = None, echo: bool = False) -> sa.Engine:
    """Build & return a SQLAlchemy `Engine`.

    Returns:
        `sqlalchemy.Engine`: A SQLAlchemy `Engine` instance.

    """
    if db_uri is None:
        raise ValueError("db_uri is not None")
    if not isinstance(db_uri, sa.URL):
        raise TypeError(
            f"db_uri must be of type sqlalchemy.URL. Got type: ({type(db_uri)})"
        )

    try:
        engine: sa.Engine = sa.create_engine(
            url=db_uri.render_as_string(hide_password=False),
            echo=echo,
        )

        return engine
    except Exception as exc:
        msg = Exception(f"Unhandled exception getting database engine. Details: {exc}")
        log.error(msg)

        raise exc


def get_session_pool(
    engine: sa.Engine = None, autoflush: bool = False, expire_on_commit: bool = False
) -> so.sessionmaker[so.Session]:
    """Configure a session pool using class's SQLAlchemy `Engine`.

    Returns:
        (sqlalchemy.orm.sessionmaker): A SQLAlchemy `Session` pool for database connections.

    """
    if engine is None:
        raise ValueError("engine cannot be None")
    if not isinstance(engine, sa.Engine):
        raise TypeError(
            f"engine must be of type sqlalchemy.Engine. Got type: ({type(engine)})"
        )

    session_pool: so.sessionmaker[so.Session] = so.sessionmaker(
        bind=engine, autoflush=autoflush, expire_on_commit=expire_on_commit
    )

    return session_pool


@contextmanager
def get_db(
    db_uri: t.Union[sa.URL, str] = None,
    echo: bool = False,
    autoflush: bool = False,
    expire_on_commit: bool = False,
) -> t.Generator[so.Session, t.Any, None]:
    """Dependency to yield a SQLAlchemy Session pool.

    Usage:

    from core.dependencies import get_db

    with get_db() as session:
        repo = someRepoClass(session)

        all = repo.get_all()

    """
    if db_uri is None:
        raise ValueError("Missing a SQLAlchemy URL object.")
    if not isinstance(db_uri, sa.URL):
        raise TypeError(
            f"Invalid type for db_uri: ({type(db_uri)}). Must be a SQLAlchemy URL object."
        )

    engine = get_engine(db_uri=db_uri, echo=echo)

    SESSION_POOL: so.sessionmaker[so.Session] = get_session_pool(
        engine=engine, autoflush=autoflush, expire_on_commit=expire_on_commit
    )

    db: so.Session = SESSION_POOL()

    try:
        yield db
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception yielding database session. Details: {exc}"
        )

        raise msg
    finally:
        db.close()

```
