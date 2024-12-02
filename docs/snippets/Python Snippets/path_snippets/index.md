---
tags:
    - python
    - snippets
---

# Path module snippets

Code snippets for the `pathlib.Path` stdlib module.

## Read files embedded in source code

If you have files like `.json` or `.txt` embedded in your app, i.e. for a module that reads from this file where both the `.json`/`.txt` file and the `.py` file that reads them are in the same subdirectory in your Python app, you need to append the `.py` file's path to the system path. This lets the Python file open the text file using `with open("./example.json", "r") as f:`.

```python title="Add module path to sys.path" linenums="1"
from pathlib import Path
import sys

# Resolve the path to the directory containing the current file
module_path = Path(__file__).parent.resolve()

file_path = module_path / "example.json"

```

### Example: read json file

As an example, say you have a package named `my_pymodule`, with code structured like this:

```plaintext title="my_pymodule package" linenums="1"
src/
  my_pymodule/
    json_reader/
      __init__.py
      reader.py
      values.json
    __init__.py
    main.py
    
```

From `reader.py`, you want to load `./values.json` and return to a function that calls the `reader.py` file, i.e. `main.py`.

```python title="src/my_pymodule/json_reader/reader.py" linenums="1"
from pathlib import Path

# Resolve the path to the directory containing the current file
module_path = Path(__file__).parent.resolve()

## Set path to values.json
VALUES_JSON_FILE = module_path / "values.json"


def read_values() -> dict:
    ## Read the JSON file
    with open(VALUES_JSON_FILE, 'r', encoding='utf-8') as f:
        data = f.read()

    return data

```

Then in `src/my_pymodule/main.py`, import the `read_values()` function. Calling `main.py` will set your path to wherever you called the script from, but `read_values()` will always open the `example.json` file that exists in the same path as the `reader.py` module:

```python title="src/my_pymodule/main.py" linenums="1"
from my_pymodule.json_reader import read_values


def main():
    ## Read values from the embedded values.json file
    values: dict = read_values()
    print(f"Values: {values}")
    

if __name__ == "__main__":
    main()

```

## Append module's 'grandparent' path

Appends the path `../..` to Python's path. Add more `.parent` for more deeply nested modules.

This is useful if you have a path like `sandbox/` at your root. In the sandbox apps you build in this directory, whatever your entrypoint is (i.e. `sandbox/ex_app/main.py`), add the code below to fix paths when running sandbox apps from the directory above `sandbox/`.

```python title="Append path to root" linenums="1"
import sys
import os

sys.path.append(str(Path(__file__).resolve().parent.parent))

```