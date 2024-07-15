# Validators

## Valid DB types

It's useful to have a `constants.py` or some other place to store validators; to limit the databases your project supports, you could create a `valid_db_types` variable, like:

```python title="constants.py - valid_db_types" linenums="1"
"""Validators for custom SQLAlchemy utilities.

`valid_db_types`: List of strings of supported database types.

Supported: `["sqlite", "postgres", "mssql"]`
"""

## List of valid/supported databases
from __future__ import annotations

valid_db_types: list[str] = ["sqlite", "postgres", "mssql"]

## Usage: assert 'some_db_name' not in valid_db_types, ValueError(f"Database 'some_db_name' is not supported. Supported databases: {valid_db_types}")
```
