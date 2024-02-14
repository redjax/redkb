---
tags:
    - standard-project-files
    - python
    - alembic
---

# Alembic env.py file

After initializing alembic (i.e. `alembic init alembic`), a file `alembic/env.py` will be created. This file can be edited to include your project's models and SQLAlchemy `Base`.

Below are snippets of custom code I add to my alembic `env.py` file.

## DB_URI

Provide database connection URL to alembic.

!!!TODO

    - [ ] Use `dynaconf` to load database connection values from environment.
    - [ ] Describe where to put this code in `env.py`

```py title="env.py: DB_URI"
DB_URI: sa.URL = sa.URL.create(
    drivername="sqlite+pysqlite",
    username=None,
    password=None,
    host=None,
    port=None,
    database="database.sqlite"
)
```

## Set Alembic's sqlalchemy.url value

Instead of hardcording the database connection string in `alembic.ini`, load it from [`DB_URI`](#db_uri).

!!!TODO

    - [ ] Describe where to push this code in `env.py`

```py title="env.py: alembic config 'sqlalchemy.url'"
## Set config's sqlalchemy.url value, after "if config.config_filename is not None:"
config.set_main_option(
    "sqlalchemy.url",
    ## Use .render_as_string(hide_password=False) with sqlalchemy.URL objects,
    #  otherwise database password will be "**"
    DB_URI.render_as_string(hide_password=False)
)
```

## Import your project's SQLAlchemy table model classes and create Base metadata

Importing your project's SQLAlchemy `Base` and table classes that inherit from the `Base` object into alembic allows for automatic metadata creation.

!!!note

    When using `alembic` to create the `Base` metadata, you do not need to run `Base.metadata.create(bind=engine)` in your code. Alembic handles the metadata creation for you. Just make sure to run `alembic` when first creating the database, or when cloning if using a local database like SQLite.

```py title="env.py: Import project models, create Base metadta"
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# Import project's SQLAlchemy table classes
from app.module.models import SomeModel
# Import project's SQLAlchemy Base object
from app.core.database import Base

# Tell Alembic to use the project's Base() object
target_metadata = Base().metadata

```
