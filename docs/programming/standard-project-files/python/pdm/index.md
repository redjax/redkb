## PDM - Python Dependency Manager

I use [`pdm`](pdm-project.org/) to manage most of my Python projects. It's a fantastic tool for managing environments, dependencies, builds, and package publishing. PDM is similar in functionality to [`poetry`](https://python-poetry.org), which I have also used and liked. My main reasons for preferring `pdm` over `poetry` are:

- Scripts. It is so useful being able to define a `[tool.pdm.scripts]` section in my `pyproject.toml`, and being able to script long/repeated things like `alembic` commands or project execution scripts is so handy.
- Dependency resolution
  - I had almost no problems with Poetry. I've had *no* problems with PDM
- Does things in a more Pythonic way than `poetry` ([reference](https://frostming.com/2021/03-26/pm-review-2021/))

Most of my notes and code snippets will assume `pdm` is the dependency manager for a given project.
