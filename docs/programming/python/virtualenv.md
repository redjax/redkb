# Use virtualenv to manage dependencies

!!! ToC

    Jump right to a section:

    - [Virtualenv commands cheat-sheet](#virtualenv-cheat-sheet)
    - [What is virtualenv?](#what-is-virtualenv)
        - [What problem does virtualenv solve?](#what-problem-does-virtualenv-solve)
    - [Importing/exporting virtualenv pip requirements](#exportingimporting-requirements)
    - [Common virtualenv troubleshooting](#common-virtualenv-troubleshooting)
    - [Alternatives to virtualenv](#alternatives-to-virtualenv)

## virtualenv cheat sheet

| Command                              | Description                                | Notes                                                                                                                                                                                                                                                          |
| ------------------------------------ | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `virtualenv .venv`                   | Create a new virtual environment           | This command creates a new directory called `.venv/` at the path where you ran the command.                                                                                                                                                                    |
| (Windows) `.\.venv\Scripts\activate` | Activate a virtual environment on Windows. | Your shell should change to show `(.venv)`, indicating you are in a virtual environment                                                                                                                                                                        |
| (Linux/Mac) `./venv/bin/activate`    | Activate a virtual environment on Linux.   | Your shell should change to show `(.venv)`, indicating you are in a virtual environment                                                                                                                                                                        |
| `deactivate`                         | Exit/deactivate a virtual environment.     | You can also simply close your shell session, which exists the environment. This command only works once a virtual environment is activated; `deactivate` will give an error saying the command is not found if you do not have an active virtual environment. |

## What is virtualenv?

[RealPython: Virtualenv Primer](https://realpython.com/python-virtual-environments-a-primer/)

`virtualenv` is a tool for creating virtual Python environments. The `virtualenv` tool has been part of the base Python install since version `These environments are stored in a directory, usually `./.venv`, and can be "activated" when you are developing a Python project. Virtual environments can also be used as Jupyter kernels if you install the `ipykernel` package.

!!! warning

    If you ever see see an error saying the `virtualenv` command cannot be found (or something along those lines), simply install `virtualenv` with:

    ```shell title="Install virtaulenv"
    $ pip install virtualenv
    ```

### What problem does virtualenv solve?

`virtualenv` helps developers avoid ["dependency hell"](https://en.wikipedia.org/wiki/Dependency_hell). Without `virtualenv`, when you insall a package with `pip`, it is installed "globally." This becomes an issue when 2 different Python projects use the same dependency, but different versions of that dependency. This leads to a "broken environment," where the only fix is to essentially uninstall *all* dependencies and start from scratch.

With `virtualenv`, you start each project by running `$ virtualenv .venv`, which will create a directory called `.venv/` at the path where you ran the command (i.e. inside of a Python project directory).

!!!note

    `.venv/` is the convention, but you can name this directory whatever you want. If you run `virtualenv` using a different path, like `virtualenv VirtualEnvironment` (which would create a directory called `VirtualEnvironment/` at the local path), make sure you use that name throughout this guide where you see `.venv`.

Once a virtual environment is created, you need to "activate" it. Activating a virtual environment will isolate your current shell/session from the global Python, allowing you to install dependencies specific to the current Python project without interfering with the global Python state.

Activating a virtual environment is as simple as:

- (on Windows): `$ ./.venv/Scripts/activate`
- (on Linux): `$ ./.venv/bin/activate`

After activating an environment, your shell will change to indicate that you are within a virtual environment. Example:

```shell title="activating virtualenv"
## Before .venv activation, using the global Python. Depdendency will
#  be installed to the global Python environment
$ pip install pandas

## Activate the virtualenv
$ ./.venv/Scripts/activate

## The shell will change to indicate you're in a venv. The "(.venv)" below
#  indicates a virtual environment has been activated. The pip install command
#  installs the dependency within the virtual environment
(.venv) $ pip install pandas
```

This method of "dependency isolation" ensures a clean environment for each Python project you start, and keeps the "system"/global Python version clean of dependency errors.

## Exporting/importing requirements

Once a virtual environment is activated, commands like `pip` will run much the same as they do without a virtual environment, but the outputs will be contained to the `.venv` directory in the project you ran the commands from.

To export `pip` dependencies:

```shell title="Export pip requirements"
## Make sure you've activated your virtual environment first
$ .\\venv\\Scripts\\activate  # Windows
$ ./venv/bin/activate  # Linux/Mac

## Export pip requirements
(.venv) $ pip freeze > requirements.txt

```

To import/install `pip` dependencies from an existing `requirements.txt` file:

```shell title="Import pip requirements"
## Make sure you've activated your virtual environment first
$ .\\venv\\Scripts\\activate  # Windows
$ ./venv/bin/activate  # Linux/Mac

## Install dependencies from a requirements.txt file
(.venv) $ pip install -r requirements.txt

```

## Common virtualenv troubleshooting

!!! TODO

    - [ ] How to recreate a `.venv` environment
    - [ ] Fix issue of virtual environment not showing in Jupyter notebooks

## Alternatives to virtualenv

!!! TODO

    - [ ] Writeup of common pain points with `virtualenv`
        - [ ] Detail limitations of `virtualenv`
        - [ ] Detail the issue of pinning dependencies/compatibility matrices
    - [ ] Brief writeup for `poetry`
    - [ ] Brief writeup for `pdm`
