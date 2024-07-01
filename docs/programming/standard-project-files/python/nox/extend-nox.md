---
tags:
    - standard-project-files
    - python
    - nox
---

# Extend Nox with importable sessions

You can import extra `nox` sessions from a module/file, moving some code out of the `noxfile.py` for extensibility and making your `nox` sessions more modular.

My preference is to create a directory in the project root called `.nox_ext`. This directory stores package namespaces, the main one being `nox_extensions`. In `.nox_ext/nox_extensions/`, I write custom code and import it in the `__init__.py`. I then have to add the `.nox_ext` directory to my path, and import `nox_extensions` in my `noxfile.py`.

## Adding custom nox extensions

!!! note

    This guide assumes your `nox` extensions directory will be called `.nox_extensions/`. If you want to use a different path while following this guide, just substitute the path you choose wherever you see `.nox_extensions`.

### Make an extensions directory & import it  

Create a directory to store your `nox` extensions. This can be named anything you like, but I call it `.nox_extensions/`. Because this directory path starts with a period, I have to add the path to my script's path.

Adding the `.nox_extensions/` directory to the path includes getting the working directory for the script with: `script_dir: Path = Path(__file__).resolve().parent`, building a `Path` object for the `.nox_ext` path with: `nox_ext_path: Path = script_dir / ".nox_ext"`, and appending it to the Python path with: `sys.path.append(str(nox_ext_path)).`

Once your script is aware of the `.nox_extensions/` directory, you will be able to import modules from it. For example, if you have a module at `.nox_extensions/nox_tests_ext/`, after adding the parent `.nox_extensions` directory to the path, you would be able to import this module with: `from nox_tests_ext import ...`.

You should end up with something like:

```
.nox_ext
└── nox_extensions  ## Importable after .nox_ext is appended to path
    ├── __extensions.py  ## Extra nox sessions
    └── __init__.py  ## Import code from __extensions.py so it's available in nox_extensions.*
```

## Custom module: `nox_extensions`

The `.nox_ext/nox_extensions/` path is my "default" extension module. The code is simple, mostly for demonstration purposes.

In `.nox_ext/nox_extensions/`, create a file called `__extensions.py`. The `__` at the beginning of this path is a technique called "name mangling" (read more: [RealPython: Python Double Underscore](https://realpython.com/python-double-underscore/#double-leading-underscore-in-classes-pythons-name-mangling)). The purpose of name mangling is to make it inaccessible. You can still import mangled code, but it is considered bad practice to import from mangled modules directly.

### Import code from mangled module

To get around this, we will import the code in `__extensions.py` in our `__init__.py`. This makes whatever code we import from `__extensions.py` available at the namespace level. For example, if there is a function called "say_hello()" in `.nox_ext/nox_extensions/__extensions.py`, importing it in `__init__.py` makes it accessible with: `from nox_extensions import say_hello`.

```python title=".nox_ext/nox_extensions/__extensions.py" linenums="1"
import logging
import platform

log = logging.getLogger("noxfile.nox_ext")

import nox

## Get tuple of Python ver ('maj', 'min', 'mic')
PY_VER_TUPLE: tuple[str, str, str] = platform.python_version_tuple()
## Dynamically set Python version
DEFAULT_PYTHON: str = f"{PY_VER_TUPLE[0]}.{PY_VER_TUPLE[1]}"


@nox.session(python=[DEFAULT_PYTHON], name="print-python", tags=["ext", "env"])
def run_print_python_ver(session: nox.Session):
    """Print the Python version found in the Nox session."""
    log.debug(f"Nox Python version: {DEFAULT_PYTHON}")

```

Then, we need to import `run_print_python_ver()` in our `__init__.py` file:

```python title="Import code from .nox_ext/nox_extensions/__extensions.py" linenums="1"
from .__extensions import run_print_python_ver

```

If we wanted to make our `PY_VER_TUPLE` and `DEFAULT_PYTHON` variables accessible in our `nox_extensions` module, we could import them as well:

```python title="Import Python variables" linenums="1"
from .__extensions import PY_VER_TUPLE, DEFAULT_PYTHON

```

### Example: partial `noxfile.py` importing `.nox_extensions`

!!! note

    This example is a partial `noxfile.py` that will not run. To see a full `noxfile.py`, check [the `nox` landing page](./index.md#noxfilepy-base) for a more complete example.

    You can adapt that `noxfile.py` with the examples & instructions below.

```python title="noxfile.py import .nox_extensions" linenums="1"
## noxfile.py
import logging
from pathlib import Path
import sys

import nox

log = logging.getLogger("nox.nox_ext")

## other imports
...

## Add .nox_ext to the path
# Get the current script directory
script_dir: Path = Path(__file__).resolve().parent

# Add the .nox_ext directory to the system path
nox_ext_path: Path = script_dir / ".nox_ext"
sys.path.append(str(nox_ext_path))

## Attempt to import nox_extensions
try:
    from nox_extensions import run_print_python_ver
except Exception as exc:
    msg = Exception(
        f"({type(exc)}) Error importing nox extensions. Check extension path exists."
    )
    log.error(msg)

## More nox code
...

```
