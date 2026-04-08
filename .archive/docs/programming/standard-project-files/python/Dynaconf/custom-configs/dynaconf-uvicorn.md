---
tags:
    - standard-project-files
    - python
    - dynaconf
    - uvicorn
---

# Dynaconf Uvicorn Configuration

Configure a `uvicorn` server.

## Settings files

### uvicorn/settings.toml

```toml title="config/uvicorn/settings.toml" linenums="1"
[default]

UVICORN_APP = "api.api_main:app"
UVICORN_HOST = "0.0.0.0"
UVICORN_PORT = 8000
UVICORN_ROOT_PATH = "/"
UVICORN_RELOAD = false
UVICORN_LOG_LEVEL = "INFO"

[dev]

UVICORN_APP = "api.api_main:app"
UVICORN_HOST = "0.0.0.0"
UVICORN_PORT = 8080
UVICORN_ROOT_PATH = "/"
UVICORN_RELOAD = true
UVICORN_LOG_LEVEL = "DEBUG"

[prod]
```

### uvicorn/.secrets.toml

```toml title="config/uvicorn/.secrets.toml" linenums="1"
[default]

[dev]

[prod]
```

## Config classes

### Pydantic uvicorn_config.py

```python title="uvicorn_config.py" linenums="1"
from __future__ import annotations

from pathlib import Path
import typing as t

from dynaconf import Dynaconf
from pydantic import ConfigDict, Field, ValidationError, computed_field, field_validator
from pydantic_settings import BaseSettings

DYNACONF_UVICORN_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    ## If you aren't using [dev] and [prod] envs,
    #  uncomment line below and add a [uvicorn] section to your settings.local.toml
    # env="uvicorn",
    envvar_prefix="UVICORN",
    settings_files=["uvicorn/settings.toml", "uvicorn/.secrets.toml"],
)


class UvicornSettings(BaseSettings):
    """Store configuration for the Uvicorn server.

    Params:
        app (str): Path to the FastAPI `App()` instance, i.e. `main:app`.
        host (str): Host address/FQDN for the server.
        port (int): Port the server should run on.
        root_path (str): The server's root path/endpoint.
        reload (bool): If `True`, server will reload when changes are detected.
        log_level (str): The log level for the Uvicorn server.
    """

    app: str = Field(default=DYNACONF_UVICORN_SETTINGS.UVICORN_APP, env="UVICORN_APP")
    host: str = Field(
        default=DYNACONF_UVICORN_SETTINGS.UVICORN_HOST, env="UVICORN_HOST"
    )
    port: int = Field(
        default=DYNACONF_UVICORN_SETTINGS.UVICORN_PORT, env="UVICORN_PORT"
    )
    root_path: str = Field(
        default=DYNACONF_UVICORN_SETTINGS.UVICORN_ROOT_PATH, env="UVICORN_ROOT_PATH"
    )
    reload: bool = Field(
        default=DYNACONF_UVICORN_SETTINGS.UVICORN_RELOAD, env="UVICORN_RELOAD"
    )
    log_level: str = Field(
        default=DYNACONF_UVICORN_SETTINGS.UVICORN_LOG_LEVEL, env="UVICORN_LOG_LEVEL"
    )


## Initialize a UvicornSettings object
uvicorn_settings: UvicornSettings = UvicornSettings()

```
