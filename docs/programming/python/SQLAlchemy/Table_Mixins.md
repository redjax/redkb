---
tags:
    - python
    - sqlalchemy
---

# Table Mixin Classes

SQLAlchemy supports "mixins," which are partial classes that define functionality when multi-inheritance is used to declare a table class. An example is the `TablenameMixin` class, which automatically creates a table name based on the class's name (i.e. a class named `UserComment` would be named `usercomments`).

## Multi-inheritance example

```python title="SQLAlchemy table class multi-inheritance example" linenums="1"
import sqlalchemy as sa
import sqlalchemy.orm as so

from your_database_module.base import Base


class TableNameMixin:
    """Mixin to automatically name tables based on class name.

    Generates a `__tablename__` for classes inheriting from this mixin.
    """

    @so.declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"


class UserComment(Base, TabeNameMixin):
    ## No need to declare a table name, the table will be named 'usercomments'
    #   __table_name__ = "user_comments_tbl"

    ...

```

## Example mixin classes

### TimestampMixin class

```python title="TimestampMixin" linenums="1"
from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as so


class TimestampMixin:
    """Add a created_at & updated_at column to records.

    Add to class declaration to automatically create these columns on
    records.

    Usage:

    py linenums=1
    class Record(Base, TimestampMixin):
        __tablename__ = ...

        ...

    """

    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now()
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()
    )

```

### TableNameMixin class

```python title="TimestampMixin" linenums="1"
class TableNameMixin:
    """Mixin to automatically name tables based on class name.

    Generates a `__tablename__` for classes inheriting from this mixin.
    """

    @so.declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: D105
        return cls.__name__.lower() + "s"

```

