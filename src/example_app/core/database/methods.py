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
