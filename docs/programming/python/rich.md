# Using rich to enhance your console output

The [`rich`](https://github.com/Textualize/rich) package helps make console/terminal output look nicer. It has colorization, animations, and more.

## Details

- [`rich` Github repository](https://github.com/Textualize/rich)
- [`rich` docs](https://rich.readthedocs.io/en/stable/introduction.html)
- [`rich` pypi](https://pypi.org/project/rich/)

## Examples

### Simple CLI spinner context manager

This example uses the `rich.console.Console` and `rich.spinner.Spinner` classes. The first context manager, `get_console()`, yields a `rich.Console()` object, which can be used with the `rich.Spinner()` class to display a spinner on the command line.

```python title="get_console() function" linenums="1"
from contextlib import contextmanager
import typing as t
from rich.console import Console

@contextmanager
def get_console() -> t.Generator[Console, t.Any, None]:
    """Yield a `rich.Console`.

    Usage:
        `with get_console() as console:`

    """
    try:
        console: Console = Console()

        yield console

    except Exception as exc:
        msg = Exception(f"Unhandled exception getting rich Console. Details: {exc}")
        log.error(msg)

        raise exc

```

The `simple_spinner()` context manager yields a `rich.Spinner()` instance. Wrap a function in `with simple_spinner(msg="Some message") as spinner:` to show a spinner while the function executes.

```python title="simple_spinner()" linenums="1"
from contextlib import contextmanager
from rich.spinner import Spinner

@contextmanager
def simple_spinner(text: str = "Processing... \n", animation: str = "dots"):
    if not text:
        text: str = "Processing... \n"
    assert isinstance(text, str), TypeError(
        f"Expected spinner text to be a string. Got type: ({type(text)})"
    )

    if not text.endswith("\n"):
        text += " \n"

    if not animation:
        animation: str = "dots"
    assert isinstance(animation, str), TypeError(
        f"Expected spinner animation to be a string. Got type: ({type(text)})"
    )

    try:
        _spinner = Spinner(animation, text=text)
    except Exception as exc:
        msg = Exception(f"Unhandled exception getting console spinner. Details: {exc}")
        log.error(msg)

        raise exc

    ## Display spinner
    try:
        with get_console() as console:
            with console.status(text, spinner=animation):
                yield console
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception yielding spinner. Continuing without animation. Details: {exc}"
        )
        log.error(msg)

        pass
```

Putting both of these functions in the same file allows you to import just the `simple_spinner` method, which calls `get_console()` for you. You can also get a console using `with get_console() as console:`, and write custom spinner/`rich` logic.

## Usage

```python title="Example CLI spinner" linenums="1"
from some_modules import simple_spinner

with simple_spinner(text="Thinking... "):
    ## Some long-running code/function
    ...

```
