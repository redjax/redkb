---
tags:
    - python
    - jupyter
---

# Jupyter

!!!warning

    In progress...

!!! todo

    - [ ] Document creating a kernel
      - [ ] With `virtualenv`
      - [ ] With `conda`
      - [ ] With `pdm`
    - [ ] Document `jupyterlab`
      - [ ] Running with custom settings
      - [ ] Installing plugins
      - [ ] (Optional) in Docker
    - [ ] Document importing custom Python modules

## Useful magic cells

!!! todo

    - [ ] Set environment variables
    - [ ] Install packages with pip

### Reload files without restarting kernel

When importing Python code into a Jupyter notebook, any changes made in the Python module(s) do not become active in the Jupyter kernel until it's restarted. This is undesirable when working with data that takes a long time up front to prepare.

Add this code to a cell (I usually put it in the very first cell) to automatically reload Python modules on changes, without having to reload the whole notebook kernel.

```py title="Automatically reload file on changes" linenums="1"

## Set notebook to auto reload updated modules
%load_ext autoreload
%autoreload 2

```

## Automations

### Automatically strip notebook cell output when committing to git

!!! todo

    - [ ] Describe VSCode error that happens after `pre-commit` runs and what to do to fix it
    - [ ] Describe disabling `pre-commit`

When running Jupyter notebooks, it's usually good practice to clear the notebook's output when committing to git. This can be for privacy/security (if you're debugging PII or environment variables in the notebook), or just a tidy repository.

Using `pre-commit` (check [my section on `pre-commit`](../standard-project-files/pre-commit/)) and the [`nbstripout action`](https://github.com/kynan/nbstripout), we can automate stripping the notebook each time a git commit is created.

**Instructions**

- Install `pre-commit`

!!! note

    !!! warning
    
        If your preferred package manager is not listed below, check the documentation for that package manager for instructions on installing packages.

    ---

    - With `pip`:
        - `pip install pre-commit`
    - With `pipx`:
        - `pipx install pre-commit`
    - With `pdm`:
        - `pdm add pre-commit`
    
    TODO:
    
    - [ ] `poetry`
    - [ ] `conda`/`miniconda`/`microconda`


- Create a file in the root of your repository `.pre-commit-config.yml` with these contents:

```yaml title=".pre-commit-config.yml" linenums="1"
repos:
    repo: https://github.com/kynan/nbstripout
    rev: 0.6.1
    hooks:
        - id: nbstripout
```

- Install the `pre-commit` hook with `$ pre-commit install`

!!! note

    If you installed `pre-commit` in a `virtualenv`, or with a tool like `pdm`, make sure the `.venv` is activated, or you run with `$ pdm run pre-commit ...`

Now, each time you make a `git commit`, after writing your commit message, `pre-commit` will execute `nbstripout` to strip your notebooks of their output.

