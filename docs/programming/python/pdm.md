---
tags:
    - python
    - pdm
---

# Use PDM to manage your Python projects & dependencies

!!! TODO

    - [x] Write section describing `pdm`
        - [x] What is `pdm`?
        - [x] What problem does `pdm` solve?
    - [x] Write `pdm` cheat sheet
        - [x] Initialize a project
            - [x] Difference between an `application` and a `library`
        - [x] Add/remove dependencies
        - [x] Execute code
        - [x] Add development dependencies
    - [ ] Detail publishing a project to `pypi` with `pdm

!!! TOC

    - [`pdm` cheat sheet](#pdm-cheat-sheet)
    - [What is PDM?](#what-is-pdm)
        - [What problem does PDM solve?](#what-problem-does-pdm-solve)
    - [How to install PDM](#how-to-install-pdm)
    - [What is a "library" vs an "application"](#library-vs-application)

## PDM cheat sheet

| Command                                  | Description                                                                                                | Notes                                                                                                                                                                                                                                                                 |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pdm init`                               | Initialize a new project with `pdm`                                                                        | The `pdm` tool will ask a series of questions, and build an environment based on your responses                                                                                                                                                                       |
| `pdm add <package-name>`                 | Add a Python package to the project's dependencies.                                                        | `pdm` will automatically find all required dependencies and add them to the install command, and will ensure the package installed is compatible with your environment.                                                                                               |
| `pdm add -d <package-name>`              | Add a Python package to the project's `development` dependency group.                                      | Use this for packages that should not be built with your Python package. Useful for things like formatters (`black`, `ruff`, `pyflakes`, etc), testing suites (`pytest`, `pytest-xidst`), automation tools (`nox`, `tox`), etc.                                       |
| `pdm add -G standard <package-name>`     | Add a Python package to the project's `standard` group.                                                    | In this example, `standard` is a custom dependency group. You can use whatever name you want, and users can install the dependencies in this group with `pip install <project-name>[standard]` (or with `pdm`: `pdm add <project-name>[standard]`)                    |
| `pdm remove <package-name>`              | Remove a Python dependency from the project.                                                               | Analagous to `pip uninstall <package-name>`                                                                                                                                                                                                                           |
| `pdm remove -d <package-name>`           | Remove a Python development dependency from the project.                                                   |                                                                                                                                                                                                                                                                       |
| `pdm remove -G standard <package-name>`  | Remove a Python dependency from the `standard` (or whatever group name you're targeting) dependency group. | `standard` is an example name. You can use whatever name you want for dependency groups, as long as they adhere to the naming rules. You will be warned if a name is not compatible.                                                                                  |
| `pdm update`                             | Update all dependencies in the `pdm.lock` file.                                                            |                                                                                                                                                                                                                                                                       |
| `pdm update <package-name>`              | Update a specific dependency.                                                                              |                                                                                                                                                                                                                                                                       |
| `pdm update -d <package-name>`           | Update a specific development dependency.                                                                  |                                                                                                                                                                                                                                                                       |
| `pdm update -G standard <package-name>`  | Update a specific dependency in the "standard" dependency group.                                           | `standard` is an example name; make sure you're using the right group name.                                                                                                                                                                                           |
| `pdm update -d`                          | Update all development dependencies.                                                                       |                                                                                                                                                                                                                                                                       |
| `pdm update -G standard`                 | Update all dependencies in the dependency group named "standard".                                          |                                                                                                                                                                                                                                                                       |
| `pdm update -G "standard,another_group"` | Update multiple dependency groups at the same time.                                                        |                                                                                                                                                                                                                                                                       |
| `pdm lock`                               | Lock dependencies to a `pdm.lock` file.                                                                    | Helps `pdm` with reproducible builds.                                                                                                                                                                                                                                 |
| `pdm run python src/app_name/main.py`    | Run the `main.py` file using the `pdm`-controller Python executable.                                       | Prepending Python commands with `pdm run` ensures you are running them with the `pdm` Python version instead of the system's Python. You can also activate the `.venv` environment and drop `pdm run` from the beginning of the command to accomplish the same thing. |
| `pdm run custom-script`                  | Execute a script defined in `pyproject.toml` file named `custom-script`.                                   | [PDM scripts](https://pdm-project.org/latest/usage/scripts/)                                                                                                                                                                                                          |

## What is PDM?

🔗 [PDM official site](https://pdm-project.org/latest/)

🔗 [PDM GitHub](https://github.com/pdm-project/pdm)

PDM (Python Dependency Manager) is a tool that helps manage Python projects & dependencies. It does many things, but a simple way to describe it is that it replaces `virtualenv` and `pip`, and ensures when you install dependencies, they will be compatible with the current Python version and other dependencies you add to the project. Some dependencies require other dependencies, and where `pip` might give you an error about a `ModuleNotFound`, `pdm` is smart enough to see that there are extra dependencies and will automatically add them as it installs the dependency you asked for.

!!! note

    Unlike `pip`, `pdm` uses a `pyproject.toml` file to manage your project and its dependencies. This is a flexible file where you can add metadata to your project, create [custom `pdm` scripts](https://pdm-project.org/latest/usage/scripts/), & more.

## What problem does PDM solve?

If you have already used tools like `poetry` or `conda`, you are familiar with the problem `pdm` solves. In a nutshell, dependency management in Python is painful, frustrating, and difficult. `pdm` (and other similar tools) try to solve this problem using a "dependency matrix," which ensures the dependencies you add to your project remain compatible with each other. This approach helps avoid "dependency hell," keeps your packages isolated to the project they were installed for, and skips the `ModuleNotFound` error you will see in `pip` when a dependency requires other dependencies to install.

`pdm` is also useful for sharing code, as anyone else who uses `pdm` can install the *exact same* set of dependencies that you installed on your machine. This is accomplished using a "lockfile," which is a special `pdm.lock` file the `pdm` tool creates any time you install a dependency in your project. Unless you manually update the package, any time you run `pdm install`, it will install the exact same set of dependencies, down to the minor release number, keeping surprise errors at bay if you update a package that does not "fit" in your current environment by ensuring a specific, compatible version of that package is installed.

`pdm` can also help you build your projects and publish them to `pypi`, and can install your development tools (like `black`, `ruff`, `pytest`, etc) outside of your project's environment, separating development and production dependencies. `pdm` also makes it easy to create dependency "groups," where a user can install your package with syntax like `package_name[group]`. You may have seen this syntax in the `pandas` or `uvicorn` packages, where the documentation will tell you to install like `pandas[excel]` or `uvicorn[standard]`. The maintainers of these packages have created different dependency "groups," where if you only need the Excel functionality included in `pandas`, for example, it will only install the dependencies required for that group, instead of all of the dependencies the `pandas` package requires.

Lastly, `pdm` can make you more efficient by providing [functionality for scripting](https://pdm-project.org/latest/usage/scripts/). With `pdm`, you can create scripts like `start` or `start-dev` to control executing commands you would manually re-type each time you wanted to run them.

## How to install PDM

!!! note

    Please refer to the [Official PDM installation instructions](https://pdm-project.org/latest/#installation) for instructions. I personally use the `pipx` method (`pipx install pdm`), but there are multiple sets of instructions that are updated occasionally, and it is best to check PDM's official documentation for installation/setup instructions.

## Library vs Application

When you initialize a new project with `pdm init`, you will be asked a series of questions that will help `pdm` determine the type of environment to set up. One of the questions asks if your project is a library or application:

```shell title="PDM library or app question"
Is the project a library that is installable?
If yes, we will need to ask a few more questions to include the project name and build backend [y/n] (n):
```

!!! warning

    This choice does matter! It affects how Python structures your project, and how the project executes. You will need to answer a couple of extra questions for an "application," but there is a correct way to answer this question when `pdm` asks it.

    Continue reading for more information.

For a more in-depth description of when to choose a "library" vs an "application", please read the [Official PDM documentation](https://pdm-project.org/latest/usage/project/#library-or-application).

As a rule of thumb, modules you import into other scripts/apps and do not have a CLI tool (like the `pydantic` or `requests` modules) are a "library." A module that includes a CLI and can be executed from the command line, but is built with Python (like `black`, `ruff`, `pytest`, `mypy`, `uvicorn`, etc) are an "application." 
