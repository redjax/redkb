---
tags:
    - standard-project-files
    - python
    - ruff
---

# Ruff

[`Ruff`](https://github.com/astral-sh/ruff)...is...awesome! It's hard to summarize, Ruff describes itself as "An extremely fast Python linter and code formatter, written in Rust." It has replaced `isort`, `flake8`, and `black` in my environments.

I use 2 `ruff.toml` files normally:

- `ruff.toml`
  - The "main" configuration, used by the `ruff` command and VSCode
- `ruff.ci.toml`
  - In my [`noxfile.py`](../nox/index.md#noxfilepy-base), I have a `lint` section.
  - This file is more permissive than `ruff.toml` to avoid pipeline errors for things that don't matter like docstring warnings and other rules I find overly strict.

!!! note
    
    You can tell `ruff` to use a specific config file with the `--config` arg.

    ```bash title="ruff custom config" linenums="1"
    $> ruff --config path/to/ruff.custom.toml path/ --fix
    ```

## ruff.toml

```toml title="ruff.toml" linenums="1"
## Set assumed Python version
target-version = "py311"

## Same as Black.
line-length = 88

## Enable pycodestyle ("E") and Pyflakes ("F") codes by default
#  # Docs: https://beta.ruff.rs/docs/rules/
lint.select = [
    "D",    ## pydocstyle
    "E",    ## pycodestyle
    "F401", ## remove unused imports
    "I",    ## isort
    "I001", ## Unused imports
]

## Ignore specific checks.
#  Comment lines in list below to "un-ignore."
#  This is counterintuitive, but commenting a
#  line in ignore list will stop Ruff from
#  ignoring that check. When the line is
#  uncommented, the check will be run.
lint.ignore = [
    "D100", ## missing-docstring-in-public-module
    "D101", ## missing-docstring-in-public-class
    "D102", ## missing-docstring-in-public-method
    "D103", ## Missing docstring in public function
    "D105", ## Missing docstring in magic method
    "D106", ## missing-docstring-in-public-nested-class
    "D107", ## Missing docstring in __init__
    "D200", ## One-line docstring should fit on one line
    "D203", ## one-blank-line-before-class
    "D205", ## 1 blank line required between summary line and description
    "D213", ## multi-line-summary-second-line
    "D401", ## First line of docstring should be in imperative mood
    "E402", ## Module level import not at top of file
    "D406", ## Section name should end with a newline
    "D407", ## Missing dashed underline after section
    "D414", ## Section has no content
    "D417", ## Missing argument descriptions in the docstring for [variables]
    "E501", ## Line too long
    "E722", ## Do note use bare `except`
    "F401", ## imported but unused
]

## Allow autofix for all enabled rules (when "--fix") is provided.
#  NOTE: Leaving these commented until I know what they do
#  Docs: https://beta.ruff.rs/docs/rules/
lint.fixable = [
    # "A",  ## flake8-builtins
    # "B",  ## flake8-bugbear
    "C",
    "D",    ## pydocstyle
    "E",    ## pycodestyle-error
    "E402", ## Module level import not at top of file
    # "F",  ## pyflakes
    "F401", ## unused imports
    # "G",  ## flake8-logging-format
    "I", ## isort
    "N", ## pep8-naming
    # "Q",  ## flake8-quotas
    # "S",  ## flake8-bandit
    "T",
    "W", ## pycodestyle-warning
    # "ANN",  ## flake8-annotations
    # "ARG",  ## flake8-unused-arguments
    # "BLE",  ## flake8-blind-except
    # "COM", ## flake8-commas
    # "DJ",  ## flake8-django
    # "DTZ",  ## flake8-datetimez
    # "EM",  ## flake8-errmsg
    "ERA", ## eradicate
    # "EXE",  ## flake8-executables
    # "FBT",  ## flake8-boolean-trap
    # "ICN",  ## flake8-imort-conventions
    # "INP",  ## flake8-no-pep420
    # "ISC",  ## flake8-implicit-str-concat
    # "NPY",  ## NumPy-specific rules
    # "PD",  ## pandas-vet
    # "PGH",  ## pygrep-hooks
    # "PIE",  ## flake8-pie
    "PL", ## pylint
    # "PT",  ## flake8-pytest-style
    # "PTH",  ## flake8-use-pathlib
    # "PYI",  ## flake8-pyi
    # "RET",  ## flake8-return
    # "RSE",  ## flake8-raise
    "RUF", ## ruf-specific rules
    # "SIM",  ## flake8-simplify
    # "SLF",  ## flake8-self
    # "TCH",  ## flake8-type-checking
    "TID", ## flake8-tidy-imports
    "TRY", ## tryceratops
    "UP",  ## pyupgrade
    # "YTT"  ## flake8-2020
]
# unfixable = []

# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".ruff_cache",
    ".venv",
    "__pypackages__",
    "__pycache__",
    "*.pyc",
]

[lint.per-file-ignores]
"__init__.py" = ["D104"]

## Allow unused variables when underscore-prefixed.
# dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[lint.mccabe]
max-complexity = 10

[lint.isort]
combine-as-imports = true
force-sort-within-sections = true
force-wrap-aliases = true
## Use a single line after each import block.
lines-after-imports = 1
## Use a single line between direct and from import
# lines-between-types = 1
## Order imports by type, which is determined by case,
#  in addition to alphabetically.
order-by-type = true
relative-imports-order = "closest-to-furthest"
## Automatically add imports below to top of files
required-imports = ["from __future__ import annotations"]
## Define isort section priority
section-order = [
    "future",
    "standard-library",
    "first-party",
    "local-folder",
    "third-party",
]

```

## ruff.ci.toml

```toml title="ruff.ci.toml" linenums="1"

## Set assumed Python version
target-version = "py311"

## Same as Black.
line-length = 88

## Enable pycodestyle ("E") and Pyflakes ("F") codes by default
#  # Docs: https://beta.ruff.rs/docs/rules/
lint.select = [
    "D",    ## pydocstyle
    "E",    ## pycodestyle
    "F401", ## remove unused imports
    "I",    ## isort
    "I001", ## Unused imports
]

## Ignore specific checks.
#  Comment lines in list below to "un-ignore."
#  This is counterintuitive, but commenting a
#  line in ignore list will stop Ruff from
#  ignoring that check. When the line is
#  uncommented, the check will be run.
lint.ignore = [
    "D100", ## missing-docstring-in-public-module
    "D101", ## missing-docstring-in-public-class
    "D102", ## missing-docstring-in-public-method
    "D103", ## Missing docstring in public function
    "D105", ## Missing docstring in magic method
    "D106", ## missing-docstring-in-public-nested-class
    "D107", ## Missing docstring in __init__
    "D200", ## One-line docstring should fit on one line
    "D203", ## one-blank-line-before-class
    "D205", ## 1 blank line required between summary line and description
    "D213", ## multi-line-summary-second-line
    "D401", ## First line of docstring should be in imperative mood
    "E402", ## Module level import not at top of file
    "D406", ## Section name should end with a newline
    "D407", ## Missing dashed underline after section
    "D414", ## Section has no content
    "D417", ## Missing argument descriptions in the docstring for [variables]
    "E501", ## Line too long
    "E722", ## Do note use bare `except`
    "F401", ## imported but unused
]

## Allow autofix for all enabled rules (when "--fix") is provided.
#  NOTE: Leaving these commented until I know what they do
#  Docs: https://beta.ruff.rs/docs/rules/
lint.fixable = [
    # "A",  ## flake8-builtins
    # "B",  ## flake8-bugbear
    "C",
    "D",    ## pydocstyle
    "E",    ## pycodestyle-error
    "E402", ## Module level import not at top of file
    # "F",  ## pyflakes
    "F401", ## unused imports
    # "G",  ## flake8-logging-format
    "I", ## isort
    "N", ## pep8-naming
    # "Q",  ## flake8-quotas
    # "S",  ## flake8-bandit
    "T",
    "W", ## pycodestyle-warning
    # "ANN",  ## flake8-annotations
    # "ARG",  ## flake8-unused-arguments
    # "BLE",  ## flake8-blind-except
    # "COM", ## flake8-commas
    # "DJ",  ## flake8-django
    # "DTZ",  ## flake8-datetimez
    # "EM",  ## flake8-errmsg
    "ERA", ## eradicate
    # "EXE",  ## flake8-executables
    # "FBT",  ## flake8-boolean-trap
    # "ICN",  ## flake8-imort-conventions
    # "INP",  ## flake8-no-pep420
    # "ISC",  ## flake8-implicit-str-concat
    # "NPY",  ## NumPy-specific rules
    # "PD",  ## pandas-vet
    # "PGH",  ## pygrep-hooks
    # "PIE",  ## flake8-pie
    "PL", ## pylint
    # "PT",  ## flake8-pytest-style
    # "PTH",  ## flake8-use-pathlib
    # "PYI",  ## flake8-pyi
    # "RET",  ## flake8-return
    # "RSE",  ## flake8-raise
    "RUF", ## ruf-specific rules
    # "SIM",  ## flake8-simplify
    # "SLF",  ## flake8-self
    # "TCH",  ## flake8-type-checking
    "TID", ## flake8-tidy-imports
    "TRY", ## tryceratops
    "UP",  ## pyupgrade
    # "YTT"  ## flake8-2020
]
# unfixable = []

# Exclude a variety of commonly ignored directories.
exclude = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".ruff_cache",
    ".venv",
    "__pypackages__",
    "__pycache__",
    "*.pyc",
]

[lint.per-file-ignores]
"__init__.py" = ["D104"]

## Allow unused variables when underscore-prefixed.
# dummy-variable-rgx = "^(_+|(_+[a-zA-Z0-9_]*[a-zA-Z0-9]+?))$"

[lint.mccabe]
max-complexity = 10

[lint.isort]
combine-as-imports = true
force-sort-within-sections = true
force-wrap-aliases = true
## Use a single line after each import block.
lines-after-imports = 1
## Use a single line between direct and from import
lines-between-types = 1
## Order imports by type, which is determined by case,
#  in addition to alphabetically.
order-by-type = true
relative-imports-order = "closest-to-furthest"
## Automatically add imports below to top of files
required-imports = ["from __future__ import annotations"]
## Define isort section priority
section-order = [
    "future",
    "standard-library",
    "first-party",
    "local-folder",
    "third-party",
]

```
