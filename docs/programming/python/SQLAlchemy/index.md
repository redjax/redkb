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

!!! todo

    - [ ] Setup
        - [ ] `Base` creation
        - [ ] `DBSettings` init
            - [ ] (Optional) with `dynaconf`
    - [ ] Model classes
        - [ ] With mixin classes/multi-inheritance
        - [ ] With custom annotated columns
    - [ ] Get session & repository
    - [ ] Commit entity
