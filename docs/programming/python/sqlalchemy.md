---
tags:
    - python
    - sqlalchemy
---


# SQLAlchemy

!!! INTRODUCTION

    These docs written for `sqlalchemy == 2.0`

    - 🏠 [SQLAlchemy Home](https://www.sqlalchemy.org)
    - 📖 [SQLAlchemy Docs Index](https://docs.sqlalchemy.org/en/20/#)
        - 📄 [SQLAlchemy ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
            - Learn the new 2.0 syntax with a guided tutorial/quickstart.
        - 📄 [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
            - The 2.0 release of SQLAlchemy introduced a new ORM syntax. It is different enough from versions prior to 2.0 that a tutorial demonstrating the "old" and "new" ways of doing things was needed.
            - The newer 2.0 syntax is simpler and more Pythonic, and feels more flexible (subjective opinions).

## Repositories

A database repository standardizes operations for a given entity. The repository is a class that contains methods like `.add()`, `.remove()`, `.get(id: int)`, etc. Each repository is meant to control a single SQLAlchemy table class (a model class that inherits from SQLAlchemy's `Base` object).

For example, if you have a class `User(Base)` and `Comment(Base)`, you would create 2 repositories, `UserRepository` and `CommentRepository`. Each repository class would have its own `.add()`, `.remove()`, `.get()`, etc.

!!! note

    **Example app using repository class**

    To see an example of one of my apps that uses this pattern, check [`auto-xkcd`](https://github.com/redjax/auto-xkcd/tree/main/src/auto_xkcd).
    
    - [`auto_xkcd.domain.xkcd.comic`](https://github.com/redjax/auto-xkcd/tree/main/src/auto_xkcd/domain/xkcd/comic) for models, schemas, and repositories.
    - [`auto_xkcd.core.database`](https://github.com/redjax/auto-xkcd/tree/main/src/auto_xkcd/core/database) for SQLAlchemy code.
    - To see the repository in action, check the `save_comic_to_db()` method in the [`auto_xkcd.modules.xkcd_modd.methods`](https://github.com/redjax/auto-xkcd/blob/main/src/auto_xkcd/modules/xkcd_mod/methods.py) module.

### Inheriting from a RepositoryBase class

You can define an abstract base class (`abc.ABCMeta`) repository, which your other repository classes can inherit from. On the base class, you can define attributes and methods that must be defined on the child class. This is helpful for requiring methods like `.add()`, `.remove()`, etc on all child classes.

```python title="Example RepositoryBase class" linenums="1"
import abc
import typing as t

T = t.TypeVar("T")

class RepositoryBase(t.Generic[T], metaclass=abc.ABCMeta):
	"""A generic SQLAlchemy repository class base."""

	@abc.abstractmethod
	def add(self, entity: T):
		"""Add new entity to database."""
		raise NotImplementedError()

	@abc.abstractmethod
	def remove(self, entity: T):
		"""Remove existing entity from database."""
		raise NotImplementedError()

	@abc.abstractmethod
	def get_by_id(self, entity_id) -> T:
		"""Retrieve entity from database by its ID."""
		raise NotImplementedError()

```

You can use thie `RepositoryBase` class to create child repeositories, for example `UserRepository`:

```python title="Example UserRepository class" linenums="1"
class UserRepository(RepositoryBase):
    ## Required by RepositoryBase
    def add(self, entity: UserModel):
        ...
    
    ## Required by RepositoryBase
    def remove(self, entity: UserModel):
        ...

    ## Required by RepositoryBase
    def get_by_id(self, entity_id: int) -> UserModel:
        ...

    ## Not required by RepositoryBase, and only available to UserRepository instances, or children fo this class
    def count(self) -> int:
        ...

```

## Sample Code

Below are sections with example code demonstrating various SQLAlchemy functionality. Some of this code is meant to be copy/pasted into a `database` module.

!!! note

    Check my [`red-utils` package's `.ext.sqlalchemy_utils`](https://github.com/redjax/red-utils/tree/main/src/red_utils/ext/sqlalchemy_utils) module for an example `database` module. You can essentially copy/paste the code into a directory in your project like `src/app/database/`.

### SQLAlchemy Base

```python title="Declare SQLAlchemy Base" linenums="1"
"""SQLAlchemy `DeclarativeBase`, `MetaData`, and `registry` objects.

Import this `Base` into SQLAlchemy model files and let classes inherit from
the `DeclarativeBase` declared here.

The `registry()` function sets the global SQLAlchemy `registry` for the `DeclarativeBase` object.

!!! note

    Docs for `DeclarativeBase` and `registry()`

    - [Using a DelcarativeBase base class](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#using-a-declarative-base-class)

    Docs for MetaData object

    - [Unified tutorial](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-working-with-metadata)
    - [MetaData Docs](https://docs.sqlalchemy.org/en/20/core/metadata.html)
    - [Impose a table naming scheme with MetaData object](https://docs.sqlalchemy.org/en/20/core/metadata.html#specifying-a-default-schema-name-with-metadata)

"""

from __future__ import annotations

import sqlalchemy as sa
import sqlalchemy.orm as so

## Global SQLAlchemy MetaData object
metadata: sa.MetaData = sa.MetaData()

## Registry object stores mappings & config hooks
reg = so.registry()


## SQLAlchemy DeclarativeBase is the parent class object table classes will inherit from
class Base(so.DeclarativeBase):
    """Default/Base class for SQLAlchemy models.

    Description:

    Child classes inheriting from this Base object will be treated as SQLAlchemy
    models. Set child class tables with `__tablename__ = ....`

    Global defaults can be set on this object (i.e. a SQLAlchemy registry), and will
    be inherited/accessible by all child classes.

    !!! note

        When this class is instantiated, it will not be of type sqlalchemy.orm.DeclarativeBase;
            Because of the way this class is intialized, its type will be
            sqlalchemy.orm.decl_api.DeclarativeAttributeIntercept

    Params:
        registry (sqlalchemy.Registry): A `registry` object for the `Base` class
        metadata (sqlalchemy.MetaData): A `MetaData` object, with data about the `Base` class
    """

    registry: so.registry = reg
    metadata: sa.MetaData = metadata

```

### DBConfig settings class

```python title="DBConfig settings" linenums="1"
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
import typing as t

import sqlalchemy as sa
import sqlalchemy.orm as so


@dataclass
class DBSettings:
    """Store configuration for a database.

    Params:
        drivername (str): The `sqlalchemy` driver name, i.e. `'sqlite+pysqlite'`.
        username (str|None): The database user's username.
        password (str|None): The database user's password.
        host (str|None): The database host address.
        port (str|int|None): The database host's port.
        database (str): The name of the database to connect to. For SQLite, use the path to the file,
            i.e. `db/app.sqlite`.
        echo (bool): If `True`, the SQLAlchemy `Engine` will echo SQL queries to the CLI, and will create tables
            that do not exist (if possible).

    """

    drivername: str = field(default="sqlite+pysqlite")
    username: str | None = field(default=None)
    password: str | None = field(default=None, repr=False)
    host: str | None = field(default=None)
    port: str | None = field(default=None)
    database: str = field(default="app.sqlite")
    echo: bool = field(default=False)

    def __post_init__(self):  # noqa: D105
        assert self.drivername is not None, ValueError("drivername cannot be None")
        assert isinstance(self.drivername, str), TypeError(
            f"drivername must be of type str. Got type: ({type(self.drivername)})"
        )
        assert isinstance(self.echo, bool), TypeError(
            f"echo must be a bool. Got type: ({type(self.echo)})"
        )
        if self.username:
            if self.username == "":
                self.username = None
            else:
                assert isinstance(self.username, str), TypeError(
                    f"user must be of type str. Got type: ({type(self.username)})"
                )
        if self.password:
            if self.password == "":
                self.password = None
            else:
                assert isinstance(self.password, str), TypeError(
                    f"password must be of type str. Got type: ({type(self.password)})"
                )
        if self.host:
            if self.host == "":
                self.host = None
            else:
                assert isinstance(self.host, str), TypeError(
                    f"host must be of type str. Got type: ({type(self.host)})"
                )
        if self.port:
            if self.port == "":
                self.port = None
            else:
                assert isinstance(self.port, int), TypeError(
                    f"port must be of type int. Got type: ({type(self.port)})"
                )
                assert self.port > 0 and self.port <= 65535, ValueError(
                    f"port must be an integer between 1 and 65535"
                )
        if self.database:
            assert isinstance(self.database, Path) or isinstance(
                self.database, str
            ), TypeError(
                f"database must be of type str or Path. Got type: ({type(self.database)})"
            )
            if isinstance(self.database, Path):
                self.database: str = f"{self.database}"

    def get_db_uri(self) -> sa.URL:
        """Construct a SQLAlchemy `URL` from class params.

        Returns:
            (sqlalchemy.URL): An initialized database connection URL.

        """
        try:
            _uri: sa.URL = sa.URL.create(
                drivername=self.drivername,
                username=self.username,
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

    def get_engine(self, echo_override: bool | None = None) -> sa.Engine:
        """Build & return a SQLAlchemy `Engine`.

        Returns:
            `sqlalchemy.Engine`: A SQLAlchemy `Engine` instance.

        """
        assert self.get_db_uri() is not None, ValueError("db_uri is not None")
        assert isinstance(self.get_db_uri(), sa.URL), TypeError(
            f"db_uri must be of type sqlalchemy.URL. Got type: ({type(self.db_uri)})"
        )

        if echo_override is not None:
            _echo: bool = echo_override
        else:
            _echo: bool = self.echo

        try:
            engine: sa.Engine = sa.create_engine(
                url=self.get_db_uri().render_as_string(hide_password=False),
                echo=_echo,
            )

            return engine
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception getting database engine. Details: {exc}"
            )

            raise msg

    def get_session_pool(self) -> so.sessionmaker[so.Session]:
        """Configure a session pool using class's SQLAlchemy `Engine`.

        Returns:
            (sqlalchemy.orm.sessionmaker): A SQLAlchemy `Session` pool for database connections.

        """
        engine: sa.Engine = self.get_engine()
        assert engine is not None, ValueError("engine cannot be None")
        assert isinstance(engine, sa.Engine), TypeError(
            f"engine must be of type sqlalchemy.Engine. Got type: ({type(engine)})"
        )

        session_pool: so.sessionmaker[so.Session] = so.sessionmaker(bind=engine)

        return session_pool

    @contextmanager
    def get_db(self) -> t.Generator[so.Session, t.Any, None]:
        """Context manager class to handle a SQLAlchemy Session pool.

        Usage:

        ```py title="get_db() dependency usage" linenums="1"

        ## Assumes `db_settings` is an initialized instance of `DBSettings`.
        with db_settings.get_db() as session:
            repo = someRepoClass(session)

            all = repo.get_all()
        ```
        """
        db: so.Session = self.get_session_pool()

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

#### DBConfig - Usage

```python title="How to use DBSettings class" linenums="1"
db_settings: DBSettings = DBSettings(
    drivername="postgresql+psycopg2",
    host="127.0.0.1",
    port=5432,
    username="postgres",
    password="postgres",
    database="example"
)
```

### Validators

#### Valid DB types

It's useful to have a `constants.py` or some other place to store validators; to limit the databases your project supports, you could create a `valid_db_types` variable, like:

```python title="constants.py - valid_db_types" linenums="1"
"""Validators for custom SQLAlchemy utilities.

`valid_db_types`: List of strings of supported database types.

Supported: `["sqlite", "postgres", "mssql"]`
"""

## List of valid/supported databases
from __future__ import annotations

valid_db_types: list[str] = ["sqlite", "postgres", "mssql"]

## Usage: assert 'some_db_name' not in valid_db_types, ValueError(f"Database 'some_db_name' is not supported. Supported databases: {valid_db_types}")
```

### SQLAlchemy dependencies

Dependencies for your database code. These can be context manager classes/functions, initialized objects, and other things to assist you interacting with the database.

```python title="_depends.py" linenums="1"
"""Dependencies for database.

Includes functions like `get_db()`, which is a context manager that yields a database session.
"""

from contextlib import contextmanager
import typing as t

from .db_config import DBSettings

import sqlalchemy as sa
import sqlalchemy.orm as so


@contextmanager
def get_db(db_settings: DBSettings = None) -> t.Generator[so.Session, t.Any, None]:
    """Dependency to yield a SQLAlchemy Session pool.

    Usage:

    from core.dependencies import get_db

    with get_db() as session:
        repo = someRepoClass(session)

        all = repo.get_all()
    
    """
    assert db_settings, ValueError("Missing DBSettings object.")

    SESSION_POOL: so.sessionmaker[so.Session] = db_settings.get_session_pool()

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

### Class mixins

SQLAlchemy supports "mixins," which are partial classes that define functionality when multi-inheritance is used to declare a table class. An example is the `TablenameMixin` class, which automatically creates a table name based on the class's name (i.e. a class named `UserComment` would be named `usercomments`).

#### Multi-inheritance example

```python title="SQLAlchemy table class multi-inheritance example" linenums="1"
import sqlalchemy as sa
import sqlalchemy.orm as so

from your_database_module.base import Base


class TableNameMixin:
    """Mixin to automatically name tables based on class name.

    Generates a `__tablename__` for classes inheriting from this mixin.
    """

    @so.declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class UserComment(Base, TabeNameMixin):
    ## No need to declare a table name, the table will be named 'usercomments'
    #   __table_name__ = "user_comments_tbl"

    ...

```

#### Example mixin classes

```python title="table_mixins.py" linenums="1"
"""SQLAlchemy models support multi-inheritance.

"Mixins" ([SQLAlchemy declarative mixins docs](https://docs.sqlalchemy.org/en/20/orm/declarative_mixins.html)) are partial classes
that predefine some attributes and methods. These can enhance SQLAlchemy table classes you create (model classes that inherit from your `Base`),
like adding a "modified" timestamp, or automatically naaming tables based on the model class's name.
"""

from __future__ import annotations

from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so


class TimestampMixin:
    """Add a created_at & updated_at column to records.

    Add to class declaration to automatically create these columns on
    records.

    Usage:

    py linenums=1
    class Record(Base, TimestampMixin):
        __tablename__ = ...

        ...

    """

    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now()
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()
    )


class TableNameMixin:
    """Mixin to automatically name tables based on class name.

    Generates a `__tablename__` for classes inheriting from this mixin.
    """

    @so.declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: D105
        return cls.__name__.lower() + "s"

```

## Annotated columns

- 📄 [SQLAlchemy docs: Mapping whole column declarations to Python types](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapping-whole-column-declarations-to-python-types)

### Example annotated columns

```python title="annotated_columns.py" linenums="1"
"""Define `Annotated` columns for SQLAlchemy models.

Examples:
    * `INT_PK`: An auto-incrementing, primary key integer value.
    * `STR_10`: A `VARCHAR(10)` column.
    * `STR_255`: A `VARCHAR(255)` column.

"""

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

### Full sample: From initializing DBSettings to adding an entity

!!! todo

    - [ ] Setup
        - [ ] `Base` creation
        - [ ] `DBSettings` init
            - [ ] (Optional) with `dynaconf`
    - [ ] Model classes
        - [ ] With mixin classes/multi-inheritance
        - [ ] With custom annotated columns
    - [ ] Get session & repository
    - [ ] Commit entity
