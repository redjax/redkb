# Alembic Notes

* Install `alembic` with `pip install alembic` (or some equivalent package install command)
* Initialize `alembic`
  * If using a `src` directory, i.e. `src/app`, initialize `alembic` at `src/app/alembic`
    * `alembic init src/app/alembic`
  * If using a "flat" repository, simply run `alembic init alembic`

    !!!note
        You can use any name for the directory instead of "alembic." For instance, another common convention is to initialize `alembic` with `alembic init migrations`
        
        Whatever directory name you choose, use that throughout these instructions where you see references to the `alembic` init path

* Edit the `alembic.ini` file
  * Change `script_location` to the path you set for alembic, i.e. `src/app/alembic`
  * Edit `prepend_sys_path`, set to `src/app`
    * This adds the script's path to `alembic` can do things like importing your app's config, loading the SQLAlchemy `Base` object, etc

```
## alembic.ini

[alembic]

script_location = src/app/alembic

...

prepend_system_path = src/app

...

```

* Edit the `alembic` `env.py` file, which should be in `src/app/alembic` (or whatever path you initialized `alembic` in)
  * If you initialized a SQLAlchemy database URI string (of type `sqlalchemy.URL`), you can import it in `env.py`, or you can create a new one:

```
## src/app/alembic.py

...

import sqlalchemy as sa

## Using a SQLite example
DB_URI: sa.URL = sa.URL.create(
    drivername="sqlite+pysqlite",
    username=None,
    password=None,
    host=None,
    port=None,
    database="database.sqlite"
)

...

## Set config's sqlalchemy.url value, after "if config.config_filename is not None:"
config.set_main_option(
    "sqlalchemy.url",
    ## Use .render_as_string(hide_password=False) with sqlalchemy.URL objects,
    #  otherwise database password will be "**"
    DB_URI.render_as_string(hide_password=False)
)

...

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from app.module.models import SomeModel  # Import project's SQLAlchemy table classes
from app.module.database import Base  # Import project's SQLAlchemy Base object

target_metadata = Base().metadata  # Tell Alembic to use the project's Base() object
```

## Performing Alembic migrations

- Perform first/initial migration:
  - `alembic revision --autogenerate -m "initial migration"`
    - If no changes have been made, `alembic revision` will create an empty revision, with no changes.
- Upgrade:
  - If you are doing multiple migrations at once, you can do:
    - `alembic upgrade +1`
      - (`+1` is how many migration levels to apply at once. If you have multiple migrations that have not been committed, you can use `+2`, `+3`, etc)
  - To push the current revision:
    - `alembic upgrade head`
      - This will push all current migrations, up to the current migration, to the database
- To Downgrade/revert a migration:
    - `alembic downgrade -1`
      - (`-1` is how many migration levels to revert, can also be `-2`, `-3`, etc)

## Manually specify migration changes when Alembic does not correctly detect them

Some changes, like renaming a column, are not possible for Alembic to accurately track. In these cases, you will need to create an Alembic migration, then edit the new file in `alembic/versions/{revision-hash}.py`.

In the `def upgrade()` section, comment the innacurate `op.add_column()`/`op.drop_column()`, then add something like this (example uses the `User` class, with a renamed column `.username` -> `.user_name`):

```
# alembic/versions/{revision-hash}.py

...

def upgrade() -> None:
    ...

    ## Comment the inaccurate changes
    #  op.add_column("users", sa.Column("user_name", sa.VARCHAR(length=255), nullable=True))
    #  op.drop_column("users", "username)

    ## Manually add a change of column type that wasn't detected by alembic
    op.alter_column("products", "description", type_=sa.VARCHAR(length=3000))

    ## Manually describe column rename
    op.alter_column("users", "username", new_column_name="user_name")
```

Also edit the `def downgrade()` function to describe the changes that should be reverted when using `alembic downgrade`:

```
# alembic/versions/{revision-hash}.py

...

def downgrade() -> None:
    ## Comment the inaccurate changes
    #  op.add_column("users", sa.Column("user_name", sa.VARCHAR(length=255), nullable=True))
    #  op.drop_column("users", "username)

    ## Manually describe changes to reverse if downgrading
    op.alter_column("users", "user_name", new_column_name="username")
    op.drop_column("products", "price")

    
```

After describing manual changes in an Alembic version file, you need to run `alembic upgrade head` to push the changes from the revision to the database.
