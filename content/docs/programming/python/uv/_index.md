---
title: "Uv"
date: 2026-08-21T00:32:41-04:00
draft: true
weight: 10
toc: true
keywords: []
tags:
  - python
  - uv
  - programming
---

[`uv`](https://docs.astral.sh/uv) is a Python project manager. It consolidates functionality of many different tools into 1 convenient CLI. The tool is written in Rust, and is extremely fast. It uses a custom dependency solver so dependency search/install from Pypi is faster, too.

The tool handles the following (and more):

- Project initialization
  - The [`uv init`](https://docs.astral.sh/uv/reference/cli/#uv-init) command initializes a directory path for developing Python programs.
  - It has `--app` and `--lib` options, scaffolding the directory for developing an [app](https://docs.astral.sh/uv/reference/cli/#uv-init--app) or [library](https://docs.astral.sh/uv/reference/cli/#uv-init--lib).
  - You can use the [`--bare`](https://docs.astral.sh/uv/reference/cli/#uv-init--bare) option to create only a `pyproject.toml` file, which tracks the project's build configuration & dependencies, but does not create any project scaffolding.
  - `uv` can also manage individual scripts with the [`--script`](https://docs.astral.sh/uv/reference/cli/#uv-init--script) option.
    - Initializes a single `.py` file, adding a docstring at the top of the file in accordance with [PEP 723 - Inline script metadata](https://peps.python.org/pep-0723/).
- Virtual environments
  - When you run a `uv` command, a `.venv/` directoy is created automatically.
  - Whenever you run a command prefixed with `uv`, i.e. `uv python main.py`, the tool will use the virtual environment's Python/Pip.
- [Manage your Python install](https://docs.astral.sh/uv/guides/install-python/), allowing you to install multiple versions scoped to individual `uv`-managed projects.
- [Manage your project dependencies](https://docs.astral.sh/uv/concepts/projects/dependencies/).
  - Can also install [dev depenencies](https://docs.astral.sh/uv/concepts/projects/dependencies/#development-dependencies), which are available locally during development but are not packaged with the app.
- [`uvx`](https://docs.astral.sh/uv/guides/tools/) runs a tool in an isolated environment, i.e. `uvx ruff`, without installing it or adding it to the project.
  - You can [install tools to  the system](https://docs.astral.sh/uv/guides/tools/#installing-tools) with `uv tool install <tool-name>`.
