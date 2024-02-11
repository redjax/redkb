from __future__ import annotations

import pendulum
import sqlalchemy as sa
import sqlalchemy.orm as so

class TimestampMixin:
    """Add a created_at & updated_at column to records.

    Add to class declaration to automatically create these columns on
    records.

    Usage:

    ``` py linenums=1
    class Record(Base, TimestampMixin):
        __tablename__ = ...

        ...
    ```
    """

    created_at: so.Mapped[pendulum.DateTime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now()
    )
    updated_at: so.Mapped[pendulum.DateTime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()
    )


class TableNameMixin:
    """Mixing to automatically name tables based on class name.

    Generates a `__tablename__` for classes inheriting from this mixin.
    """

    @so.declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
