---
tags:
    - python
    - sqlalchemy
---

# Repositories

A database repository standardizes operations for a given entity. The repository is a class that contains methods like `.add()`, `.remove()`, `.get(id: int)`, etc. Each repository is meant to control a single SQLAlchemy table class (a model class that inherits from SQLAlchemy's `Base` object).

For example, if you have a class `User(Base)` and `Comment(Base)`, you would create 2 repositories, `UserRepository` and `CommentRepository`. Each repository class would have its own `.add()`, `.remove()`, `.get()`, etc.

!!! note

    **Example app using repository class**

    To see an example of one of my apps that uses this pattern, check [`auto-xkcd`](https://github.com/redjax/auto-xkcd/tree/main/src/auto_xkcd).
    
    - [`auto_xkcd.domain.xkcd.comic`](https://github.com/redjax/auto-xkcd/tree/main/src/auto_xkcd/domain/xkcd/comic) for models, schemas, and repositories.
    - [`auto_xkcd.core.database`](https://github.com/redjax/auto-xkcd/tree/main/src/auto_xkcd/core/database) for SQLAlchemy code.
    - To see the repository in action, check the `save_comic_to_db()` method in the [`auto_xkcd.modules.xkcd_modd.methods`](https://github.com/redjax/auto-xkcd/blob/main/src/auto_xkcd/modules/xkcd_mod/methods.py) module.

## Inheriting from a RepositoryBase class

You can define an abstract base class (`abc.ABCMeta`) repository, which your other repository classes can inherit from. On the base class, you can define attributes and methods that must be defined on the child class. This is helpful for requiring methods like `.add()`, `.remove()`, etc on all child classes.

```python title="Example RepositoryBase class" linenums="1"
import abc
import typing as t

T = t.TypeVar("T")

import sqlalchemy as sa
import sqlalchemy as so

class RepositoryBase(t.Generic[T], metaclass=abc.ABCMeta):
	"""A generic SQLAlchemy repository class base."""
    def __init__(self, session: so.Session) -> None:
        if session is None:
            raise ValueError("session cannot be None")

        if not isinstance(session, so.Session):
            raise TypeError(
            f"session must be of type sqlalchemy.orm.Session. Got type: ({type(session)})"
        )

        self.session: so.Session = session

    def __exit__(self):
        """Close database session."""
        self.session.close()

	@abc.abstractmethod
	def add(self, entity: T):
		"""Add new entity to database."""
		raise NotImplementedError()

	@abc.abstractmethod
	def remove(self, entity: T):
		"""Remove existing entity from database."""
		raise NotImplementedError()

	@abc.abstractmethod
	def get_by_id(self, entity_id) -> T:
		"""Retrieve entity from database by its ID."""
		raise NotImplementedError()

```

## Example: UserRepository (inherits from RepositoryBase)

You can use this `RepositoryBase` class to create child repeositories, for example `UserRepository`:

```python title="Example UserRepository class" linenums="1"
class UserRepository(RepositoryBase):
    ## Required by RepositoryBase
    def add(self, entity: UserModel):
        ...
    
    ## Required by RepositoryBase
    def remove(self, entity: UserModel):
        ...

    ## Required by RepositoryBase
    def get_by_id(self, entity_id: int) -> UserModel:
        ...

    ## Not required by RepositoryBase, and only available to UserRepository instances, or children fo this class
    def count(self) -> int:
        ...

```
