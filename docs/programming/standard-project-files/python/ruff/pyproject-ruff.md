# pyproject.toml tool.ruff section

```python title="pyproject.toml: [tool.ruff] section" linenums="1"
[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = [
    "D",    # pydocstyle
    "E",    # pycodestyle
    "F401", # remove unused imports
    "I",    # isort
    "I001", # Unused imports
]
ignore = [
    "D100", # missing-docstring-in-public-module
    "D101", # missing-docstring-in-public-class
    "D102", # missing-docstring-in-public-method
    "D103", # Missing docstring in public function
    "D105", # Missing docstring in magic method
    "D106", # missing-docstring-in-public-nested-class
    "D107", # Missing docstring in __init__
    "D200", # One-line docstring should fit on one line
    "D203", # one-blank-line-before-class
    "D205", # 1 blank line required between summary line and description
    "D213", # multi-line-summary-second-line
    "D401", # First line of docstring should be in imperative mood
    "E402", # Module level import not at top of file
    "D406", # Section name should end with a newline
    "D407", # Missing dashed underline after section
    "D414", # Section has no content
    "D417", # Missing argument descriptions in the docstring for [variables]
    "E501", # Line too long
    "E722", # Do not use bare `except`
    "F401", # imported but unused
]
fixable = [
    "C",
    "D",    # pydocstyle
    "E",    # pycodestyle-error
    "E402", # Module level import not at top of file
    "F401", # unused imports
    "I",    # isort
    "N",    # pep8-naming
    "T",
    "W",    # pycodestyle-warning
    "ERA",  # eradicate
    "PL",   # pylint
    "RUF",  # ruf-specific rules
    "TID",  # flake8-tidy-imports
    "TRY",  # tryceratops
    "UP",   # pyupgrade
]

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

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["D104"]

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.isort]
combine-as-imports = true
force-sort-within-sections = true
force-wrap-aliases = true
lines-after-imports = 1
order-by-type = true
relative-imports-order = "closest-to-furthest"
required-imports = ["from __future__ import annotations"]
section-order = [
    "future",
    "standard-library",
    "first-party",
    "local-folder",
    "third-party",
]

```
