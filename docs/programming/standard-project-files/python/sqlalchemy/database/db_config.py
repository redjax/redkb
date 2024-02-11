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
