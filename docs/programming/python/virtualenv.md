---
tags:
    - python
    - virtualenv
---


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

`virtualenv` is a tool for creating virtual Python environments. The `virtualenv` tool is sometimes installed with the "system" Python, but you may need to install it yourself (see the warning below).

These virtual environments are stored in a directory, usually `./.venv`, and can be "activated" when you are developing a Python project. Virtual environments can also be used as Jupyter kernels if you install the `ipykernel` package.

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

### Recreate .venv

Sometimes you find yourself with a `.venv` that's in disrepair, and you might want to start from scratch and recreate it. This is as simple as removing the `.venv` directory with `rm -r .venv` (you may get warnings about write-protected files, in which case you will need to use `sudo` to remove the `.venv`).

After removing the `.venv`, you can recreate it with `virtualenv .venv`. Make sure to activate the new virtualenv and reinstall your dependencies with `pip install -r requirements.txt`

### Fix virtual environment not showing in Jupyter notebooks

This is almost always because your virtualenv is missing the `ipykernel` package. This package is required for a virtualenv to be detectable by Jupyter notebooks.

Simply add the package: `pip install ipykernel`.

## Alternatives to virtualenv

There are other ways to manage a virtual environment for Python. Most people start out using `virtualenv`, and some people never find a need to replace `virtualenv` with another tool.

If you want to separate your development dependencies from production, or "manage" your Python project including building & publishing your code, running scripts/tasks, and resolving dependencies more quickly/reliably than with `pip`, you can use a Python project manager.

Python's package management ecosystem is much older than other languages like Node's `npm`, and as a result package management came later and was not "figured out" by the time Python developed `pip`. The `pip` utility has served a very important role for many years, and there are those who would argue you never need anything more than `pip + virtualenv`. It is true that you can be just as effective with `pip + virtualenv` as any of the project managers below, but there are some conveniences to using a project manager, such as installing non-Python dependencies with `conda` for scientific/ML/AI development.

This section will not go into much detail on each package manager. Other sections of this KB site may expand more on how to use each of these. This page serves to simply list alternatives to `virtualenv`.

Alternatives to `pip/virtualenv`:

| tool                                                                                                                                                                                         | description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`pdm`](https://pdm-project.org)                                                                                                                                                             | The "Python Dependency Manager" is one of the best all-around tools on this list. It can handle complex dependency resolution (i.e. `pytorch` installation), project scripts (something `poetry` needs a plugin for, and that is completely missing from `virtualenv`), and can build & publish your code to `pypi`.                                                                                                                                                                                                                                                                                                    |
| [`uv`](https://astral.sh/uv)                                                                                                                                                                 | A new(ew) Python project manage, `uv` is built with Rust and boasts the fastest dependency resolution of any package manager I've tried. What might take 30 seconds to install with `pdm` (a perfectly acceptable dependency resolution/installation time) may take only 2-3 seconds in `uv`. Support for monorepos, building the project, scripts (that function differently from `pdm`, but are still useful), installing Python (you don't even need Python installed to run `uv`!), `venv` management, and more. I am slowly converting most/all of my projects to `uv`, and using it for new projects. It's great! |
| [`poetry`](https://python-poetry.org/)                                                                                                                                                       | A favorite of many in the Python community, the `poetry` tool is another fast, capable project manager. The project does not follow PEP standards, which puts it at odds with some other tools. For example, `poetry` makes heavy modifications to the standard `pyproject.toml` file, and has not expressed interest in following a number of PEPs, which could lead to complicated divergence over time. Scripting is not a first-class feature of `poetry` either, requiring a plugin called `poe-the-poet`.                                                                                                         |
| [`conda`](https://docs.conda.io)                                                                                                                                                             | The package manager for the Anaconda Python distribution, aimed at scientific Python and machine learning/AI development. Conda filled a desperately needed role in the mid-2010s, when it was very difficult to install packages required for machine learning development. The tool continues to see use, but if you are interested in using `conda` for development, you would be better served using something like `mamba`/`micromamba`, or the newer `pixi` tool that uses Conda's repositories but is written in Rust and has many more convenient features.                                                     |
| [`mamba`](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html)/[`micromamba`](https://mamba.readthedocs.io/en/latest/installation/micromamba-installation.html) | `mamba` is a resolver for `conda` packages that significantly speeds up environment resolution time. `conda` is great, but is very, very slow. The `mamba` solver makes `conda` far more useable. `micromamba` is a statically linked, self-contained tool. It supports all of the major features of `mamba`, but instead of installing a whole package, you simply place the `micromamba` binary somewhere in your `PATH`. `micromamba` is faster than `conda` and `mamba`, and will serve most use cases.                                                                                                             |
| [`pixi`](https://prefix.dev/)                                                                                                                                                                | A newer project manager, `pixi` uses the `conda` package sources (meaning any package you can install with `conda`/`mamba` can be installed with `pixi`). The tool is written in Rust and is extremely fast. It also has a number of very useful features that put it more in line with `pdm` or `uv` than `conda`. If you are interested in using `conda` for your development, I highly recommend trying `pixi` over the other options.                                                                                                                                                                               |
