# Use PDM to manage your Python projects & dependencies

!!! TODO

    - [x] Write section describing `pdm`
        - [x] What is `pdm`?
        - [x] What problem does `pdm` solve?
    - [ ] Write `pdm` cheat sheet
        - [x] Initialize a project
            - [x] Difference between an `application` and a `library`
        - [ ] Add/remove dependencies
        - [ ] Execute code
        - [ ] Add development dependencies
        - [ ] Publish project to `pypi`

!!! TOC

    - [`pdm` cheat sheet](#pdm-cheat-sheet)
    - [What is PDM?](#what-is-pdm)
        - [What problem does PDM solve?](#what-problem-does-pdm-solve)
    - [How to install PDM](#how-to-install-pdm)
    - [What is a "library" vs an "application"](#library-vs-application)

## PDM cheat sheet

!!! TODO

    - [ ] Install dependency
    - [ ] Install dependency in a specific group
        - [ ] "development" group
        - [ ] A custom "standard" group
    - [ ] Uninstall dependency
    - [ ] Uninstall dependency from a specific group
        - [ ] "development" group
        - [ ] A custom "standard" group
    - [ ] Update a package
    - [ ] Lock dependencies
    - [ ] Run commands with `pdm run`
    - [ ] Execute a PDM script
    - [ ] Publish a package to pypi

| Command    | Description                         | Notes                                                                                           |
| ---------- | ----------------------------------- | ----------------------------------------------------------------------------------------------- |
| `pdm init` | Initialize a new project with `pdm` | The `pdm` tool will ask a series of questions, and build an environment based on your responses |

## What is PDM?

🔗 [PDM official site](https://pdm-project.org/latest/)

🔗 [PDM GitHub](https://github.com/pdm-project/pdm)

PDM (Python Dependency Manager) is a tool that helps manage Python projects & dependencies. It does many things, but a simple way to describe it is that it replaces `virtualenv` and `pip`, and ensures when you install dependencies, they will be compatible with the current Python version and other dependencies you add to the project. Some dependencies require other dependencies, and where `pip` might give you an error about a `ModuleNotFound`, `pdm` is smart enough to see that there are extra dependencies and will automatically add them as it installs the dependency you asked for.

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
