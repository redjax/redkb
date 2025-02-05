---
tags:
  - alembic
  - python
  - programming
  - database
---
# Alembic

[Alembic](https://alembic.sqlalchemy.org/en/latest/) is a database migration tool, meant to be used with the [SQLAlchemy](../SQLAlchemy/index.md) package. The tool has a bit of a learning curve, but making changes to your database models using a migration tool is highly recommended, especially for long-lived projects.

!!! question

    What is a database migration?

    Migrations offer version control of your database schema by scripting your changes in a repeatable way, incrementally changing your database models over time and offering a path backward if a migration goes south.

    It's kind of like git, but for your database.

## Using Alembic in Python

This is a quick guide on how I set up Alembic for my projects. I am still learning the tool and I'm sure there are more efficient ways of doing some/all of this. I will update this page over time.

### Install Alembic

First install the `alembic` package, i.e. `pip install alembic`. Alembic is normally installed as a "dev" dependency, and not included in your production app/package. If your application does a migration as it is coming online, you would want to include `alembic` in your regular dependencies; otherwise, you should add it as a dev dependency:

```shell title="Installing alembic" linenums="1"
## with pip
pip install alembic --extra dev

## with uv
uv add --dev alembic

## with poetry
poetry add --group dev alembic
```

### Create alembic.ini config file

Next, create an `alembic.ini` file at the root of your repository. Check the [example `alembic.ini` file](#example-alembicini-config-file) I copy/paste into all my projects. You can make changes to the configuration if you want, but **don't hardcode any real connection details in this file**! You will learn how to connect Alembic to your database below.

### Initialize migrations directory

After creating an `alembic.ini` file, initialize your Alembic directory by running the command below. The convention for `<migrations-dir>` below is "migrations." After initializing Alembic, you will have a directory named `migrations/` (or whatever value you used for `<migrations-dir>`) in the path where you ran the init command; you can use whatever name you want for this directory, i.e. `alembic` or `project`. This guide assumes you are using the conventional "migrations":

```shell title="Initialize alembic" linenums="1"
alembic init <migrations-dir>
```

The `migrations/` directory created after running the init command is where your Alembic code lives. As you create migrations, you will see Python files in the `migrations/versions/` directory. This is where Alembic keeps a history of previous migrations, allowing you to travel backwards or forwards at will.

### Edit Alembic's env.py file

The Alembic initialization also created a file `migrations/env.py`. This is the file Alembic uses to do your migrations. You need to make a couple of edits to this file before you can create a migration.

- Import your database configuration so you can pass a database URI to Alembic.
- Import your database model classes.
    - Your SQLAlchemy models (i.e. `class ModelName(Base):`) must be imported, otherwise Alembic will not be aware of them and won't be able to track changes.
    - If the files are sourced in an `__init__.py`, it is sufficient to import that entire directory.
        - i.e. if you have models in `domain/models.py`, and you import your model classes in `domain/__init__.py`, it is sufficient to simply import the whole `domain` module.
- Set your `sqlalchemy.url` value in the alembic `config` object.
- Set your `target_metadata` to your SQLAlchemy `Base.metadata`

Below is an example of an `env.py` file I might use in one of my projects.

!!! warning
    
    The contents below are only the parts of Alembic's `env.py` that I change. Don't copy/paste the whole file, there are only a few values to change. Look for a comment like `# changed by me` to spot lines where you need to make an edit.

```python title="alembic env.py" linenums="1"
from logging.config import fileConfig

from alembic import context

from database.config import DB_URI # changed by me, import the database URI string you use to connect with SQLAlchemy.
from database.base import Base # changed by me, import the SQLAlchemy Base object.
from domain.example.models import ModelClass1, ModelClass2 # changed by me, import the database models.

from sqlalchemy import engine_from_config, pool

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
config.set_main_option( # changed by me, set the Alembic config object's "sqlalchemy.url" value to your database URI.
    "sqlalchemy.url", DB_URI # changed by me, note you could also pass a SQLAlchemy Url object using db_uri.render_as_string(hide_password=False).
)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata # changed by me, set Alembic's target_metadata to the SQLAlchemy Base object's .metadata property

def run_migrations_offline() -> None:
  ...

## the rest of the alembic code
```

### Create the first migration

Use the command below to set your migrations starting point. Each migration after this will be an ancestor in a chain of migrations detailing upgrade paths for the database as your schemas change.

```shell title="Create first migration" linenums="1"
alembic revision --autogenerate -m "Initial migration"
```

Your migration is created, and can be found in the `migrations/versions/` directory. The file will be named `<version_hash>_autogenerated_migration.py`, where `<version_hash>` is a string like `8d185c0473ce`. You can edit this migration script if necessary, and sometimes you will need to if Alembic's `--autogenerate` creates a migration script that fails.

Now you need to apply it with an Alembic "upgrade." This makes changes live in your database to bring the table's schemas inline with the changes described in your migration. You need to do this after each migration.

```shell title="Upgrade database using Alembic migration script." linenums="1"
alembic upgrade head
```

The `head` in the above command indicates the most recent migration.

### Switch between Alembic versions with downgrade/upgrade

`alembic downgrade <revision>` and `alembic upgrade <revision>` are the commands you use to move backwards/forwards through the Alembic migration versions.

#### alembic downgrade

When using the `downgrade` command, you can use a numeric value like `-1` to move back 1 revision, or `-5` to move back 5, etc (any number works as long as there's a version that far back from `head`). You can also give the command a specific reversion commit hash (i.e. `alembic downgrade 8d185c0473ce`).

#### alembic upgrade

The `upgrade` command functions similarly to `downgrade`, except the numeric values are `+#` (i.e. `+3`), a specific hash like `8d185c0473ce` (must be ahead of the current migration), or `head` which is the most recent version.

### Example alembic.ini config file

The following is an `alembic.ini` file I copy/paste into most of my projects. I will occasionally make project-specific tweaks to the file, but the contents below have served me well as a generic Alembic configuration (handling things like the database connection details in [`migrations/env.py`](#create-alembicini-config-file)).

```ini title="alembic.ini" linenums="1"
# A generic, single database configuration.

[alembic]
# path to migration scripts
# Use forward slashes (/) also on windows to provide an os agnostic path
script_location = alembic

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# see https://alembic.sqlalchemy.org/en/latest/tutorial.html#editing-the-ini-file
# for all available tokens
# file_template = %%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s

# sys.path path, will be prepended to sys.path if present.
# defaults to the current working directory.
prepend_sys_path = .

# timezone to use when rendering the date within the migration file
# as well as the filename.
# If specified, requires the python>=3.9 or backports.zoneinfo library.
# Any required deps can installed by adding `alembic[tz]` to the pip requirements
# string value is passed to ZoneInfo()
# leave blank for localtime
# timezone =

# max length of characters to apply to the "slug" field
# truncate_slug_length = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to migrations/versions.  When using multiple version
# directories, initial revisions must be specified with --version-path.
# The path separator used here should be the separator specified by "version_path_separator" below.
# version_locations = %(here)s/bar:%(here)s/bat:migrations/versions

# version path separator; As mentioned above, this is the character used to split
# version_locations. The default within new alembic.ini files is "os", which uses os.pathsep.
# If this key is omitted entirely, it falls back to the legacy behavior of splitting on spaces and/or commas.
# Valid values for version_path_separator are:
#
# version_path_separator = :
# version_path_separator = ;
# version_path_separator = space
version_path_separator = os  # Use os.pathsep. Default configuration used for new projects.

# set to 'true' to search source files recursively
# in each "version_locations" directory
# new in Alembic version 1.10
# recursive_version_locations = false

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

sqlalchemy.url = driver://user:pass@localhost/dbname


[post_write_hooks]
# post_write_hooks defines scripts or Python functions that are run
# on newly generated revision scripts.  See the documentation for further
# detail and examples

# format using "black" - use the console_scripts runner, against the "black" entrypoint
# hooks = black
# black.type = console_scripts
# black.entrypoint = black
# black.options = -l 79 REVISION_SCRIPT_FILENAME

# lint with attempts to fix using "ruff" - use the exec runner, execute a binary
# hooks = ruff
# ruff.type = exec
# ruff.executable = %(here)s/.venv/bin/ruff
# ruff.options = --fix REVISION_SCRIPT_FILENAME

# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

## My AlembicController context manager class

Alembic can be imported into a Python file so you can script Alembic functions. You can put the contents below into a file like `alembic_ctl.py` to create a custom Alembic CLI.

!!! tip

    Run the file without any args, or with `-h/--help`, to see the CLI's help menu. Example:

    ```shell
    python alembic_ctl.py -h
    ```

```python title="AlembicController class" linenums="1"
from pathlib import Path
import typing as t
import argparse
import logging

from contextlib import AbstractContextManager

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory

log = logging.getLogger(__name__)


def setup_logging(
    log_level: str = "INFO",
    log_fmt: str = "%(asctime)s - %(levelname)s - %(message)s",
    date_fmt: str = "%Y-%m-%d %H:%M:%S",
) -> None:
    """Initialize script logging.

    Params:
        log_level (str, optional): Log level. Defaults to "INFO".
        log_fmt (str, optional): Log format. Defaults to "%(asctime)s - %(levelname)s - %(message)s".
        date_fmt (str, optional): Date format. Defaults to "%Y-%m-%d %H:%M:%S".
    """
    logging.basicConfig(
        level=log_level or "INFO",
        format=log_fmt,
        datefmt=date_fmt,
    )


class AlembicController(AbstractContextManager):
    """Context manager for Alembic operations.

    Params:
        alembic_ini_path (str | Path, optional): Path to the Alembic configuration file. Defaults to "alembic.ini".
    Attributes:
        cfg_file (str): Path to the Alembic configuration file.
        config (Config | None): Alembic configuration object.
        log (logging.Logger | None): Logger for the class.

    Example:
        with AlembicController() as ac:
            ac.upgrade()
            ac.create_migration()

    Raises:
        Exception: If an error occurs during Alembic operations.
    """

    def __init__(
        self,
        alembic_ini_path: t.Union[str, Path] = "alembic.ini",
        dry_run: bool = False,
        do_upgrade: bool = False,
    ):
        ## Path to the Alembic configuration file
        self.cfg_file: str = str(alembic_ini_path)

        ## Dry run flag
        self.dry_run: bool = dry_run

        ## Do upgrade flag
        self.do_upgrade: bool = do_upgrade

        ## Alembic configuration object
        self.config: Config | None = None

        ## Logger for the class
        self.log: logging.Logger | None = None

    def __enter__(self) -> t.Self:
        ## Initialize class logger
        self.log = log.getChild("AlembicController")
        ## Initialize Alembic configuration object
        self.config = Config(self.cfg_file)

        return self

    def __exit__(self, exc_type, exc_val, traceback) -> t.Literal[False] | None:
        if exc_val:
            self.log.error(f"({exc_type}) {exc_val}")

            if traceback:
                self.log.error(f"Traceback: {traceback}")

            return False

        return True

    def __repr__(self) -> str:
        return f"AlembicController(alembic_ini_path={self.cfg_file}, dry_run={self.dry_run}, do_upgrade={self.do_upgrade})"

    def upgrade(self, revision: str = "head") -> None:
        """Upgrade the database, or simulate with --dry-run.

        Args:
            revision (str, optional): Revision to upgrade to. Defaults to "head".
            dry_run (bool, optional): Simulate upgrade. Defaults to False.

        Raises:
            Exception: If an error occurs during upgrade.
        """
        log.info(
            f"{'Simulating' if self.dry_run else 'Upgrading'} to revision: {revision}"
        )
        try:
            command.upgrade(self.config, revision, sql=self.dry_run)
            self.log.info(
                f"Database {('would be ' if self.dry_run else '')}upgraded to: {revision}"
            )
        except Exception as exc:
            self.log.error(f"({type(exc)}) Error during upgrade: {exc}")
            raise exc

    def downgrade(self, revision: str = "-1") -> None:
        """Downgrade the database, or simulate with --dry-run.

        Args:
            revision (str, optional): Revision to downgrade to. Defaults to "-1".

        Raises:
            Exception: If an error occurs during downgrade.
        """
        log.info(
            f"{'Simulating' if self.dry_run else 'Downgrading'} to revision: {revision}"
        )

        try:
            if self.dry_run:
                ## Get the current revision before proceeding
                script = self.config.get_main_option("script_location")

                ## Create ScriptDirectory object
                script_directory = ScriptDirectory.from_config(self.config)
                ## Get current head
                current_head = script_directory.get_current_head()

                if not current_head:
                    raise ValueError(
                        "Cannot determine the current revision for --sql mode."
                    )

                ## Target revision to downgrade to
                downgrade_target = f"{current_head}:{revision}"
            else:
                downgrade_target = revision

            if not self.dry_run:
                ## Downgrade the database
                command.downgrade(self.config, downgrade_target, sql=self.dry_run)

            self.log.info(
                f"Database {('would be ' if self.dry_run else '')}downgraded to: {downgrade_target}"
            )
        except Exception as exc:
            self.log.error(f"({type(exc)}) Error during downgrade: {exc}")
            raise exc

    def create_migration(
        self,
        message: str = "autogenerated migration",
    ):
        """Generate a new migration file.

        Args:
            message (str, optional): Message for the migration. Defaults to "autogenerated migration".
            do_upgrade (bool, optional): Upgrade the database after creating the migration. Defaults to False.
            dry_run (bool, optional): Simulate migration creation. Defaults to False.

        Raises:
            Exception: If an error occurs during migration creation.
        """
        if self.dry_run:
            self.log.info(
                f"[DRY-RUN] Would create migration with message: {message}{', and would upgrade the database' if self.do_upgrade else ''}"
            )
            return

        self.log.info(f"Creating migration: {message}")
        try:
            command.revision(self.config, message=message, autogenerate=True)
            log.info(f"Migration created: {message}")
        except Exception as exc:
            self.log.error(f"({type(exc)}) Error creating migration: {exc}")
            raise exc

        if self.do_upgrade:
            self.log.info(f"Upgrading database after creating migration: {message}")
            if not self.dry_run:
                self.upgrade("head", dry_run=self.dry_run)


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Alembic migration controller args.")

    ## Arg for alembic.ini config file path
    parser.add_argument(
        "-f",
        "--config-file",
        nargs="?",
        const="alembic.ini",
        default="alembic.ini",
        metavar="ALEMBIC_INI_FILE",
        help="Path to the Alembic configuration file (default: 'alembic.ini').",
    )

    ## Arg for upgrading database
    parser.add_argument(
        "-u",
        "--upgrade",
        nargs="?",
        const="head",
        default=None,
        metavar="REVISION",
        help="Upgrade database to a specific revision (default: 'head').",
    )

    ## Arg for downgrading database
    parser.add_argument(
        "-d",
        "--downgrade",
        nargs="?",
        const="-1",
        default=None,
        metavar="REVISION",
        help="Downgrade database to a specific revision (default: '-1').",
    )

    ## Arg for creating a new migration
    parser.add_argument(
        "-m",
        "--migrate",
        nargs="?",
        const="autogenerated migration",
        metavar="MESSAGE",
        default=None,
        help="Create a new migration file with the given message.",
    )

    ## Arg for upgrading database after creating a migration
    parser.add_argument(
        "-U",
        "--do-upgrade",
        action="store_true",
        help="Upgrade database after creating a migration (only valid with -m).",
    )

    ## Arg for simulating actions when true, instead of making actual changes
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate the action without making actual changes.",
    )

    args: argparse.Namespace = parser.parse_args()

    ## If no arguments were passed, print help and exit
    if not any([args.upgrade, args.downgrade, args.migrate]):
        parser.print_help()
        exit(1)

    return args


def main(
    args: argparse.Namespace,
):
    """Main entry point for the script.

    Args:
        args (argparse.Namespace): Parsed command-line arguments.
    """
    alembic_ini_file: str = args.config_file
    log.debug(f"Alembic configuration file: {alembic_ini_file}")

    if not Path(alembic_ini_file).exists():
        raise FileNotFoundError(
            f"Could not find Alembic configuration file at '{alembic_ini_file}'"
        )

    ## Initialize Alembic controller
    alembic_controller: AlembicController = AlembicController(
        alembic_ini_path=alembic_ini_file,
        dry_run=args.dry_run,
        do_upgrade=args.do_upgrade,
    )
    log.debug(f"Alembic controller: {alembic_controller}")

    ## Enter alembic controller
    try:
        with alembic_controller as alembic_ctl:
            if args.migrate:
                alembic_ctl.create_migration(args.migrate)
            elif args.upgrade is not None:
                alembic_ctl.upgrade(args.upgrade)
            elif args.downgrade is not None:
                alembic_ctl.downgrade(args.downgrade)
            else:
                raise ValueError("Missing required arguments.")
    except Exception as exc:
        msg = f"({type(exc)}) Unhandled exception. Details: {exc}"
        log.error(msg)

        raise exc


if __name__ == "__main__":
    ## Initialize logging
    setup_logging(log_level="DEBUG")

    ## Get CLI args
    args: argparse.Namespace = parse_args()

    ## Run main function
    main(args=args)
```
