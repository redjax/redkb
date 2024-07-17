---
tags:
    - python
    - sqlalchemy
---

# Annotated columns & custom types

- 📄 [SQLAlchemy docs: Mapping whole column declarations to Python types](https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html#mapping-whole-column-declarations-to-python-types)

## Annotated columns

### Example annotated columns

```python title="annotated_columns.py" linenums="1"
"""Define `Annotated` columns for SQLAlchemy models.

Examples:
    * `INT_PK`: An auto-incrementing, primary key integer value.
    * `STR_10`: A `VARCHAR(10)` column.
    * `STR_255`: A `VARCHAR(255)` column.

"""

from __future__ import annotations

import sqlalchemy as sa
import sqlalchemy.orm as so
from typing_extensions import Annotated

## Annotated auto-incrementing integer primary key column
INT_PK = Annotated[
    int, so.mapped_column(sa.INTEGER, primary_key=True, autoincrement=True, unique=True)
]

## SQLAlchemy VARCHAR(10)
STR_10 = Annotated[str, so.mapped_column(sa.VARCHAR(10))]
## SQLAlchemy VARCHAR(255)
STR_255 = Annotated[str, so.mapped_column(sa.VARCHAR(255))]

```

## Custom Column Types

### Example CustomJson column type

Column type for converting objects to JSON for storage in SQLAlchemy. Inputs can be a list of types, like `list[int]`, `list[str]`, a Python `dict`, or any other JSON-serializable object.

```python title="CustomJson SQLAlchemy column type" linenums="1"
import json

import sqlalchemy as sa

class CustomJson(sa.TypeDecorator):
    impl = sa.String

    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

```
