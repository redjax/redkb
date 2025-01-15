---
tags:
    - python
    - utilities
    - cyclopts
---

# Building a CLI app with cyclopts

!!! note

    This guide uses `my_pymodule` as the name of the example package/app that a `cyclopts` CLI will be added to. Wherever you see `my_pymodule` in this guide, replace with the name of the Python app you are adding a CLI to.

    As with every other guide on this site, I am writing about the way I personally use `cyclopts`. It may not suit your needs, but I hope it helps you learn the concepts.

When I'm adding a CLI to one of my apps, I like to create a directory inside my app's source named `cli/`, and a file beneath that `main.py`, which represents my CLI's entrypoint. In my app's `__main__.py`, I call the `cyclopts` app, parsing arguments when the app is called.

For example, if I'm working on a Python app named `my_pymodule`, I would create the following file structure:

```plaintext title="Example CLI app location in a Python app" linenums="1"
pyproject.toml  # Project root with a pyproject.toml or requirements.txt file
src/  # Code exists in a src directory
  my_pymodule/
    cli/  # The cyclopts app
      __init__.py
      main.py  # The CLI's entrypoint
      commands.py  # Import commands from a separate file for easier development
    __init__.py
    __main__.py  # Import the cli app here
    main.py  # Regular app entrypoint

```

In my `src/my_pymodule/cli/main.py`, I declare a `cyclopts` app and add a command to accept a user's name and print "hello, {name}"

```python title="Create cyclopts app" linenums="1"
from cyclopts import App

## Initialize the app. Give the app a name, and a help message for --help
app = App(name="demo", help="Cyclopts demo app.")


@app.command(name="hello")
def say_hello(name: str = "world"):
    """Say hello to a user.

    Description:
        Says hello to a user, or 'world' if no user is given. This docstring becomes the command's help messsage!
    Params:
        name (str): Name of user to say hello to.

    """
    print(f"Hello, {name}!")


if __name__ == "__main__":
    ## When this script is called directly, run the app
    app()

```

This file become's the main entrypoint to the `cyclopts` app. As you add commands and functionality to the CLI app, you will import code from other modules and "mount" them in the main app.

## Cyclopts Meta app

Running the `cyclopts` app with `app()` calls the app directly, but you can also call a `cyltops` ["Meta app"](https://cyclopts.readthedocs.io/en/latest/meta_app.html). Calling the app this way gives you more control over `cyclopts`'s launch process. This allows you to do things like setup logging (or add a `--debug` flag that sets logging level to `DEBUG` when present), run functions before startup, and control tokens (inputs) that are passed to the app.

The setup for using a meta app is simple; after adding the code below, anywhere you would normally call `app()`, call `app.meta()` instead. The code imports `Parameter` from `cyclopts`, and the stdlib `typing` library for accessing the `Annotated` class. The new meta app is created in `@app.meta.default`, and the function `cli_app_launcher` now calls the app. You can name this function anything you want.

When adding function parameters to `cli_app_launcher`, they become CLI args.

```python title="cyclopts meta app" linenums="1"
from cyclopts import App, Parameter
import typing as t

## Initialize the app. Give the app a name, and a help message for --help
app = App(name="demo", help="Cyclopts demo app.")
## Allow global flags like --debug
app.meta.group_parameters = Group("Session Parameters", sort_key=0)


@app.command(name="hello")
def say_hello(name: str = "world"):
    """Say hello to a user.

    Description:
        Says hello to a user, or 'world' if no user is given. This docstring becomes the command's help messsage!
    Params:
        name (str): Name of user to say hello to.

    """
    print(f"Hello, {name}!")


## Add a meta launcher to the app. Call with app.meta()
@app.meta.default
def cli_app_launcher(
    *tokens: t.Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
):
    ## Uncomment to print tokens for debugging
    # print(f"Tokens: {tokens}")

    ## Call the app, passing tokens as arguments
    app(tokens)


if __name__ == "__main__":
    ## Call the app's meta launcher
    app.meta()

```

### Setup logging with meta app

Launching the `cyclopts` app using a "meta" launcher provides control over the CLI app's startup. As an example, the `cli_app_launcher` command below configures logging based on the presence of a `-d/--debug` flag. If present, the logging level for the [`loguru`]() library is set to `DEBUG`.

```python title="cyclopts meta logging config" linenums="1"
from cyclopts import App, Parameter
from loguru import logger as log
import typing as t
import sys

app = App(name="demo", help="Cyclopts demo app.")
app.meta.group_parameters = Group("Session Parameters", sort_key=0)


@app.meta.default
def cli_launcher(
    *tokens: t.Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
    debug: t.Annotated[
        bool,
        Parameter(
            name=["-d", "--debug"], show_default=True, help="Enable debug logging."
        ),
    ] = False,
    file_log: t.Annotated[
        bool,
        Parameter(
            name=["-l", "--log-file"], show_default=True, help="Enable logging to file"
        ),
    ] = False,
):
    ## Initialize Loguru logger
    log.remove(0)

    ## If --debug flag was passed, set logging to `DEBUG` and more verbose log format
    if debug:
        log.add(
            sys.stderr,
            format="{time:YYYY-MM-DD HH:mm:ss} | [{level}] | {name}.{function}:{line} | > {message}",
            level="DEBUG",
        )
    
    ## If --debug flag not passed, set logging to `INFO` and a shorter log message format
    else:
    
        log.add(
            sys.stderr,
            format="{time:YYYY-MM-DD HH:mm:ss} [{level}] : {message}",
            level="INFO",
        )

    ## Call the cyclopts app with user's inputs
    app(tokens)

```

## Adding commands and sub-apps

So far, we have added a `say_hello()` function to the app. When `my_pymodule hello <name>` is called, the CLI will say hello to the user. The `hello` arg here is a "command."

You can make your CLI modular by putting commands into other `.py` files. You can also create multiple `cyclopts.App` instances, and mount them in the main app. This allows for creating complex but maintainable commands.

### Create sub-app/command

To start, let's add some more "top level" commands like the `hello` command. Let's create one that adds 2 numbers together. We will put this code into `cli/commands.py`, and import into `cli/main.py`. We will create a new `cyclopts` app for this called `math`, and create a command beneath it for adding numbers. We will import this sub-app into the `cli/main.py` file and mount it in our `cyclopts` app.

I will also add `DEBUG` logging messages so you can see how the `--debug` param works.

```python title="cli/commands.py" linenums="1"
from cyclopts import App, Parameter
import typing as t
from loguru import logger as log


math_subapp = App(name="math", help="Math commands.")


@math_subapp.command(name="add")
def add_nums(a: int = 0, b: int = 0):
    """Add 2 numbers and print the sum.
    
    Params:
        a (int): First number to add.
        b (int): Second number to add.
    """
    log.debug(f"a={a}, b={b}")

    ## Add the numbers
    sum: int = a + b

    if sum == 0:
        print("Nothing to add!")
    else:
        print(f"{a} + {b} = {sum}")

```

Then, in the `cli/main.py` file, I will import the `math_subapp` command, which will make `my_pymodule math add <a> <b>` available.

```python title="cli/main.py" linenums="1"
from cyclopts import App, Parameter, Group
import typing as t
from loguru import logger as log

## Import the math subapp
from my_pymodule.commands import math_subapp


## Initialize the app. Give the app a name, and a help message for --help
app = App(name="demo", help="Cyclopts demo app.")
## Allow global flags like --debug
app.meta.group_parameters = Group("Session Parameters", sort_key=0)

## Mount the math subcommand
app.command(math_subapp)


@app.command(name="hello")
def say_hello(name: str = "world"):
    """Say hello to a user.

    Description:
        Says hello to a user, or 'world' if no user is given. This docstring becomes the command's help messsage!
    Params:
        name (str): Name of user to say hello to.

    """
    print(f"Hello, {name}!")


@app.meta.default
def cli_launcher(
    *tokens: t.Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
    debug: t.Annotated[
        bool,
        Parameter(
            name=["-d", "--debug"], show_default=True, help="Enable debug logging."
        ),
    ] = False,
    file_log: t.Annotated[
        bool,
        Parameter(
            name=["-l", "--log-file"], show_default=True, help="Enable logging to file"
        ),
    ] = False,
):
    ## Initialize Loguru logger
    log.remove(0)

    ## If --debug flag was passed, set logging to `DEBUG` and more verbose log format
    if debug:
        log.add(
            sys.stderr,
            format="{time:YYYY-MM-DD HH:mm:ss} | [{level}] | {name}.{function}:{line} | > {message}",
            level="DEBUG",
        )

    ## If --debug flag not passed, set logging to `INFO` and a shorter log message format
    else:
        log.add(
            sys.stderr,
            format="{time:YYYY-MM-DD HH:mm:ss} [{level}] : {message}",
            level="INFO",
        )

    ## Call the cyclopts app with user's inputs
    app(tokens)


if __name__ == "__main__":
    ## Call the app's meta launcher
    app.meta()

```

Now, run `my_pymodule math --help` to see the `add` command, and `my_pymodule math add --help` to see the help message for `add`. Call the command with `my_pymodule math add 1 2` and `my_pymodule math add 1 2 --debug`.

You can nest commands/sub-apps like this to add functionality to your CLI. These are the basics of `cyclopts`. Check the [`cyclopts` documentation]() for more information on building CLIs and TUIs using the package.

## Adding as package entrypoint

When you call your package as a module, i.e. `python -m my_pymodule`, you want to be able to pass args like `math add 1 2`. To do this, import your `cyclopts` app into `src/my_pymodule/cli/__init__.py`, then add the app to `src/my_pymodule/__main__.py`.

```python title="src/my_pymodule/cli/__init__.py"
from .main import app

```

Then set it as your package's entrypoint in `__main__.py`:

```python title="src/my_pymodule/__main__.py" linenums="1"
from my_pymodule import cli

if __name__ == "__main__":
    ## When my_pymodule is called from the CLI, launch the cyclopts app
    cli.app.meta()

```
