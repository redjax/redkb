---
tags:
    - standard-project-files
    - python
    - sqlalchemy
    - database
---

# app/core/database

My standard SQLAlchemy base setup. The files in the `core/database` directory of my projects provides a database config from a `dataclass` (default values create a SQLite database at the project root), a SQLAlchemy `Base`, and methods for getting SQLAlchemy `Engine` and `Session`.

## __init__.py

```py title="database/__init__.py" linenums="1"

from __future__ import annotations

from .annotated import INT_PK, STR_10, STR_255
from .base import Base
from .db_config import DBSettings
from .methods import get_db_uri, get_engine, get_session_pool
from .mixins import TableNameMixin, TimestampMixin

```

## Annotations

Custom annotations live in `database/annotated`

### __init__.py

```py title="database/annotated/__init__.py" linenums="1"

from __future__ import annotations

from .annotated_columns import INT_PK, STR_10, STR_255

```

### annotated_columns.py

```py title="database/annotated/annotated_columns.py" linenums="1"

from __future__ import annotations

import sqlalchemy as sa
import sqlalchemy.orm as so
from typing_extensions import Annotated

## Annotated auto-incrementing integer primary key column
INT_PK = Annotated[
    int, so.mapped_column(sa.INTEGER, primary_key=True, autoincrement=True, unique=True)
]

## SQLAlchemy VARCHAR(10)
STR_10 = Annotated[str, so.mapped_column(sa.VARCHAR(10))]
## SQLAlchemy VARCHAR(255)
STR_255 = Annotated[str, so.mapped_column(sa.VARCHAR(255))]

```

## Mixins

Mixin classes can be used with classes that inherit from the SQLAlchemy `Base` class to add extra functionality.

!!!Example

    Automatically add a `created_at` and `updated_at` column by inheriting from `TimestampMixin`

```py title="SQLAlchemy mixed inheritance" linenums="1"
...

class ExampleModel(Base, TimestampMixin):
    """Class will have a created_at and modified_at timestamp applied automatically."""
    __tablename__ = "example"

    id: Mapped[int] = mapped_column(sa.INTEGER, primary_key=True, autoincrement=True, unique=True)

    ...
```

### __init__.py

```py title="database/mixins/__init__.py" linenums="1"

from __future__ import annotations

from .classes import TableNameMixin, TimestampMixin

```

### classes.py

```py title="daatabase/mixins/classes.py" linenums="1"

from __future__ import annotations

import pendulum
import sqlalchemy as sa
import sqlalchemy.orm as so

class TimestampMixin:
    """Add a created_at & updated_at column to records.

    Add to class declaration to automatically create these columns on
    records.

    Usage:

    ``` py linenums=1
    class Record(Base, TimestampMixin):
        __tablename__ = ...

        ...
    ```
    """

    created_at: so.Mapped[pendulum.DateTime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now()
    )
    updated_at: so.Mapped[pendulum.DateTime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()
    )


class TableNameMixin:
    """Mixing to automatically name tables based on class name.

    Generates a `__tablename__` for classes inheriting from this mixin.
    """

    @so.declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"

```

## base.py

```py title="database/base.py" linenums="1"

from __future__ import annotations

import sqlalchemy as sa
import sqlalchemy.orm as so

REGISTRY: so.registry = so.registry()
METADATA: sa.MetaData = sa.MetaData()


class Base(so.DeclarativeBase):
    registry = REGISTRY
    metadata = METADATA

```

## db_config.py

```py title="database/db_config.py" linenums="1"

from __future__ import annotations

import sqlalchemy as sa
import sqlalchemy.orm as so

from dataclasses import dataclass, field


@dataclass
class DBSettings:
    drivername: str = field(default="sqlite+pysqlite")
    user: str | None = field(default=None)
    password: str | None = field(default=None)
    host: str | None = field(default=None)
    port: str | None = field(default=None)
    database: str = field(default="app.sqlite")
    echo: bool = field(default=False)

    def __post_init__(self):
        assert self.drivername is not None, ValueError("drivername cannot be None")
        assert isinstance(self.drivername, str), TypeError(
            f"drivername must be of type str. Got type: ({type(self.drivername)})"
        )
        assert isinstance(self.echo, bool), TypeError(
            f"echo must be a bool. Got type: ({type(self.echo)})"
        )
        if self.user:
            assert isinstance(self.user, str), TypeError(
                f"user must be of type str. Got type: ({type(self.user)})"
            )
        if self.password:
            assert isinstance(self.password, str), TypeError(
                f"password must be of type str. Got type: ({type(self.password)})"
            )
        if self.host:
            assert isinstance(self.host, str), TypeError(
                f"host must be of type str. Got type: ({type(self.host)})"
            )
        if self.port:
            assert isinstance(self.port, int), TypeError(
                f"port must be of type int. Got type: ({type(self.port)})"
            )
            assert self.port > 0 and self.port <= 65535, ValueError(
                f"port must be an integer between 1 and 65535"
            )

    def get_db_uri(self) -> sa.URL:
        try:
            _uri: sa.URL = sa.URL.create(
                drivername=self.drivername,
                username=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            )

            return _uri

        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting SQLAlchemy database URL. Details: {exc}"
            )
            raise msg

    def get_engine(self) -> sa.Engine:
        assert self.get_db_uri() is not None, ValueError("db_uri is not None")
        assert isinstance(self.get_db_uri(), sa.URL), TypeError(
            f"db_uri must be of type sqlalchemy.URL. Got type: ({type(self.db_uri)})"
        )

        try:
            engine: sa.Engine = sa.create_engine(
                url=self.get_db_uri().render_as_string(hide_password=False),
                echo=self.echo,
            )

            return engine
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting database engine. Details: {exc}"
            )

            raise msg

    def get_session_pool(self) -> so.sessionmaker[so.Session]:
        engine: sa.Engine = self.get_engine()
        assert engine is not None, ValueError("engine cannot be None")
        assert isinstance(engine, sa.Engine), TypeError(
            f"engine must be of type sqlalchemy.Engine. Got type: ({type(engine)})"
        )

        session_pool: so.sessionmaker[so.Session] = so.sessionmaker(bind=engine)

        return session_pool
```

## methods.py

```py title="database/methods.py" linenums="1"
from __future__ import annotations

import sqlalchemy as sa
import sqlalchemy.orm as so

def get_db_uri(
    drivername: str = "sqlite+pysqlite",
    username: str | None = None,
    password: str | None = None,
    host: str | None = None,
    port: int | None = None,
    database: str = "demo.sqlite",
) -> sa.URL:
    assert drivername is not None, ValueError("drivername cannot be None")
    assert isinstance(drivername, str), TypeError(
        f"drivername must be of type str. Got type: ({type(drivername)})"
    )
    if username is not None:
        assert isinstance(username, str), TypeError(
            f"username must be of type str. Got type: ({type(username)})"
        )
    if password is not None:
        assert isinstance(password, str), TypeError(
            f"password must be of type str. Got type: ({type(password)})"
        )
    if host is not None:
        assert isinstance(host, str), TypeError(
            f"host must be of type str. Got type: ({type(host)})"
        )
    if port is not None:
        assert isinstance(port, int), TypeError(
            f"port must be of type int. Got type: ({type(port)})"
        )
    assert database is not None, ValueError("database cannot be None")
    assert isinstance(database, str), TypeError(
        f"database must be of type str. Got type: ({type(database)})"
    )

    try:
        db_uri: sa.URL = sa.URL.create(
            drivername=drivername,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )

        return db_uri
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception creating SQLAlchemy URL from inputs. Details: {exc}"
        )

        raise msg


def get_engine(db_uri: sa.URL = None, echo: bool = False) -> sa.Engine:
    assert db_uri is not None, ValueError("db_uri is not None")
    assert isinstance(db_uri, sa.URL), TypeError(
        f"db_uri must be of type sqlalchemy.URL. Got type: ({type(db_uri)})"
    )

    try:
        engine: sa.Engine = sa.create_engine(url=db_uri, echo=echo)

        return engine
    except Exception as exc:
        msg = Exception(f"Unhandled exception getting database engine. Details: {exc}")

        raise msg


def get_session_pool(engine: sa.Engine = None) -> so.sessionmaker[so.Session]:
    assert engine is not None, ValueError("engine cannot be None")
    assert isinstance(engine, sa.Engine), TypeError(
        f"engine must be of type sqlalchemy.Engine. Got type: ({type(engine)})"
    )

    session_pool: so.sessionmaker[so.Session] = so.sessionmaker(bind=engine)

    return session_pool

```
