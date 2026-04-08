---
tags:
    - python
    - sqlalchemy
---


# SQLAlchemy

!!! INTRODUCTION

    These docs written for `sqlalchemy == 2.0`

    - 🏠 [SQLAlchemy Home](https://www.sqlalchemy.org)
    - 📖 [SQLAlchemy Docs Index](https://docs.sqlalchemy.org/en/20/#)
        - 📄 [SQLAlchemy ORM Quick Start](https://docs.sqlalchemy.org/en/20/orm/quickstart.html)
            - Learn the new 2.0 syntax with a guided tutorial/quickstart.
        - 📄 [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
            - The 2.0 release of SQLAlchemy introduced a new ORM syntax. It is different enough from versions prior to 2.0 that a tutorial demonstrating the "old" and "new" ways of doing things was needed.
            - The newer 2.0 syntax is simpler and more Pythonic, and feels more flexible (subjective opinions).


## Sample Code

Check the pages in this section for sample code & explanations for using SQLAlchemy in your app.

!!! note

    Check my [`red-utils` package's `.ext.sqlalchemy_utils`](https://github.com/redjax/red-utils/tree/main/src/red_utils/ext/sqlalchemy_utils) module for an example `database` module. You can essentially copy/paste the code into a directory in your project like `src/app/database/`.


## Full sample: From initializing DBSettings to adding an entity

When setting SQLAlchemy up in a new project, you must lay some groundwork first. You need to create a [`Base`](https://docs.sqlalchemy.org/en/20/orm/declarative_styles.html#orm-declarative-generated-base-class) class that your models will inherit from, and you need to configure an engine & session pool. Repository classes are optional, but highly recommended to control reading from/writing to the database.

The guide below assumes you have created a directory in your project called `db/` to store all the SQLAlchemy code.

### Setup SQLAlchemy configuration

!!! TODO

    - [ ] Section for loading from `dynaconf`
    - [ ] Section for loading from env with `os.getenv()`
    - [ ] Creating a `DBSettings` class

### Create engine & session pool

!!! TODO

    - [ ] Creating an engine
    - [ ] Creating a session pool

### Create your SQLAlchemy and repository Base classes

In your `db/` directory, create a file called `base.py`. This file is where you will configure your SQLAlchemy `Base` class, as well as any other base classes for the app like `BaseRepository`:

```python title="db/base.py" linenums="1"
from __future__ import annotations

import typing as t

import sqlalchemy as sa
import sqlalchemy.exc as sa_exc
import sqlalchemy.orm as so

## Generic type representing an instance of a class
T = t.TypeVar("T")


class Base(so.DeclarativeBase):
    pass


class BaseRepository(t.Generic[T]):
    """Base class for a SQLAlchemy database repository.

    Usage:
        When creating a new repository class, inherit from this BaseRepository.
        The new class will have sessions for create(), get(), update(), delete(), and list().
    """

    def __init__(self, session: so.Session, model: t.Type[T]):
        self.session = session
        self.model = model

    def create(self, obj: T) -> T:
        self.session.add(obj)

        self.session.commit()
        self.session.refresh(obj)

        return obj

    def get(self, id: int) -> t.Optional[T]:
        return self.session.get(self.model, id)

    def update(self, obj: T, data: dict) -> T:
        for key, value in data.items():
            setattr(obj, key, value)

        self.session.commit()

        return obj

    def delete(self, obj: T) -> None:
        self.session.delete(obj)

        self.session.commit()

    def list(self) -> list[T]:
        return self.session.execute(sa.select(self.model)).scalars().all()

    def count(self) -> int:
        """Return the count of entities in the table."""
        return self.session.query(self.model).count()

```

When creating new database model classes, you will inherit from this `Base` class. For example, to create a `User` model in a file called `models.py`:

```python title="Example models.py" linenums="1"
## Import the Base class from the db/ directory
from db import Base

import sqlalchemy as sa
import sqlalchemy.orm as so


## Create a User class that inherits from the SQLAlchemy Base class
class User(Base):
    __tablename__ = "users"

    id: so.Mapped[int] = so.mapped_column(sa.INTEGER, primary_key=True)

    name: so.Mapped[str] = so.mapped_column(sa.TEXT, nullable=False, default=None)
    age: so.Mapped[int] = so.mapped_column(sa.INTEGER, nullable=False, default=0)

```

Similarly, the `BaseRepository` class can be inherited from when creating a `UserRepository` class to handle CRUD operations on the `User` model:

```python title="Example UserRepository() class" linenums="1"
## Import the BaseRepository class from db/
from db import BaseRepository
## Import the User model from models.py
from .models import User

import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.exc as sa_exc


## Inherit from the BaseRepository class, granting access to all functions/parameters
class UserRepository(BaseRepository):
    def __init__(self, session: so.Session):
        ## The super() function here calls the base class's __init__. This is required for inheritance
        super().__init__(session, User)

    ## This class now has access to the BaseRepository's functions, like create(), get(), update(), etc
    #  Any functions/parameters defined on this class are exclusive to this class and do not get propagated
    #  "down" to the BaseRepository
    def get_by_name(self, name: str) -> User:
        return self.session.query(User).filter(User.name == name).one_or_none()

    ...

```

### Committing a User to the database

!!! TODO

    - [ ] Example converting a dict to a `User` class
    - [ ] Example of creating a `session_pool`
    - [ ] Example of using a repository to commit a `User` to the database
