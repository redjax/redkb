# DBConfig settings class

I use a Python `dataclass` to store my database settings. The `DBSettings` class below accepts SQLAlchemy parameters for a database connection, and handles getting session pools, engines, and more using class methods.

```python title="DBConfig settings" linenums="1"
from __future__ import annotations

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
            f"db_uri must be of type sqlalchemy.URL. Got type: ({type(self.get_db_uri)})"
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
        SESSION_POOL: so.sessionmaker[so.Session] = self.get_session_pool()
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

## DBConfig - Usage

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
