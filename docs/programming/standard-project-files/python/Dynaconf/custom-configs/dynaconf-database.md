# Dynaconf database configuration

This is the basis I use for configuring a database for use with SQLAlchemy. The settings classes and Dynaconf expect configurations to live at `config/db/*.toml`, if you put them somewhere else, make sure to update the Dynaconf `settings_files` path(s).

## Settings files

### db/settings.toml

```toml title="config/db/settings.toml" linenums="1"
[default]

db_type = "sqlite"
db_drivername = "sqlite+pysqlite"
db_username = ""
# Set in db/.secrets.toml
# db_password = ""
db_host = ""
db_port = ""
db_database = ".data/app.sqlite"
db_echo = false

[dev]

db_type = "sqlite"
db_drivername = "sqlite+pysqlite"
db_username = ""
# Set in db/.secrets.toml
# db_password = ""
db_host = ""
db_port = ""
db_database = ".data/app-dev.sqlite"
db_echo = true

[prod]

db_type = "sqlite"
db_drivername = "sqlite+pysqlite"
db_username = ""
# Set in db/.secrets.toml
# db_password = ""
db_host = ""
db_port = ""
db_database = ".data/app.sqlite"
db_echo = false

```

### db/.secrets.toml base

```toml title="config/db/.secrets.toml" linenums="1"
[default]

db_password = ""

[dev]

db_password = ""

[prod]

db_password = ""

```

## Config classes

### Pydantic db_config.py

```python title="db_config.py" linenums="1"
from dynaconf import Dynaconf
from pydantic import Field, field_validator, ValidationError
from pydantic_settings import BaseSettings

import sqlalchemy as sa
import sqlalchemy.orm as so

valid_db_types: list[str] = ["sqlite", "postgres", "mssql"]

DYNACONF_SETTINGS  = Dynaconf(
    environments=True,
    envvar_prefix="DB",
    settings_files=["db/settings.toml", "db/.secrets.toml"]
)


class DBSettings(BaseSettings):
    type: str = Field(default=DYNACONF_SETTINGS.DB_TYPE, env="DB_TYPE")
    drivername: str = Field(
        default=DYNACONF_DB_SETTINGS.DB_DRIVERNAME, env="DB_DRIVERNAME"
    )
    user: str | None = Field(
        default=DYNACONF_DB_SETTINGS.DB_USERNAME, env="DB_USERNAME"
    )
    password: str | None = Field(
        default=DYNACONF_DB_SETTINGS.DB_PASSWORD, env="DB_PASSWORD", repr=False
    )
    host: str | None = Field(default=DYNACONF_DB_SETTINGS.DB_HOST, env="DB_HOST")
    port: Union[str, int, None] = Field(
        default=DYNACONF_DB_SETTINGS.DB_PORT, env="DB_PORT"
    )
    database: str = Field(default=DYNACONF_DB_SETTINGS.DB_DATABASE, env="DB_DATABASE")
    echo: bool = Field(default=DYNACONF_DB_SETTINGS.DB_ECHO, env="DB_ECHO")

    @field_validator("port")
    def validate_db_port(cls, v) -> int:
        if v is None or v == "":
            return None
        elif isinstance(v, int):
            return v
        elif isinstance(v, str):
            return int(v)
        else:
            raise ValidationError

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

### Dataclass db_config.py

If you don't install `pydantic`/`pydantic_settings`, you can use this `dataclass` instead. It's a bit more fragile because of `pydantic`'s superior validation & parsing, but it generally works alright!

```python title="db_config.py dataclass version" linenums="1"
"""Contained database configuration class.

The `DBSettings` defined in `core.config` is generic. The `DBSettings` defined
in this module can be configured/tweaked for this specific project.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
import typing as t

import sqlalchemy as sa
import sqlalchemy.orm as so

from dynaconf import Dynaconf

valid_db_types: list[str] = ["sqlite", "postgres", "mssql"]

DYNACONF_SETTINGS  = Dynaconf(
    environments=True,
    envvar_prefix="DB",
    settings_files=["db/settings.toml", "db/.secrets.toml"]
)


@dataclass
class DBSettings:
    """Store configuration for a database.

    Params:
        drivername (str): The `sqlalchemy` driver name, i.e. `'sqlite+pysqlite'`.
        user (str|None): The database user's username.
        password (str|None): The database user's password.
        host (str|None): The database host address.
        port (str|int|None): The database host's port.
        database (str): The name of the database to connect to. For SQLite, use the path to the file,
            i.e. `db/app.sqlite`.
        echo (bool): If `True`, the SQLAlchemy `Engine` will echo SQL queries to the CLI, and will create tables
            that do not exist (if possible).

    """

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
        """Build & return a SQLAlchemy `Engine`.

        Returns:
            `sqlalchemy.Engine`: A SQLAlchemy `Engine` instance.

        """
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

        ``py title="get_db() dependency usage" linenums="1"

        ## Assumes `db_settings` is an initialized instance of `DBSettings`.
        with db_settings.get_db() as session:
            repo = someRepoClass(session)

            all = repo.get_all()
        ``
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


db_settings: DBSettings = DBSettings(
    drivername=DYNACONF_SETTINGS.DB_DRIVERNAME,
    user=DYNACONF_SETTINGS.DB_USERNAME,
    password=DYNACONF_SETTINGS.DB_PASSWORD,
    host=DYNACONF_SETTINGS.DB_HOST,
    port=DYNACONF_SETTINGS.DB_PORT,
    database=DYNACONF_SETTINGS.DB_DATABASE,
    echo=DYNACONF_SETTINGS.DB_ECHO,
)


```
