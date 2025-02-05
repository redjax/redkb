---
tags:
    - python
    - utilities
    - cyclopts
---

# Call a cyclopts CLI from another Python script

It is possible to call your `cyclopts` app from other Python scripts. This can be useful for calling a specific set of arguments in a repeatable way. As an example, we'll create a Python script that prompts a user for their name, then calls the `say_hello()` command of the `cyclopts` app we built above.

In the root of the project folder, i.e. where your `pyproject.toml` or `requirements.txt` are, above the `src/` path, create a file `say_hi.py`. This script will import the `my_pymodule.cli` module, prompt the user for a name, then call the `say_hello()` command of the CLI app, all within the Python script file.

```python title="say_hi.py" linenums="1"
from my_pymodule import cli

if __name__ == "__main__":
    name: str = input("What is your name? ")
    command: list[str] = ["hello", name]

    cli.app.meta(tokens=command)

```

Now when you run `python say_hi.py`, the script will create a list of commands to pass as tokens to the meta app. If you want to enable debugging, you can just add `--debug` to the commands list:

```python title="Add debugging to command list" linenums="1"
...

command: list[str] = [..., "--debug"]

...

```
