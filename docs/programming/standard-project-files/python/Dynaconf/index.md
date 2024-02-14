---
tags:
    - standard-project-files
    - python
    - dynaconf
---

# Dynaconf base files

I use [`Dynaconf`](https://dynaconf.com) frequently to manage loading my project's settings from a local file (`config/settings.local.toml`) during development, and environment variables when running in a container. `Dynaconf` allows for overriding configurations by setting environment variables.

To load configurations from the environment, you can:

* Set environment variables by prepending them with the configured `envvar_prefix` value of a `Dynaconf()` instance
    * Example: To set a value `LOG_LEVEL`: `export DYNACONF_LOG_LEVEL=...`
* Create a `config/settings.local.toml` file
    * The `config/settings.toml` file should not be edited, nor should it contain any real values
    * This file is meant to be added to source control, then copied to `config/settings.local.toml` during local development
    * Set your real values in `config/settings.local.toml`

## settings.toml base

!!!note
    The `Database` section is commented below because not all projects will start with a database. This file can still be copy/pasted to `config/settings.toml`/`config/settings.local.toml` as a base/starting point.

```toml title="config/settings.toml (and config/settings.local.toml)" linenums="1"
##
# My standard Dynaconf settings.toml file.
#
# I normally put this file in a directory like src/config/settings.toml, then update my config.py, adding
# root_path="config" to the Dynaconf instance.
##

[default]

env = "prod"
container_env = false
log_level = "INFO"

############
# Database #
############

# db_type = "sqlite"
# db_drivername = "sqlite+pysqlite"
# db_username = ""
# # Set in .secrets.toml
# db_password = ""
# db_host = ""
# db_port = ""
# db_database = ".data/app.sqlite"
# db_echo = false

[dev]

env = "dev"
log_level = "DEBUG"

############
# Database #
############

# db_type = "sqlite"
# db_drivername = "sqlite+pysqlite"
# db_username = ""
# # Set in .secrets.toml
# db_password = ""
# db_host = ""
# db_port = ""
# db_database = ".data/app-dev.sqlite"
# db_echo = true

[prod]

############
# Database #
############

# db_type = "sqlite"
# db_drivername = "sqlite+pysqlite"
# db_username = ""
# # Set in .secrets.toml
# db_password = ""
# db_host = ""
# db_port = ""
# db_database = ".data/app.sqlite"
# db_echo = false

```

## .secrets.toml base

!!!note
    The `Database` section is commented below because not all projects will start with a database. This file can still be copy/pasted to `config/.secrets.toml` as a base/starting point.

```toml title="config/.secrets.toml" linenums="1"
##
# Any secret values, like an API key or database password, or Azure connection string.
##

[default]

############
# Database #
############

# db_password = ""

[dev]

############
# Database #
############

# db_password = ""

[prod]

############
# Database #
############

# db_password = ""

```

## My Pydantic config.py file

!!!warning

    This code is highly specific to the way I structure my apps. Make sure to understand what it's doing so you can customize it to your environment, if you're using this code as a basis for your own `config.py` file

!!!note

    Notes:

    The following imports/vars/classes start out commented, in case the project is not using them or they require additional setup:
      
      - All SQLAlchemy imports
      - The `valid_db_types` list (used to validate `DBSettings.type`)
      - The `DYNACONF_DB_SETTINGS` Dynaconf settings object
      - The `DBSettings` class definition

    If the project is using a database and SQLAlchemy as the ORM, uncomment these values and modify your `config/settings.local.toml` & `config/.secrets.toml` accordingly.

```py title="core/config.py" linenums="1"
from __future__ import annotations

from typing import Union

from dynaconf import Dynaconf
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

## Uncomment if adding a database config
# import sqlalchemy as sa
# import sqlalchemy.orm as so

DYNACONF_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
)

## Uncomment if adding a database config
# valid_db_types: list[str] = ["sqlite", "postgres", "mssql"]

## Uncomment to load database settings from environment
# DYNACONF_DB_SETTINGS: Dynaconf = Dynaconf(
#     environments=True,
#     envvar_prefix="DB",
#     settings_files=["settings.toml", ".secrets.toml"],
# )


class AppSettings(BaseSettings):
    env: str = Field(default=DYNACONF_SETTINGS.ENV, env="ENV")
    container_env: bool = Field(
        default=DYNACONF_SETTINGS.CONTAINER_ENV, env="CONTAINER_ENV"
    )
    log_level: str = Field(default=DYNACONF_SETTINGS.LOG_LEVEL, env="LOG_LEVEL")


## Uncomment if you're configuring a database for the app
# class DBSettings(BaseSettings):
#     type: str = Field(default=DYNACONF_SETTINGS.DB_TYPE, env="DB_TYPE")
#     drivername: str = Field(
#         default=DYNACONF_DB_SETTINGS.DB_DRIVERNAME, env="DB_DRIVERNAME"
#     )
#     user: str | None = Field(
#         default=DYNACONF_DB_SETTINGS.DB_USERNAME, env="DB_USERNAME"
#     )
#     password: str | None = Field(
#         default=DYNACONF_DB_SETTINGS.DB_PASSWORD, env="DB_PASSWORD", repr=False
#     )
#     host: str | None = Field(default=DYNACONF_DB_SETTINGS.DB_HOST, env="DB_HOST")
#     port: Union[str, int, None] = Field(
#         default=DYNACONF_DB_SETTINGS.DB_PORT, env="DB_PORT"
#     )
#     database: str = Field(default=DYNACONF_DB_SETTINGS.DB_DATABASE, env="DB_DATABASE")
#     echo: bool = Field(default=DYNACONF_DB_SETTINGS.DB_ECHO, env="DB_ECHO")

#     @field_validator("port")
#     def validate_db_port(cls, v) -> int:
#         if v is None or v == "":
#             return None
#         elif isinstance(v, int):
#             return v
#         elif isinstance(v, str):
#             return int(v)
#         else:
#             raise ValidationError

#     def get_db_uri(self) -> sa.URL:
#         try:
#             _uri: sa.URL = sa.URL.create(
#                 drivername=self.drivername,
#                 username=self.user,
#                 password=self.password,
#                 host=self.host,
#                 port=self.port,
#                 database=self.database,
#             )

#             return _uri

#         except Exception as exc:
#             msg = Exception(
#                 f"Unhandled exception getting SQLAlchemy database URL. Details: {exc}"
#             )
#             raise msg

#     def get_engine(self) -> sa.Engine:
#         assert self.get_db_uri() is not None, ValueError("db_uri is not None")
#         assert isinstance(self.get_db_uri(), sa.URL), TypeError(
#             f"db_uri must be of type sqlalchemy.URL. Got type: ({type(self.db_uri)})"
#         )

#         try:
#             engine: sa.Engine = sa.create_engine(
#                 url=self.get_db_uri().render_as_string(hide_password=False),
#                 echo=self.echo,
#             )

#             return engine
#         except Exception as exc:
#             msg = Exception(
#                 f"Unhandled exception getting database engine. Details: {exc}"
#             )

#             raise msg

#     def get_session_pool(self) -> so.sessionmaker[so.Session]:
#         engine: sa.Engine = self.get_engine()
#         assert engine is not None, ValueError("engine cannot be None")
#         assert isinstance(engine, sa.Engine), TypeError(
#             f"engine must be of type sqlalchemy.Engine. Got type: ({type(engine)})"
#         )

#         session_pool: so.sessionmaker[so.Session] = so.sessionmaker(bind=engine)

#         return session_pool


settings: AppSettings = AppSettings()
## Uncomment if you're configuring a database for the app
# db_settings: DBSettings = DBSettings()

```