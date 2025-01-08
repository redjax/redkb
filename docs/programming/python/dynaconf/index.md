---
tags:
  - python
  - dynaconf
  - configuration
  - environment
---

# Dynaconf <!-- omit in toc -->

[Dynaconf](https://www.dynaconf.com) is a tool for managing app configurations. The tool is inspired by the [12-factor application guide](https://12factor.net/config), and is focused on assisting with separating your app's configuration from the business logic.

!!! tip

    If you just want to see Dynaconf in action, you can skip to the [Example app](#example-app) section.

## Providing Configurations to Dynaconf

Dynaconf is very flexible, and [can read configurations from a number of formats](https://www.dynaconf.com/settings_files/#supported-formats) (`.toml`, `.json`, `.yaml`, `.env`), and from the environment itself. The documentation covers different methods of loading environment variables, but the flow I've settled on is defining `.toml` settings and secrets files in a `config/` directory, breaking the settings into environments (`[dev]`, `[rc]`, `[prod]`) and creating individual `Dynaconf()` settings objects for each configuration domain (`app`, `logging`, `database`, etc). This sentence will make more sense as you read on.

Dynaconf reads variables in the following order:

- The environment, or from CLI args
    - You can set env variables in your environment (`export VAR_NAME=value` on Linux, `$env:VAR_NAME = 'value'` on Windows), but note that you must prepend the variable name with `DYNACONF_` for Dynaconf to detect it.
        - You can sometimes get away with changing the `envvar_prefix=` portion of a `Dynaconf()` instantiation, but to *reliably* read a variable from the environment with Dynaconf, you should set `DYNACONF_` before the variable name.
        - For example, if you have an environment variable named `LOG_LEVEL`, you would define it like: `export DYNACONF_LOG_LEVEL=...`.
    - You can also prepend a Python command with variables for Dynaconf to load, like:
        - `LOG_LEVEL='DEBUG' python app.py`
        - Or, for more durability, `DYNACONF_LOG_LEVEL='DEBUG' python app.py`
- `.secrets*.toml`, `settings*.toml`, `.secrets*.json`, `settings*.json`, etc
      - The `*` in each settings file above indicates `dynaconf` will read the `settings.local.toml`/`settings.local.json` version of the file, if it exists, before trying to read from `settings.toml`/`settings.json`.
- Default values
    - When retrieving a value from a `Dynaconf()` object, you can set a default value, which is 3rd in precedence:
        - `DYNACONF_SETTINGS_OBJECT.get("ENV_VAR_NAME", default="The default value")`
- Global defaults:
    - If no value can be determined using a method above, `dynaconf` will try to use global defaults as a fallback, i.e. `null`/`None` or any value you've configured as a default in your code.

### Environment Variables

Dynaconf reads from the environment first. You can set environment variables on your host (search online for 'how to set environment variable on <OS>' to see how to do this for your specific environment), or if you're running in Docker, with the `environment:` section.

When you define environment variables for Dynaconf to read, you should prepend the variable name with `DYNACONF_`. This prefix catches Dynaconf's attention right away and ensure that the value is read. If you are expecting a variable named, for example, `LOG_LEVEL`, you would set the environment variable `DYNACONF_LOG_LEVEL`, and the value will be accessible in a `Dynaconf()` object as `LOG_LEVEL`. Note that the `DYNACONF_` prefix is not needed when retrieving a value Dynaconf has already loaded, it's only necessary for telling Dynaconf to load that value in the first place.

You can play around with the `envvar_prefix=` portion of a `Dynaconf()` settings object, but I recommend getting into the habit of using the `DYNACONF_` prefix. After much trial and error on my end, this is a surefire way to make sure Dynaconf reads your configuration.

Here are some example environment variables I might set in a Python app I'm writing:

```text title="Example environment variables"
## If I'm using Dynaconf's environments to separate by production, dev, etc
# ENV_FOR_DYNACONF="dev"

## Configure my logging level dynamically
DYNACONF_LOG_LEVEL="DEBUG"  # Dynaconf reads this variable as 'LOG_LEVEL'

## Configure a max HTTP timeout on requests
DYNACONF_HTTP_TIMEOUT=15
```

### Setting File (.toml, .json, .yaml, .env)

Dynaconf can read from [many file formats](https://www.dynaconf.com/settings_files/#supported-formats), but my preferred format (and the one you will see most often in the documentation and in examples online) is the `.toml` format. This guide assumes you are using `.toml` files for configuration.

When running in Production, you should use [environment variables](#environment-variables) for configuring your app. These `.toml` file examples are great for local development, and you *could* provide a Production app with a Production `settings.toml` file to read, but configuring with environment variables is the best way to load your environment variables into an app.

!!! warning

    This guide uses the term "environment variables" to describe non-sensitive app configurations, like the timezone or logging level. For local development, it is acceptable to use a `.secrets.toml` file, but in Production you should always load from a secure vault of some sort. Leaving password in plain text anywhere in the environment is bad practice, and should be avoided even when self-hosting.

Dynaconf will start reading at the current path `./` for `.toml` files, and if no `settings.toml`/`settings.local.toml` file is found, will look for a `config/` directory.

I put my `.toml` configuration files in a `config/` directory because I tend to create separate files for different parts of the app (`config/settings.toml` for my app's configuration like logging, `config/database/settings.toml` for database settings, etc). This guide will assume your `settings.toml` file(s) exist in a `config/` directory at the repository root.

There are a number of ways to write a `settings.toml` file. This is a simple example of a valid configuration file:

```toml title="Example settings.toml file for Dynaconf" linenums="1"
## settings.toml
log_level = "DEBUG"
```

You can also add "environments" to a settings file, and tell Dynaconf to read from a specific environment when it loads the configuration. Environments are created with `[brackets]`, and you should provide a `[default]` environment where you set all of your variables and a default value:

```toml title="Example settings.toml with app environments" linenums="1"
## settings.toml
[default]
log_level = "INFO"

[dev]
## Set env='logging' in your Dynaconf object.
#  Dynaconf will use this value before the default value, if it's defined
log_level = "DEBUG"

[rc]
## Omit the log_level to use the default INFO in production

[prod]
## Show only warning & error messages in Production
log_level = "WARNING
```

You can also use environments to define arbitrary environments like `[cli]` for running in a pipeline, or `[container]` when running in a container environment.

When using `production`/`dev` environments like this, you must set an `ENV_FOR_DYNACONF={dev,prod,testing,etc}`, where the value matches an `[environment]` in your settings file. This will tell Dynaconf to only load values from the matching `[environment]`.

### Secrets file

For local development, you can also store secrets (API keys, passwords, etc) in a `.secrets.toml` file. You **can** commit this file to git, because you should be creating a `.secrets.local.toml` file to override the defaults you set in `.secrets.toml`. **DO NOT COMMIT THE .local VERSION OF YOUR SECRETS FILE TO GIT**! You should put real values in `.secrets.local.toml`, and you do not want to track those in version control!

Declaring secrets is exactly the same as writing a `settings.toml` file. You do not even *have* to separate these configurations, but it is recommended to separate secrets from configurations for cleanliness and separation of concerns.

Like your `settings.toml` file, you should put your "actual" configuration in a non-source controlled `.secrets.local.toml`. Dynaconf knows to read the `.local.toml` version of a config before the version without `.local` in the name, you do not need to do anything special for this functionality:

```toml title="Example .secrets.toml file" linenums="1"
## .secrets.local.toml
[default]
## 'service' here could be anything; if you're adding a key to WeatherAPI for example,
#  you could name this value 'weatherapi_api_key'
service_api_key = ""

## Create an environment for the 'service' above. Again, using WeatherAPI as the example,
#  this section would be called [weatherapi] in a "real" .secrets.toml file
[dev]
service_api_key = "hgib1n5g-l159nruo-b083n34k"

[rc]
service_api_key = "hgib1n5g-l159nruo-b083n34k"

[production]
## Use a different key for Production
service_api_key = "lgborne-giotnri2-9bf0njl0"
```

## Reading Configurations with Dynaconf

Look at this code and keep it in mind as you read through the rest of the examples; this is one way to load environment variables with Dynaconf. I prefer this method using `.get()` because you can set a default value if no environment variable is detected:

```python title="Retrieving env variables with Dynaconf" linenums="1"
## The variable name (on the left of the = ) can be anything; DYNACONF_SETTINGS
#  is a generic variable you will see in the Dynaconf configuration.
DYNACONF_SETTINGS.get("VAR_NAME", default="Default Value")
```

We will go into more detail on the code above in another section, but the simple way of describing what is happening above is that your code is reading a `Dynaconf()` object (you will see an example of this below) object you named `DYNACONF_SETTINGS` for an environment variable named `VAR_NAME`, and setting a value of `"Default Value"` if the environment variable is not found.

### The Dynaconf() object

After defining your configurations in the environment or [in a supported file](#setting-file-toml-json-yaml-env), you need to create a `Dynaconf()` object to load those settings. This is where Dynaconf's flexibility really comes into play. You can create a single `Dynaconf()` settings object for the entire app, or you can use `envvar_prefix=` to "scope" your configurations.

Below are 2 examples of loading environment variables with a `Dynaconf()` object. The first example assumes you are using the `[environment]` tags to separate configurations by domain, i.e. `[logging]` and `[database]`, while the second example assumes you're using the `[production]`/`[dev]`/etc environment definitions.

### Environment Tags as Configuration Domains

Example `settings.toml` file:

```toml title="settings.toml" linenums="1"
[default]
log_level = "INFO"

[dev]
log_level = "DEBUG"

[rc]

[prod]
log_level = "WARNING"
```

```python title="Load settings with Dynaconf" linenums="1"
from dynaconf import Dynaconf

## Load the logging settings from the [logging] section of a settings.toml file
#  Dynaconf will check the environment for any DYNACONF_LOG_xxx value first, then
#  read settings.local.toml, then settings.toml for a log_level value
LOGGING_SETTINGS = Dynaconf(
    ## Enable reading [environment] tags
    environments=True,
    ## Tell Dynaconf to read environment variables starting with DYNACONF_LOG or LOG_
    envvar_prefix="LOG",
    ## Tell Dynaconf to look for ./settings.toml, ./settings.local.toml, or config/settings[.local].toml,
    #  and the same for .secrets[.local].toml or config/.secrets[.local].toml
    settings_files=["settings.toml", ".secrets.toml"]
)

## This should return 'DEBUG' because of the configuration in [logging] in the settings.toml file
#  If the log_level variable is not set in the environment or a settings.toml file, default to '"INFO"'
print(LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))

```

If you are using Dynaconf environments to separate values into different environments like `dev`, `prod`, etc, it is advisable to break the `.toml` settings files into domain-specific configurations, like `settings.logging.toml`/`settings.logging.local.toml`, or in separate subdirectories like `config/logging/{settings,.secrets}.toml`. You can set the `[environment]` Dynaconf should read from using the `ENV_FOR_DYNACONF` environment variable; to read the `[dev]` configuration, you would set `ENV_FOR_DYNACONF="dev"` in your environment. Dynaconf is built to be very flexible, and allows for separating configurations by domain (app, logging, http_server, for example).

You can also store all of your configuration domains in a single `settings.toml` file, using variable prefixes like `log_` and `api_` to separate configuration domains.

```toml title="Domain-specific 'logging' settings file" linenums="1"
## config/logging/settings.toml
[default]
log_level = "INFO"
api_key = ""

[dev]
log_level = "DEBUG"
api_key = "bntkq2wo-gbbab340-olkjb2ti"

[rc]
log_level = "INFO"
api_key = "kgbnaorjb-nosbn234-oab564ag"

[prod]
log_level = "WARNING"
api_key = "ljatbo23-b007a43-alkjatph"

## You can configure a lower/higher (depending on how you understand log levels)
#  level when ENV_FOR_DYNACONF="ci", like in a pipeline
[ci]
log_level = "VERBOSE"
## CI environment in this example does not require an API key,
#  so it is omitted and defaults to ""
```

## Gitignore

You should commit your `settings.toml` and `.secrets.toml` file(s) to git, but do not put your "real" values in these files. Instead, use default or empty values, and create `settings.local.toml` and `.secrets.local.toml` files, which should *not* be committed to git.

Here's an example `.gitignore` that will ignore all `.local.toml` configurations:

```.gitignore title="Example .gitignore for Dynaconf" linenums="1"
## .gitignore

## Dynaconf
**/*.local.toml

!**/*.example.toml
!**/.*.example.toml
```

## Example app

Here you can see a simple example of configuring an app with Dynaconf. The app will make a request to the [Faker API](https://fakerapi.it), with values configured from the environment.

I am using [HTTPX](https://www.python-httpx.org/) as my request client because I prefer it over the `requests` package.

For the sake of example, this app will use Dynaconf's environments feature to separate configurations by domain; this example does not use `[dev]`/`[production]`/etc environments. If you want to use these environments instead, create separate files for each `[section]` you see below.

### Settings files

First I'll create a `config/` directory, and a `settings.toml` and `.secrets.toml` file. These will be committed to source control, and I will set default values here with the idea that when I clone this repository on a new machine, I will manually create a `settings.local.toml` and `.secrets.local.toml` file, copying the contents of these 2 source controlled files into the ignored `.local` versions and modifying them for local execution.

```toml title="Dynaconf settings.toml file" linenums="1"
## settings.toml
[default]
log_level = "INFO"

fakerapi_base_url = "https://fakerapi.it/api/v2"
fakerapi_endpoint = "addresses"
fakerapi_quantity = 1

[dev]
log_level = "DEBUG"
## I am not updating the base URL. Leaving this commented will default to the value
#  in the [default] section above
# fakerapi_base_url = ""
## Use the /books endpoint instead of /addresses
fakerapi_endpoint = "books"

[rc]
log_level = "WARNING"
## Ask for 3 addresses instead of 1
fakerapi_quantity = 3
```

The FakerAPI does not require an API key, but if it did, I would also declare it in my `.secrets.toml` file:

```toml title="Dynaconf .secrets.toml file" linenums="1"
## .secrets.toml
[default]
fakerapi_api_key = ""

[dev]
## Put a placeholder API key for the user to replace when they create a
#  .secrets.local.toml file
fakerapi_api_key = "<your-fakerapi-api-key>"
```

After creating these 2 files and adding them to source control, I will copy them to the `.local` version and edit them:

```shell title="Copy source controlled settings files to local dev versions" linenums="1"
cp config/settings.toml config/settings.local.toml
cp config/.secrets.toml config/.secrets.local.toml
```

Again, these `.local.toml` versions of the settings files **should not be committed to git**. You will create these files locally on fresh clones and use them for local testing (i.e. not in a Docker container, where you can just set the values as environment variables).

To tell my app which configuration environment to use (dev, rc, or prod), set an an environment variable called `ENV_FOR_DYNACONF`:

```bash title="Set Dynaconf env on Linux/Mac" linenums="1"
export ENV_FOR_DYNACONF=dev
```

```bash title="Set Dynaconf env on Windows" linenums="1"
$env:ENV_FOR_DYNACONF="dev"
```

### Dynaconf() object

Now I'll create a file named `settings.py`, where I will load these configurations. Dynaconf is incredibly flexible in this regard; you can put your `Dynaconf()` objects anywhere, they can be alongside your business logic, in a separate file so you can import them throughout the app, you can define multiple `Dynaconf()` objects in a single Python project to load different sections of your settings/environment, etc.

I am keeping things simple for this example by creating a `settings.py` file, where I will initialize all of my `Dynaconf()` objects so I can import them in other scripts.

```python title="Example settings.py script that loads configurations from the environment/settings.toml file" linenums="1"
## settings.py

from dynaconf import Dynaconf

## Initialize a logging config object.
#  This object will only load variables in the [logging] section of settings.toml/.secrets.toml,
#  or from environment variables that start with DYNACONF_LOG_ or LOG_
LOGGING_SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="LOG",
    settings_files=["settings.toml", ".secrets.toml"]
)

## Initialize FakerAPI config object.
#  This object will only load variables in the [fakerapi] section of settings.toml/.secrets.toml,
#  or from environment variables that start with DYNACONF_FAKERAPI_ or FAKERAPI_
FAKERAPI_SETTINGS = Dynaconf(
    environments=True,
    envvar_prefix="FAKERAPI",
    settings_files=["settings.toml", ".secrets.toml"]
)
```

### Python app

Now, in a `main.py`, I will configure my logging from the `LOGGING_SETTINGS` object, and make a request to the Faker API.

```python title="Example app that uses Dynaconf to configure itself" linenums="1"
## main.py
import logging
from settings import LOGGING_SETTINGS, FAKERAPI_SETTINGS
import httpx

## Initialize a logger
log = logging.getLogger(__name__)

if __name__ == "__main__":
    ## Set the log level from the environment. If no LOG_LEVEL/DYNACONF_LOG_LEVEL is detected,
    #  default to "INFO"
    logging.basicConfig(level=LOGGING_SETTINGS.get("LOG_LEVEL", default="INFO"))

    ## Build the request URL from your settings.
    #  Note that I'm omitting 'default=' from the .get(). This means if the
    #  value isn't found in the environment or TOML settings files, the value
    #  will be None.
    url: str = f"{FAKERAPI_SETTINGS.get('FAKERAPI_BASE_URL')}/{FAKERAPI_SETTINGS.get('FAKERAPI_ENDPOINT')}"
    params = {"_quantity": FAKERAPI_SETTINGS.get("FAKERAPI_QUANTITY")}

    req = httpx.Request(method="GET", url=url, params=params)

    ## Send a request to https://fakerapi.it/api/v2/books?_quantity=3
    #  The base URL, endpoint, and _quantity param are loaded with Dynaconf
    res = httpx.send(req)
```
