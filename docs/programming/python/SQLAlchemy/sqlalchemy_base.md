# SQLAlchemy Base class

## SQLAlchemy Base

The SQLAlchemy [`DeclarativeBase`](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html) class is the "base" class all of your SQLalchemy table model classes should inherit from. When describing a new entity, you intialize the class like:

```python title="Initialize table class" linenums="1"
...

class SomeTableModel(Base):
    ...

```

When you use SQLAlchemy to [create the table metadata](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.MetaData.create_all), the `Base` class gathers all models that inherit from the same `Base` instance and creates table structures in your database.

## Example base.py

In your project, you can put your SQLAlchemy `DeclarativeBase` code in a file, i.e. `app_name/database/base.py`, so it can be imported throughout the rest of your app.

```python title="Declare SQLAlchemy Base (example base.py)" linenums="1"
"""SQLAlchemy `DeclarativeBase`, `MetaData`, and `registry` objects.

Import this `Base` into SQLAlchemy model files and let classes inherit from
the `DeclarativeBase` declared here.

The `registry()` function sets the global SQLAlchemy `registry` for the `DeclarativeBase` object.

!!! note

    Docs for `DeclarativeBase` and `registry()`

    - [Using a DelcarativeBase base class](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#using-a-declarative-base-class)

    Docs for MetaData object

    - [Unified tutorial](https://docs.sqlalchemy.org/en/20/tutorial/metadata.html#tutorial-working-with-metadata)
    - [MetaData Docs](https://docs.sqlalchemy.org/en/20/core/metadata.html)
    - [Impose a table naming scheme with MetaData object](https://docs.sqlalchemy.org/en/20/core/metadata.html#specifying-a-default-schema-name-with-metadata)

"""

from __future__ import annotations

import sqlalchemy as sa
import sqlalchemy.orm as so

## Global SQLAlchemy MetaData object
metadata: sa.MetaData = sa.MetaData()

## Registry object stores mappings & config hooks
reg = so.registry()


## SQLAlchemy DeclarativeBase is the parent class object table classes will inherit from
class Base(so.DeclarativeBase):
    """Default/Base class for SQLAlchemy models.

    Description:

    Child classes inheriting from this Base object will be treated as SQLAlchemy
    models. Set child class tables with `__tablename__ = ....`

    Global defaults can be set on this object (i.e. a SQLAlchemy registry), and will
    be inherited/accessible by all child classes.

    !!! note

        When this class is instantiated, it will not be of type sqlalchemy.orm.DeclarativeBase;
            Because of the way this class is intialized, its type will be
            sqlalchemy.orm.decl_api.DeclarativeAttributeIntercept

    Params:
        registry (sqlalchemy.Registry): A `registry` object for the `Base` class
        metadata (sqlalchemy.MetaData): A `MetaData` object, with data about the `Base` class
    """

    registry: so.registry = reg
    metadata: sa.MetaData = metadata

```
