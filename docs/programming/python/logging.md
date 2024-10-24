---
tags:
    - python
    - stdlib
    - logging
    - configuration
---

# Logging

The Python [`logging`](https://docs.python.org/3/library/logging.html) module is a powerful, highly configurable logger for applications. The downside to `logging` is that it can be a little difficult to wrap your head around at first, and there are [many, many, *many* ways to configure it](https://docs.python.org/3/library/logging.config.html).

I have settled on using [`logging.config.dictConfig`]() to configure my logging, and that is how my notes/code are written.

## Configuring logging module

The `logging` module can be configured a number of ways, most notably with `basicConfig()`, but my personal favorite is with `dictConfig()`, which lets you pre-define your entire applications' logging (all current and potential future loggers) in a Python `dict`. No need to import handlers, formatters, and other miscellaneous classes from the `logging` module; with `dictConfig()`, everything is a string or integer!

!!! Shameless-Plug

    I wrote a module, [`red-logging`](https://github.com/redjax/red-logging) to aid with `logging` boilerplate. This module is specific to my own needs and uses, and may not be suitable for you or your project(s), but can serve as a helpful reference for some patterns.

    `red-logging` does not import any dependencies, it simply organizes some of `logging`'s functionality into classes, context managers, and functions.

### Configure with basicConfig()

The simplest, quickest way to configure Python's `logging` module is by using the `basicConfig()` function. As with other methods of initializing `logging`, you only need to call this once, at your program's entrypoint (i.e. at the top of a `if __name__ == "__main__"` statement, or in a `__main__.py` file).

```python title="Example of configuring logging with basicConfig()" linenums="1"
logging.basicConfig(
    ## You can use logging.LEVEL or an uppercase string
    level="INFO",
    ## Configure the log message string's format
    format="%(asctime)s | [%(levelname)s] | (%(name)s) > %(module)s.%(funcName)s:%(lineno)s |> %(message)s",
    ## Configure the format for timestamps/datetimes in log messages (i.e. the %(asctime)s value
    datefmt="%Y-%m-%dT%H:%M:%S"
)
```

#### setup_logging() function

I use a function in most of my apps called `setup_logging()` to configure logging with `basicConfig()` (if I'm not using `dictConfig()`). The function accepts a level, format, and datefmt, as well as a list of `silence_loggers`, which are string names of 3rd party modules to "silence" by setting their log level to `WARNING`. When using a `DEBUG` log level, you will also see debug messages for any 3rd party dependencies in your package (i.e. `SQLAlchemy`, `httpx`, etc); the `silence_loggers` list will stop these debug messages.

```python title="setup_logging()" linenums="1"
def setup_logging(
    level: str = "INFO",
    format: str = "%(asctime)s | [%(levelname)s] | (%(name)s) > %(module)s.%(funcName)s:%(lineno)s |> %(message)s",
    datefmt: str = "%Y-%m-%d_%H-%M-%S",
    silence_loggers: list[str] = [
        "httpx",
        "hishel",
        "httpcore",
        "urllib3",
        "sqlalchemy",
    ],
):
    logging.basicConfig(level=level, format=format, datefmt=datefmt)

    if silence_loggers:
        for _logger in silence_loggers:
            logging.getLogger(_logger).setLevel("WARNING")

```

### Configure with dictConfig()

You can use a custom `dict` to configure an entire app's logging all in one place.

!!! warning

    When using `logging.config.dictConfig(logging_config_dict)`, be careful to only call `dictConfig()` once per execution. Calling this method multiple times can lead to instability in your logging as the logging config `dict`s overwrite each other.

    `dictConfig()` should be called very early in your program's execution. You can put it in your root `__init__.py` file, or very early in the `main.py` file (or whatever entrypoint you run). If your project has multiple entrypoints, you can put `dictConfig()` below your `if __name__ == "__main__"`, but imports may fire log messages that do not get caught before the logger is configured, or they may be missed entirely.

    Finally, you can use a `setup_logging()` function, which you can store in a module and import into whatever entrypoint script you target. This is a configurable and flexible way to manage logging.

#### dictConfig keys

The following options are available as `dict` keys for your logging config `dict`.

| Key                      | Description                                                                                                                                                                                                                                                                                                        |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| version                  | an integer indicating the schema version that is being used. If the logging configuration schema changes in the future, the `version` key will be used to indicate which version of the schema the `dictConfig` is using. This allows the `dictConfig` function to handle both current and future schema versions. |
| formatters               | a dictionary with each key being a formatter id and its value describing how to configure the corresponding [Formatter](https://docs.python.org/3/library/logging.html#logging.Formatter) instance.                                                                                                                |
| filters                  | a dictionary with each key being a filter id and its value describing how to configure the corresponding [Filter](https://docs.python.org/3/library/logging.html#filter-objects) instance.                                                                                                                         |
| handlers                 | a dictionary with each key being a handler id and its value describing how to configure the corresponding [Handler](https://docs.python.org/3/library/logging.html#logging.Handler) instance. All other keys are passed through as keyword arguments to the handler’s constructor.                                 |
| loggers                  | a dictionary with each key being a logger name and its value describing how to configure the corresponding Logger instance.                                                                                                                                                                                        |
| root                     | the configuration for the root logger. It’s processed like any other logger, except that the propagate setting is not applicable.                                                                                                                                                                                  |
| incremental              | a boolean indicating whether the configuration specified in the dictionary should be merged with any existing configuration, or should replace entirely. Its default value is `False`, which means that the specified configuration replaces any existing configuration.                                           |
| disable_existing_loggers | a boolean indicating whether any non-root loggers that currently exist should be disabled. If absent, this parameter defaults to `True`. Its value is ignored when incremental is `True`.                                                                                                                          |

#### Logging config dict template

This `logging_config_template` `dict` can serve as a base/root for your project. Copy/paste the code and modify it to your needs, adding formatters, handlers, etc.

```python title="logging_config dict template" linenums="1"
logging_config_template: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "propagate": True,
    "root": {},
    "formatters": {},
    "handlers": {},
    "loggers": {},
}

```

#### Example logging config dict

This is an example of a fully configured `logging` config dict. It includes a couple of console handlers, one which filters messages to only show `CRITICAL` and above, a custom format, and a number of loggers.

!!! note

    You only need to configure the root (`""`) logger once; the configuration below configures te root logger in the `"root"` dictionary key, as well as in `"loggers": {"": {}}`. In a real logging configuration dict, you would only do one of these. I personally prefer putting my configuration in the top-level `"root"` key.

```python title="Example logging config dict" linenums="1"
## Root logger config. Use with .dictConfig(log_config)
log_config: dict = {
    "version":1,
    ## When True, clears all logging configuration.
    #  Best used only on the root logger
    "disable_existing_loggers": True,
    ## Configure the root logger
    "root":{
	    ## Set handlers
        "handlers" : ["console"],
        ## Set log level string
        "level": "DEBUG"
    },
    ## Configure handlers
    "handlers":{
	    ## Default console logger
        "console":{
	        ## Use stdout stream
	        "stream": "ext://sys.stdout",
	        ## Name of formatter
            "formatter": "std_out",
            ## The logging module to subclass
            "class": "logging.StreamHandler",
            ## Log level for this logger
            "level": "DEBUG"
        },
        ## Only log CRITICAL messages with with `.getLogger("cli")`
        "cli": {
	        "console": {
	            "level": "CRITICAL",
	            "class": "logging.StreamHandler",
	            "formatter": "consoleFormatter",
	        },
        }
    },
    ## Configure formatters for log messages
    "formatters": {
	    ## Set formatting for std_out formatter messages & dates
        "std_out": {
            "format": "%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : (Process Details : (%(process)d, %(processName)s), Thread Details : (%(thread)d, %(threadName)s))\nLog : %(message)s",
            "datefmt":"%d-%m-%Y %I:%M:%S"
        }
    },
    ## (Optional) pre-configure logger namespaces.
    #  Example: you have a module named `requests.py`; define
    #  a "requests" logger below, and when `requests.py` uses
    #  `logging.getLogger(__name__)`, it will use the "requests"
    #  logger config.
    #  This can also be used to override module loggers, like `uvicorn`
    "loggers": {
	    "": {
		    "handlers": ["console"],
		    ## Hide all but warning messages on root logger
		    "level": "WARNING",
		    "propagate": False
	    },
	    ## if __name__ == '__main__'
	    '__main__': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        ## Suppress all log messages.
        #  Usage: logging.getLogger("silent")
        "silent": {
	        "level:" "NOTSET"
        },
	    ## Disable logs from the requests module by setting to WARNING
	    "requests": {
		    ## Set to warning to disable logging of 3rd party modules
		    "level": "WARNING"
	    },
	    ## Set logging for a module named my_module in advance
	    "my_module": {
		    "level": "INFO"
	    }
    },
}

```

## Log Levels

| Value      | Int Level | Description                                                                                                                                                                                                                                                                                   |
| ---------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `NOTSET`   | `0`       | It is the lowest level in the logging hierarchy and is used to indicate that no specific logging level has been set for a logger or a handler (more on handler later on in the article). It is essentially a placeholder level that is used when the logging level is not explicitly defined. |
| `DEBUG`    | `10`      | It is used for low-level debugging messages that provide detailed information about the code’s behavior. These messages are typically used during development and are not required in production.                                                                                             |
| `INFO`     | `20`      | It is used to log informational messages about the program’s behavior. These messages can be used to track the program’s progress or to provide context about the user.                                                                                                                       |
| `WARNING`  | `30`      | It is used to log messages that indicate potential issues or unexpected behavior in the program. These messages do not necessarily indicate an error but are useful for diagnosing problems.                                                                                                  |
| `ERROR`    | `40`      | It is used to log messages that indicate an error has occurred in the program. These messages can be used to identify and diagnose problems in the code.                                                                                                                                      |
| `CRITICAL` | `50`      | It is used to log messages that indicate a critical error has occurred that prevents the program from functioning correctly. These messages should be used sparingly and only when necessary.                                                                                                 |

### Creating a custom log level

Example: `VERBOSE`

```python title="Example VERBOSE custom log level" linenums="1"
import logging

# Define the custom log level
VERBOSE = 15
logging.VERBOSE = VERBOSE
logging.addLevelName(logging.VERBOSE, 'VERBOSE')

# Set up basic logging configuration for the root logger
logging.basicConfig(level=logging.DEBUG)


# Define a custom logging method for the new level
def verbose(self, message, *args, **kwargs):
    if self.isEnabledFor(logging.VERBOSE):
        self._log(logging.VERBOSE, message, args, **kwargs)


# Add the custom logging method to the logger class
logging.Logger.verbose = verbose

# Create a logger instance
logger = logging.getLogger()

# Log a message using the custom level and method
logger.verbose("This is a verbose message")

```

## Links

| Title                                               | URL                                                                                                                                                                |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Python docs: `logging`                              | [https://docs.python.org/3/library/logging.html](https://docs.python.org/3/library/logging.html)                                                                   |
| Python docs: `logging.config`                       | [https://docs.python.org/3/library/logging.config.html](https://docs.python.org/3/library/logging.config.html)                                                     |
| Python docs: `logging.config.dictConfig`            | [https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig](https://docs.python.org/3/library/logging.config.html#logging.config.dictConfig) |
| Python docs: `LogRecord` attributes (formatting)    | [https://docs.python.org/3/library/logging.html#logrecord-attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)                         |
| Python docs: `time.strftime` (timestamp formatting) | [https://docs.python.org/3/library/time.html#time.strftime](https://docs.python.org/3/library/time.html#time.strftime)                                             |
| Python docs: `logging` `Handler` objects            | [https://docs.python.org/3/library/logging.html#handler-objects](https://docs.python.org/3/library/logging.html#handler-objects)                                   |
