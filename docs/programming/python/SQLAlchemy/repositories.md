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
