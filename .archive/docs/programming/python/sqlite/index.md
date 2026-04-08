---
tags:
    - python
    - sqlite
    - database
---

# Python SQLite

Python provides native support for SQLite database operations using the stdlib [`sqlite3` module](https://docs.python.org/3/library/sqlite3.html).

Initializing a connection is as simple as:

```python title="Initialize SQLite connection" linenums="1"
import sqlite3

conn = sqlite3.connect("path/to/your/db.sqlite3")
```

To execute SQL statements, you also need to initialize a `sqlite3.Cursor` object:

```python title="Get Cursor from active connection." linenums="1"
c = conn.cursor()
```

Then you can execute statements against your database:

```python title="Example SQLite statements" linenums="1"
## Create a table
c.execute("CREATE TABLE movie(title, year, score)")

## Show table names
res = c.execute("SELECT name FROM sqlite_master")
res.fetchone()

## Insert data into the movie table
c.execute("""
    INSERT INTO movie VALUES
        ('Monty Python and the Holy Grail', 1975, 8.2),
        ('And Now for Something Completely Different', 1971, 7.5)
""")
```
