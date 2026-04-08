---
tags:
    - python
    - stdlib
    - imports
---
# Package imports

When developing Python packages/modules, you will often want to break your functions into multiple scripts and sub-modules. You will use the `__init__.py` files throughout the package to import functionality from the `.py` script files you write.

Over time, as the module grows, certain methods of importing functions & objects from the module's packages will cause slowdowns and errors. Python has an [`__all__`](https://realpython.com/python-all-attribute/) [dunder method](https://realpython.com/python-magic-methods/) to control what is exported from a `.py` file. Adding defined functions, variables, and objects to the `__all__` list for a package allows you to write a simple `from .script_name import *` in the module's `__init__.py`.

## Example package

The following is an example of a Python module. Pretend you're building an app, and you created a `packages/` directory in the repository root. Each directory in `packages/` represents a Python package, an isolated collection of modules which contain `.py` scripts with functionality you want to import into the rest of your app.

In `packages/example/`, you are writing "helper" functions for operations like path and string manipulation.

```text title="example package layout"
example/
├── __init__.py
├── io
│   ├── __init__.py
│   └── pathio.py
└── str_ops
    ├── __init__.py
    └── _manipulate.py
```

Each `__init__.py` imports the `__all__` list from the associated `.py` file. For example, the `example/io/__init__.py` file's contents are:

```python title="example/io/__init__.py" linenums="1"
## Import everything from pathio's __all__
from .pathio import *

```

### example/io/pathio.py

In `example/io/pathio.py`, there are functions defined and a variable called `__all__`, which is a list of strings matching functions and/or variables in the `pathio.py` file:

```python title="example/io/pathio.py" linenums="1"
from pathlib import Path
import typing as t

## Export specific functions from the app
__all__ = ["return_path_as_str", "path_exists", "expand_path"]

## This variable is not in __all__, and won't be exported
example_var: str = "I won't be exported!"


def return_path_as_str(path: Path) -> str:
    """Return a Path object as a string."""
    return str(expand_path(path))


def path_exists(path: t.Union[str, Path]) -> bool:
    """Return True if path exists, else return False."""
    _path = expand_path(path)

    return _path.exists()


def expand_path(path: t.Union[str, Path]) -> Path:
    """Expand a Path to its absolute path."""
    return Path(str(path)).expanduser() if "~" in str(path) else Path(str(path))


## Function is not in __all__, and won't be exported
def example_function() -> None:
    """Example function that is not explicitly exported."""
    print("I am not exported!")
```

### Importing the example.io.pathio module

Only the functions/variables defined in `__all__` will be available with `from example.io import pathio`. For example:

```python title="Script that imports the example io.pathio module" linenums="1"
## Import the pathio module. Now, anything in __all__ from pathio is availalbe.
from example.io import pathio

## Use the io.pathio.path_exists() function to test if a path exists
pathio.path_exists("example/path")

## The example_var was not added to __all__, so it is not available
print(pathio.example_var)
```

### example/str_ops/

The same is true for `example.str_ops`, which imports the `_manipulate.py`'s functions with `__all__`.

```python title="example/str_ops/_manipulate.py" linenums="1"
__all__ = ["to_uppercase", "to_lowercase", "to_titlecase", "remove_word_from_str", "example_var"]

example_var: str = "I will be exported!"

def to_uppercase(_str: str) -> str:
    """Return uppercased string."""
    return _str.upper()

def to_lowercase(_str: str) -> str:
    """Return a lowercased string."""
    return _str.lower()

def to_titlecase(_str: str) -> str:
    """Return Title-Cased string."""
    return _str.title()

def remove_word_from_str(_str: str, remove_word: str) -> str:
    """Remove instances of a substring by replacing with ''."""
    return _str.replace(remove_word, "")
```

This module exports the `example_var`, unlike `example.io.pathio`'s `example_var`.

### Importing the example.str_ops module

The `example.str_ops.__init__.py` file imports everything from _manipulate.py:

```python title="example/str_ops/__init__.py" linenums="1"
from ._manipulate import *
```

This makes the `to_uppercase`, `to_lowercase`, `to_titlecase`, `remove_word_from_str`, functions are available, as well as the `example_var` variable:

```python title="Script that imports the example str_ops module" linenums="1"
## Import the str_ops module. Now, anything in __all__ from str_ops is availalbe.
from example import str_ops

## Use the str_ops.to_uppercase() function to uppercase a string
uppercased: str = str_ops.to_uppercase("uppercased string") # becomes "UPPERCASED STRING"

## The example_var was added to __all__, so it is available
print(str_ops.example_var) # Prints "I will be exported!"

```

## Summary

By adding an `__all__` list variable to your Python module scripts, you can control what is exported. This way, you can have private variables/functions accessible only from within the `.py` script file, and public/exported objects that are available when you import the module in another script.

Using an `__all__` list also simplifies your imports in `__init__.py` files. You can simply use `from .script_name import *`, which will only import what's listed in that file's `__all__`.
