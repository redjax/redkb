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
# I normally put this file in a directory like config/settings.toml, then update my config.py, adding
# root_path="config" to the Dynaconf instance.
##

[default]

env = "prod"
container_env = false
log_level = "INFO"

[dev]

env = "dev"
log_level = "DEBUG"

[prod]

```

## .secrets.toml base

```toml title="config/.secrets.toml" linenums="1"
##
# Any secret values, like an API key or database password, or Azure connection string.
##

[default]

[dev]

[prod]

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

DYNACONF_SETTINGS: Dynaconf = Dynaconf(
    environments=True,
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
)

class AppSettings(BaseSettings):
    env: str = Field(default=DYNACONF_SETTINGS.ENV, env="ENV")
    container_env: bool = Field(
        default=DYNACONF_SETTINGS.CONTAINER_ENV, env="CONTAINER_ENV"
    )
    log_level: str = Field(default=DYNACONF_SETTINGS.LOG_LEVEL, env="LOG_LEVEL")



settings: AppSettings = AppSettings()

```
