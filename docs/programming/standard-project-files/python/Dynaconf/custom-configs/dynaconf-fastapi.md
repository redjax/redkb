---
tags:
    - standard-project-files
    - python
    - dynaconf
    - fastapi
---

# Dynaconf FastAPI configuration

Configure a `fastapi` application.

## Settings files

### fastapi/settings.toml

```toml title="config/fastapi/settings.toml" linenums="1"
[default]

FASTAPI_DEBUG = false
FASTAPI_TITLE = "DEFAULT_APPNAME"
FASTAPI_SUMMARY = "DEFAULT_SUMMARY"
FASTAPI_DESCRIPTION = "DEFAULT_DESCRIPTION"
FASTAPI_VERSION = "0.1.0"
FASTAPI_OPENAPI_URL = "/openapi.json"
FASTAPI_REDIRECT_SLASHES = true
FASTAPI_DOCS_URL = "/docs"
FASTAPI_REDOC_URL = "/redoc"
FASTAPI_OPENAPI_PREFIX = ""
FASTAPI_ROOT_PATH = ""
FASTAPI_ROOT_PATH_IN_SERVERS = true

## Include custom admin router
FASTAPI_INCLUDE_ADMIN_ROUTER = false

[dev]

FASTAPI_DEBUG = true
FASTAPI_TITLE = "[DEV] DEFAULT_APPNAME"

## Include custom admin router
FASTAPI_INCLUDE_ADMIN_ROUTER = true

[prod]

```

### fastapi/.secrets.toml

```toml title="config/fastapi/.secrets.toml" linenums="1"
[default]

[dev]

[prod]

```

## Config classes

### Pydantic fastapi_config.py

```python title="fastapi_config.py" linenums="1"
from __future__ import annotations

from pathlib import Path
import typing as t

from dynaconf import Dynaconf
from loguru import logger as log
from pydantic import ConfigDict, Field, ValidationError, computed_field, field_validator
from pydantic_settings import BaseSettings

DYNACONF_API_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    envvar_prefix="FASTAPI",
    settings_files=["fastapi/settings.toml", "fastapi/.secrets.toml"],
)


class APISettings(BaseSettings):
    debug: bool = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_DEBUG, env="FASTAPI_DEBUG"
    )
    title: str = Field(default=DYNACONF_API_SETTINGS.FASTAPI_TITLE, env="FASTAPI_TITLE")
    summary: str = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_SUMMARY, env="FASTAPI_SUMMARY"
    )
    description: str = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_DESCRIPTION, env="FASTAPI_DESCRIPTION"
    )
    version: str = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_VERSION, env="FASTAPI_VERSION"
    )
    openapi_url: str = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_OPENAPI_URL, env="FASTAPI_OPENAPI_URL"
    )
    redirect_slashes: bool = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_REDIRECT_SLASHES,
        env="FASTAPI_REDIRECT_SLASHES",
    )
    docs_url: str = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_DOCS_URL, env="FASTAPI_DOCS_URL"
    )
    redoc_url: str = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_REDOC_URL, env="FASTAPI_REDOC_URL"
    )
    openapi_prefix: str = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_OPENAPI_PREFIX,
        env="FASTAPI_OPENAPI_PREFIX",
    )
    root_path: str = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_ROOT_PATH, env="FASTAPI_ROOT_PATH"
    )
    root_path_in_servers: bool = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_ROOT_PATH_IN_SERVERS,
        env="FASTAPI_ROOT_PATH_IN_SERVERS",
    )
    include_admin_router: bool = Field(
        default=DYNACONF_API_SETTINGS.FASTAPI_INCLUDE_ADMIN_ROUTER,
        env="FASTAPI_INCLUDE_ADMIN_ROUTER",
    )

    @field_validator("include_admin_router")
    def validate_include_admin_router(cls, v) -> bool:
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            match v.lower():
                case "true":
                    return True
                case "false":
                    return False
                case _:
                    raise ValidationError

        raise ValidationError


api_settings: APISettings = APISettings()

```
