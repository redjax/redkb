---
tags:
    - python
    - sqlite
    - database
---

# Convert JSON to SQLite

The following scripts can be used to convert arbitrary JSON data to tables in a SQLite database. Both scripts also provide a CLI, run them with `--help` to see usage. Both scripts perform the following actions:

- Read & parse JSON data from an input string or a JSON file path.
- Open a SQLite connection.
- Store parsed JSON data as SQLite tables.

The [controller version of the script](#controller-class-version) uses a [Python context manager class](https://realpython.com/python-with-statement/#coding-class-based-context-managers) to manage the reading & writing operations. This prevents data loss due to errors & interruptions.

## Script version

```python title="json_to_sqlite.py" linenums="1"
"""Identify JSON structure & create SQLite database dynamically from data.

Description:
  Ingest JSON data, either from a file or an input string (i.e. encoded with `json.dumps()`). Iterate over the fields & construct
  tables in a SQLite database from the input data.

  Script is useful for converting arbitrarily structured JSON data into a 'raw' format.

Usage:
    Run `python json_to_sqlite.py --help` to see options.
"""

import logging
import json
import typing as t
import sqlite3
from pathlib import Path
from argparse import ArgumentParser, Namespace
import re

log = logging.getLogger()

## Possible return values for JsonTypeLiteral
JSON_TYPE_LITERALS = t.Literal[
    "key_value_pair",
    "nested_object",
    "array",
    "array_of_arrays",
    "array_of_values",
]

## Possible values for JsonType
JSON_READ_RETURN_TYPES = (
    t.Dict[str, t.Any] | t.List[t.Any] | str | int | float | bool | None
)

## Type of data in input JSON
JsonTypeLiteral = t.Annotated[
    JSON_TYPE_LITERALS,
    """Allowed JSON types:
- "key_value_pair"
- "nested_object"
- "array"
- "array_of_arrays"
- "array_of_values"
""",
]

## Expanded json.loads() -> t.Any
JsonType = t.Annotated[
    JSON_READ_RETURN_TYPES,
    "Return value for json.loads(). One of: dict[str, Any], list[Any], str, int, float, bool, None.",
]


def parse_args() -> Namespace:
    """Parse user's input params into arguments."""

    ## Initialize parser
    parser: ArgumentParser = ArgumentParser(
        "json_to_sqlite", description="Convert input JSON data to SQLite tables."
    )

    ## Add params

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--json-str", type=str, default=None, help="A JSON string to convert to SQLite."
    )
    parser.add_argument(
        "--json-file",
        type=str,
        default=None,
        help="Path to a .json file to convert to SQLite.",
    )
    parser.add_argument(
        "--db-file",
        type=str,
        default="converted_from_json.sqlite3",
        help="Path to a SQLite database file where converted data will be saved. If the database does not exist, it will be created.",
    )

    ## Parse into args
    args: Namespace = parser.parse_args()

    return args


def process_json_params(json_str: str | None, json_file: str | None) -> t.Any:
    """Process the JSON input parameters and return the JSON data.

    Params:
        json_str (str | None): JSON string passed directly.
        json_file (str | None): Path to a JSON file.

    Returns:
        t.Any: JSON data as a dictionary, list, or other JSON-compatible type.

    Raises:
        ValueError: If neither `json_str` nor `json_file` is provided.
    """
    if not json_str and not json_file:
        raise ValueError("Must pass either --json-str or --json-file")

    if json_str:
        ## Prefer --json-str if both are provided
        if json_file:
            log.warning(
                "Both --json-str and --json-file provided. Preferring --json-str."
            )
        try:
            return json.loads(json_str)  # Parse the JSON string
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

    ## If only --json-file is provided, read its content
    try:
        data = read_json_file(file=json_file)
        return data
    except FileNotFoundError:
        raise ValueError(f"File not found: {json_file}")


def read_json_file(file: str | Path) -> t.Any:
    """Read contents of a JSON file into a variable.

    Params:
        file (str | Path): Path to a JSON file to read.

    Returns:
        t.Any: The JSON data as a dictionary, list, or other JSON-compatible type.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be read or contains invalid JSON.
    """
    file: Path = Path(str(file)).expanduser() if "~" in str(file) else Path(str(file))

    if not file.exists():
        raise FileNotFoundError(f"Could not find JSON file at path: {file}")

    try:
        with open(str(file), "r") as f:
            contents: str = f.read()
    except Exception as exc:
        log.error(f"Error reading from file '{file}'. Details: {exc}")
        raise ValueError(f"Error reading file: {exc}")

    try:
        data = json.loads(contents)
        return data

    except json.JSONDecodeError as exc:
        log.error(
            f"Error converting contents of file '{file}' from JSON. Details: {exc}"
        )
        raise ValueError(f"Error decoding JSON from file: {exc}")


def make_json_serializable(
    data: dict | list[dict] | bytearray,
) -> dict | list[dict] | str | bytearray:
    """Recursively convert non-serializable fields (e.g., bytes) to JSON-serializable formats.

    Params:
        data (dict | list[dict] | bytearray): Input data to evaluate/convert.

    Returns:
        (dict | list[dict] | str | bytearray): Object with all types converted to JSON serializable type.
    """
    if isinstance(data, dict):
        try:
            return {key: make_json_serializable(value) for key, value in data.items()}
        except Exception as exc:
            log.error(
                f"Error coverting input data to JSON serializable type. Details: {exc}"
            )
            raise

    elif isinstance(data, list):
        try:
            return [make_json_serializable(item) for item in data]
        except Exception as exc:
            log.error(
                f"Error coverting input data to JSON serializable type. Details: {exc}"
            )
            raise

    elif isinstance(data, bytes):
        ## Convert bytes to string
        try:
            return data.decode("utf-8", errors="replace")
        except Exception as exc:
            log.error(
                f"Error coverting input data to JSON serializable type. Details: {exc}"
            )
            raise

    else:
        return data


def sanitize_column_name(column_name: str) -> str:
    """Sanitizes a column name by replacing unsupported characters with '_'.

    Params:
        column_name (str): The original column name.

    Returns:
        str: A sanitized column name compatible with SQLite.
    """
    ## SQLite allows letters, numbers, and underscores in column names
    #  Replace invalid characters with '_'
    sanitized_name: str = re.sub(r"[^a-zA-Z0-9_]", "_", column_name)

    ## Ensure the name starts with a letter or underscore (SQLite requirement)
    if not sanitized_name[0].isalpha() and not sanitized_name[0] != "_":
        sanitized_name = "_" + sanitized_name

    return sanitized_name


def check_json_type(data: t.Dict | t.List[t.Dict]) -> JsonTypeLiteral:
    """Return a string value describing the type of JSON inputted.

    Params:
        data (dict | list[dict]): The JSON-like data structure to evaluate.

    Returns:
        (Literal["Key-value pair JSON", "Nested JSON object", "JSON array", "JSON array of arrays", "JSON array of values"]): A string
        describing the type of JSON data inputted as `data`.

    Raises:
        (ValueError): When type cannot be determined, or input is None/empty.
    """
    if data is None:
        raise ValueError("Missing a data input, either a dict or list of dicts.")

    if isinstance(data, dict):
        if all(
            isinstance(value, (str, int, float, bool, type(None)))
            for value in data.values()
        ):
            return "key_value_pair"

        else:
            return "nested_object"

    elif isinstance(data, list):
        if all(isinstance(item, dict) for item in data):
            return "array"
        elif all(isinstance(item, list) for item in data):
            return "array_of_arrays"
        else:
            return "array_of_values"

    else:
        raise ValueError(f"Unknown JSON type: {type(data)}")


def create_table(c: sqlite3.Cursor, table_name: str, columns: list[str]) -> None:
    """Create a table in the SQLite database.

    Params:
        c (sqlite3.Cursor): A SQLite Cursor object for an active database connection.
        table_name (str): The name of the table to create.
        columns (list[str]): Column name values for the table.

    Raises:
        (Exception): When any unhandled exception occurs.
    """
    ## Join list of column names into string
    columns_definition: str = ", ".join([f"{col} TEXT" for col in columns])

    ## Build query string
    create_statement: str = (
        f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})"
    )
    log.debug(f"CREATE TABLE statement: {create_statement}")

    ## Create table
    log.info(f"Creating table: {table_name}")
    try:
        c.execute(create_statement)
        log.info(f"Table '{table_name}' created or already exists.")
    except Exception as exc:
        log.error(f"Error executing CREATE TABLE {table_name}. Details: {exc}")
        raise


def insert_into_db(json_type: JsonTypeLiteral, data: t.Dict, db_file: str):
    """Insert data into SQLite table."""

    def preprocess_value(value):
        """Preprocess values to ensure they are SQLite-compatible."""
        if isinstance(value, list):
            return json.dumps(value)
        elif isinstance(value, dict):
            return json.dumps(value)
        else:
            return value

    def add_missing_columns(
        c: sqlite3.Cursor,
        table_name: str,
        existing_columns: list[str],
        new_columns: list[str],
    ) -> None:
        """Add missing columns to an SQLite table.

        Params:
            c (sqlite3.Cursor): A SQLite cursor from an active SQLite connection.
            table_name (str): The name for the SQLite table.
            existing_columns (list[str]): List of columns that already exist in the table.
            new_columns (list[str]): List of new columns to create.
        """
        for column in new_columns:
            if column not in existing_columns:
                try:
                    c.execute(f"ALTER TABLE {table_name} ADD COLUMN {column} TEXT")
                    log.info(
                        f"Added missing column '{column}' to table '{table_name}'."
                    )
                except Exception as exc:
                    log.error(
                        f"Error adding column '{column}' to table '{table_name}'. Details: {exc}"
                    )
                    raise

    ## Connect to database
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
    except Exception as exc:
        log.error(f"Error connecting to database '{db_file}'. Details: {exc}")
        raise

    ## Handle nested JSON objects
    if json_type == "nested_object":
        log.debug(f"Data is of JSON type: {json_type}:\n{data}")
        table_name = "nested_data"

        ## Preprocess and sanitize data
        sanitized_data = {
            sanitize_column_name(key): preprocess_value(value)
            for key, value in data.items()
        }
        columns = list(sanitized_data.keys())

        ## Create table if it doesn't exist
        try:
            create_table(c, table_name, columns)
        except Exception as exc:
            log.error(f"Error creating table '{table_name}'. Details: {exc}")
            conn.close()
            raise

        ## Check existing columns and add missing ones
        try:
            c.execute(f"PRAGMA table_info({table_name})")
            existing_columns = [row[1] for row in c.fetchall()]
            add_missing_columns(c, table_name, existing_columns, columns)
        except Exception as exc:
            log.error(f"Error updating schema for table '{table_name}'. Details: {exc}")
            conn.close()
            raise

        ## Insert data into the table
        placeholders = ", ".join("?" for _ in range(len(columns)))
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        values = [sanitized_data.get(col) for col in columns]

        try:
            c.execute(sql, values)
            log.info(f"Data inserted into '{table_name}': {values}")
        except Exception as exc:
            log.error(f"Error inserting data into table '{table_name}'. Details: {exc}")
            conn.close()
            raise

    ## Commit changes and close connection
    try:
        conn.commit()
    except Exception as exc:
        log.error(f"Error committing changes to database '{db_file}'. Details: {exc}")
        raise
    finally:
        conn.close()


def convert_json_to_sqlite(json_data: t.Any, db_file: str):
    """Convert JSON data to SQLite tables.

    Params:
        json_data (t.Any): Parsed JSON data. Can be a dict or a list of dicts.
        db_file (str): Path to the SQLite database file.
    """
    try:
        if isinstance(json_data, list):
            for item in json_data:
                if isinstance(item, dict):
                    try:
                        json_type: JsonTypeLiteral = check_json_type(item)
                        log.debug(f"JSON Type Identified: '{json_type}'")
                        log.info(
                            f"Creating database from input JSON data at path: {db_file}"
                        )
                        ## Insert data into DB.
                        insert_into_db(json_type, item, db_file)
                    except Exception as exc:
                        log.error(
                            f"Error processing list item and inserting into database '{db_file}'. Details: {exc}"
                        )
                        raise
                else:
                    log.error(
                        f"List item is not a dict, but of type {type(item)}. Skipping."
                    )
        elif isinstance(json_data, dict):
            try:
                json_type: JsonTypeLiteral = check_json_type(json_data)
                log.debug(f"JSON Type Identified: '{json_type}'")
                log.info(f"Creating database from input JSON data at path: {db_file}")
                insert_into_db(json_type, json_data, db_file)
            except Exception as exc:
                log.error(
                    f"Error inserting data into database '{db_file}'. Details: {exc}"
                )
                raise
        else:
            log.error(
                f"Unsupported JSON data type: {type(json_data)}.  Must be a dict or a list of dicts."
            )
            raise ValueError(
                f"Unsupported JSON data type: {type(json_data)}. Must be a dict or list."
            )
    except Exception as exc:
        log.error(f"Error converting JSON data to SQLite tables. Details: {exc}")
        raise


def main(json_data: t.Any, db_file: str):
    """Main function to convert JSON data to SQLite database."""
    log.info("Analyzing input data")

    ## Normalize input data into a list for consistent processing
    if isinstance(json_data, (str, dict)):
        json_data = [json_data]
    elif isinstance(json_data, bytearray):
        try:
            json_data = [json.loads(json_data.decode("utf-8"))]
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            log.error(f"Failed to decode bytearray as JSON: {exc}")
            raise ValueError("Invalid bytearray input. Must be valid JSON.") from exc
    elif not isinstance(json_data, list):
        log.error(
            f"Invalid input type: {type(json_data)}. Must be str, dict, bytearray, or list."
        )
        raise ValueError("Invalid input type. Must be str, dict, bytearray, or list.")

    try:
        convert_json_to_sqlite(json_data, db_file)
        log.info("JSON data inserted into the database.")
    except Exception as exc:
        log.error(f"Error during main execution: {exc}")
        raise


if __name__ == "__main__":
    ## Pargs CLI args
    args: Namespace = parse_args()

    ## Set logging level
    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    ## Add stream handler
    stream_handler: logging.StreamHandler = logging.StreamHandler()
    formatter: logging.Formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s:%(lineno)s :: %(message)s"
    )
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    ## Process JSON into Python object
    json_data = process_json_params(args.json_str, args.json_file)

    try:
        main(json_data, args.db_file)
    except Exception as exc:
        log.error(f"Program failed. Details: {exc}")

```

## Controller class version

This version uses a `JsonSqliteConverter` controller class to manage reading from a JSON file, initializing a SQLite database, & storing the JSON data in tables & columns by parsing the JSON into a flatter schema.

```python title="convert_json.py" linenums="1"
"""Identify JSON structure & create SQLite database dynamically from data.

Description:
  Ingest JSON data, either from a file or an input string (i.e. encoded with `json.dumps()`). Iterate over the fields & construct
  tables in a SQLite database from the input data.

  Script is useful for converting arbitrarily structured JSON data into a 'raw' format.

Usage:
    Run `python json_to_sqlite.py --help` to see options.
"""
import sqlite3
import logging
import json
import typing as t
import sqlite3
from pathlib import Path
from argparse import ArgumentParser, Namespace
import re
from contextlib import AbstractContextManager

log = logging.getLogger()

## Possible return values for JsonTypeLiteral
JSON_TYPE_LITERALS = t.Literal[
    "key_value_pair",
    "nested_object",
    "array",
    "array_of_arrays",
    "array_of_values",
]

## Possible values for JsonType
JSON_READ_RETURN_TYPES = (
    t.Dict[str, t.Any] | t.List[t.Any] | str | int | float | bool | None
)

## Type of data in input JSON
JsonTypeLiteral = t.Annotated[
    JSON_TYPE_LITERALS,
    """Allowed JSON types:
- "key_value_pair"
- "nested_object"
- "array"
- "array_of_arrays"
- "array_of_values"
""",
]

## Expanded json.loads() -> t.Any
JsonType = t.Annotated[
    JSON_READ_RETURN_TYPES,
    "Return value for json.loads(). One of: dict[str, Any], list[Any], str, int, float, bool, None.",
]


def parse_args() -> Namespace:
    """Parse user's input params into arguments."""

    ## Initialize parser
    parser: ArgumentParser = ArgumentParser(
        "json_to_sqlite", description="Convert input JSON data to SQLite tables."
    )

    ## Add params

    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument(
        "--json-str", type=str, default=None, help="A JSON string to convert to SQLite."
    )
    parser.add_argument(
        "--json-file",
        type=str,
        default=None,
        help="Path to a .json file to convert to SQLite.",
    )
    parser.add_argument(
        "--db-file",
        type=str,
        default="converted_from_json.sqlite3",
        help="Path to a SQLite database file where converted data will be saved. If the database does not exist, it will be created.",
    )

    ## Parse into args
    args: Namespace = parser.parse_args()

    return args


class JsonSqliteConverter(AbstractContextManager):
    """Controller class for converting JSON data to a SQLite database.

    Description:
        When calling as a context manager, i.e. `with JsonSqliteConverter(db_file=..., json_file=..., json_str=...)`, a SQLite
        database connection is immediately created at the path in `db_file`. If the database does not already exist, this step
        creates the database file.

        The controller opens a SQLite connection & creates a Cursor object for executing queries. It also loads & parses any JSON data,
        whether that be a string that was passed as a CLI arg, or the data in the file defined in `json_file`. The controller reads the JSON
        data during initialization, storing it in a class variable '.json_data'.

        Finally, the controller tries to write the JSON to SQLite tables.

    Params:
        db_file (str): Path to the SQLite database file. Will be created if it does not already exist.
        json_file (Optional[str]): Path to a JSON file with data to read and convert.
        json_str (Optional[str]): A JSON string on your clipboard to read & convert.
    """

    def __init__(
        self, db_file: str, json_file: t.Optional[str], json_str: t.Optional[str]
    ):
        self.db_file = db_file
        self.json_file = json_file
        self.json_str = json_str

        self.json_data: JsonType | None = None

        self.logger = log.getChild("JsonSqliteConverter")
        self.conn: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    def __enter__(self) -> "JsonSqliteConverter":
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
        except Exception as exc:
            self.logger.error(
                f"Error connecting to database '{self.db_file}'. Details: {exc}"
            )
            raise

        try:
            self._process_json_params()
        except Exception as exc:
            self.logger.error(f"Error parsing input JSON. Details: {exc}")
            raise

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            try:
                if exc_type is None:
                    self.logger.info(f"Committing changes to database: {self.db_file}")
                    self.conn.commit()
                else:
                    self.logger.warning(
                        f"Rolling back changess due to error: ({exc_type}) {exc_val}"
                    )
            except Exception as exc:
                self.logger.error(f"({exc_type}) {exc}")
            finally:
                self.logger.info(f"Closing connection to database: {self.db_file}")
                self.conn.close()
                self.conn = None
                self.cursor = None

    def __repr__(self):
        return f"JsonSqliteConverter(db_file={self.db_file}, json_file={self.json_file}{', json_str=None' if self.json_str is None else ''})"

    @property
    def db_file_exists(self) -> bool:
        if self.db_file is None:
            return False

        return Path(str(self.db_file)).exists()

    @property
    def json_file_exists(self) -> bool:
        if self.json_file is None:
            return False

        return Path(str(self.json_file)).exists()

    def _process_json_params(self) -> t.Any:
        """Process the JSON input parameters and return the JSON data.

        Params:
            json_str (str | None): JSON string passed directly.
            json_file (str | None): Path to a JSON file.

        Returns:
            t.Any: JSON data as a dictionary, list, or other JSON-compatible type.

        Raises:
            ValueError: If neither `json_str` nor `json_file` is provided.
        """
        if not self.json_str and not self.json_file:
            raise ValueError("Must pass either --json-str or --json-file")

        if self.json_str:
            ## Prefer --json-str if both are provided
            if self.json_file:
                self.logger.warning(
                    "Both --json-str and --json-file provided. Preferring --json-str."
                )
            try:
                self.json_data = self.read_json_file()
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON string: {e}")

        ## If only --json-file is provided, read its content
        try:
            data = self.read_json_file()
            self.json_data = data
        except FileNotFoundError:
            raise ValueError(f"File not found: {self.json_file}")

    def read_json_file(self) -> t.Any:
        """Read contents of a JSON file into a variable.

        Params:
            file (str | Path): Path to a JSON file to read.

        Returns:
            t.Any: The JSON data as a dictionary, list, or other JSON-compatible type.

        Raises:
            FileNotFoundError: If the file does not exist.
            ValueError: If the file cannot be read or contains invalid JSON.
        """
        self.json_file: Path = (
            Path(str(self.json_file)).expanduser()
            if "~" in str(self.json_file)
            else Path(str(self.json_file))
        )

        if not self.json_file.exists():
            raise FileNotFoundError(
                f"Could not find JSON file at path: {self.json_file}"
            )

        try:
            with open(str(self.json_file), "r") as f:
                contents: str = f.read()
        except Exception as exc:
            self.logger.error(
                f"Error reading from file '{self.json_file}'. Details: {exc}"
            )
            raise ValueError(f"Error reading file: {exc}")

        try:
            data = json.loads(contents)
            return data

        except json.JSONDecodeError as exc:
            self.logger.error(
                f"Error converting contents of file '{self.json_file}' from JSON. Details: {exc}"
            )
            raise ValueError(f"Error decoding JSON from file: {exc}")

    def sanitize_column_name(self, column_name: str) -> str:
        """Sanitizes a column name by replacing unsupported characters with '_'.

        Params:
            column_name (str): The original column name.

        Returns:
            str: A sanitized column name compatible with SQLite.
        """
        ## SQLite allows letters, numbers, and underscores in column names
        #  Replace invalid characters with '_'
        sanitized_name: str = re.sub(r"[^a-zA-Z0-9_]", "_", column_name)

        ## Ensure the name starts with a letter or underscore (SQLite requirement)
        if not sanitized_name[0].isalpha() and not sanitized_name[0] != "_":
            sanitized_name = "_" + sanitized_name

        return sanitized_name

    def make_json_serializable(
        self,
        data: dict | list[dict] | bytearray,
    ) -> dict | list[dict] | str | bytearray:
        """Recursively convert non-serializable fields (e.g., bytes) to JSON-serializable formats.

        Params:
            data (dict | list[dict] | bytearray): Input data to evaluate/convert.

        Returns:
            (dict | list[dict] | str | bytearray): Object with all types converted to JSON serializable type.
        """
        if isinstance(data, dict):
            try:
                return {
                    key: self.make_json_serializable(value)
                    for key, value in data.items()
                }
            except Exception as exc:
                self.logger.error(
                    f"Error coverting input data to JSON serializable type. Details: {exc}"
                )
                raise

        elif isinstance(data, list):
            try:
                return [self.make_json_serializable(item) for item in data]
            except Exception as exc:
                self.logger.error(
                    f"Error coverting input data to JSON serializable type. Details: {exc}"
                )
                raise

        elif isinstance(data, bytes):
            ## Convert bytes to string
            try:
                return data.decode("utf-8", errors="replace")
            except Exception as exc:
                self.logger.error(
                    f"Error coverting input data to JSON serializable type. Details: {exc}"
                )
                raise

        else:
            return data

    def create_table(self, table_name: str, columns: list[str]) -> None:
        """Create a table in the SQLite database.

        Params:
            c (sqlite3.Cursor): A SQLite Cursor object for an active database connection.
            table_name (str): The name of the table to create.
            columns (list[str]): Column name values for the table.

        Raises:
            (Exception): When any unhandled exception occurs.
        """
        ## Join list of column names into string
        columns_definition: str = ", ".join([f"{col} TEXT" for col in columns])

        ## Build query string
        create_statement: str = (
            f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition})"
        )
        self.logger.debug(f"CREATE TABLE statement: {create_statement}")

        ## Create table
        self.logger.info(f"Creating table: {table_name}")
        try:
            self.cursor.execute(create_statement)
            self.logger.info(f"Table '{table_name}' created or already exists.")
        except Exception as exc:
            self.logger.error(
                f"Error executing CREATE TABLE {table_name}. Details: {exc}"
            )
            raise

    def insert_into_db(self, json_type: JsonTypeLiteral, data: t.Dict, db_file: str):
        """Insert data into SQLite table."""

        def preprocess_value(value):
            """Preprocess values to ensure they are SQLite-compatible."""
            if isinstance(value, list):
                return json.dumps(value)
            elif isinstance(value, dict):
                return json.dumps(value)
            else:
                return value

        def add_missing_columns(
            table_name: str,
            existing_columns: list[str],
            new_columns: list[str],
        ) -> None:
            """Add missing columns to an SQLite table.

            Params:
                c (sqlite3.Cursor): A SQLite cursor from an active SQLite connection.
                table_name (str): The name for the SQLite table.
                existing_columns (list[str]): List of columns that already exist in the table.
                new_columns (list[str]): List of new columns to create.
            """
            for column in new_columns:
                if column not in existing_columns:
                    try:
                        self.cursor.execute(
                            f"ALTER TABLE {table_name} ADD COLUMN {column} TEXT"
                        )
                        self.logger.info(
                            f"Added missing column '{column}' to table '{table_name}'."
                        )
                    except Exception as exc:
                        self.logger.error(
                            f"Error adding column '{column}' to table '{table_name}'. Details: {exc}"
                        )
                        raise

        ## Handle nested JSON objects
        if json_type == "nested_object":
            self.logger.debug(f"Data is of JSON type: {json_type}:\n{data}")
            table_name = "nested_data"

            ## Preprocess and sanitize data
            sanitized_data = {
                self.sanitize_column_name(key): preprocess_value(value)
                for key, value in data.items()
            }
            columns = list(sanitized_data.keys())

            ## Create table if it doesn't exist
            try:
                self.create_table(table_name, columns)
            except Exception as exc:
                self.logger.error(
                    f"Error creating table '{table_name}'. Details: {exc}"
                )
                raise

            ## Check existing columns and add missing ones
            try:
                self.cursor.execute(f"PRAGMA table_info({table_name})")
                existing_columns = [row[1] for row in self.cursor.fetchall()]
                add_missing_columns(table_name, existing_columns, columns)
            except Exception as exc:
                self.logger.error(
                    f"Error updating schema for table '{table_name}'. Details: {exc}"
                )
                raise

            ## Insert data into the table
            placeholders = ", ".join("?" for _ in range(len(columns)))
            sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

            values = [sanitized_data.get(col) for col in columns]

            try:
                self.cursor.execute(sql, values)
                self.logger.info(f"Data inserted into '{table_name}': {values}")
            except Exception as exc:
                self.logger.error(
                    f"Error inserting data into table '{table_name}'. Details: {exc}"
                )
                raise
            finally:
                self.conn.commit()

    def convert_json_to_sqlite(self):
        """Convert JSON data to SQLite tables.

        Params:
            json_data (t.Any): Parsed JSON data. Can be a dict or a list of dicts.
            db_file (str): Path to the SQLite database file.
        """
        try:
            if isinstance(self.json_data, list):
                for item in self.json_data:
                    if isinstance(item, dict):
                        try:
                            json_type: JsonTypeLiteral = check_json_type(item)
                            log.debug(f"JSON Type Identified: '{json_type}'")
                            log.info(
                                f"Creating database from input JSON data at path: {self.db_file}"
                            )
                            ## Insert data into DB.
                            self.insert_into_db(json_type, item, self.db_file)
                        except Exception as exc:
                            log.error(
                                f"Error processing list item and inserting into database '{self.db_file}'. Details: {exc}"
                            )
                            raise
                    else:
                        log.error(
                            f"List item is not a dict, but of type {type(item)}. Skipping."
                        )
            elif isinstance(self.json_data, dict):
                try:
                    json_type: JsonTypeLiteral = check_json_type(self.json_data)
                    log.debug(f"JSON Type Identified: '{json_type}'")
                    log.info(
                        f"Creating database from input JSON data at path: {self.db_file}"
                    )
                    self.insert_into_db(json_type, self.json_data, self.db_file)
                except Exception as exc:
                    log.error(
                        f"Error inserting data into database '{self.db_file}'. Details: {exc}"
                    )
                    raise
            else:
                log.error(
                    f"Unsupported JSON data type: {type(self.json_data)}.  Must be a dict or a list of dicts."
                )
                raise ValueError(
                    f"Unsupported JSON data type: {type(self.json_data)}. Must be a dict or list."
                )
        except Exception as exc:
            log.error(f"Error converting JSON data to SQLite tables. Details: {exc}")
            raise


def check_json_type(data: t.Dict | t.List[t.Dict]) -> JsonTypeLiteral:
    """Return a string value describing the type of JSON inputted.

    Params:
        data (dict | list[dict]): The JSON-like data structure to evaluate.

    Returns:
        (Literal["Key-value pair JSON", "Nested JSON object", "JSON array", "JSON array of arrays", "JSON array of values"]): A string
        describing the type of JSON data inputted as `data`.

    Raises:
        (ValueError): When type cannot be determined, or input is None/empty.
    """
    if data is None:
        raise ValueError("Missing a data input, either a dict or list of dicts.")

    if isinstance(data, dict):
        if all(
            isinstance(value, (str, int, float, bool, type(None)))
            for value in data.values()
        ):
            return "key_value_pair"

        else:
            return "nested_object"

    elif isinstance(data, list):
        if all(isinstance(item, dict) for item in data):
            return "array"
        elif all(isinstance(item, list) for item in data):
            return "array_of_arrays"
        else:
            return "array_of_values"

    else:
        raise ValueError(f"Unknown JSON type: {type(data)}")


def main(db_file=str, json_file=t.Optional[str], json_str=t.Optional[str]):
    """Main function to convert JSON data to SQLite database."""
    json_sqlite_converter: JsonSqliteConverter = JsonSqliteConverter(
        db_file=db_file, json_file=json_file, json_str=json_str
    )

    try:
        with json_sqlite_converter as converter:
            converter.convert_json_to_sqlite()
            log.info(f"JSON data inserted into database: {db_file}")
    except Exception as exc:
        log.error(f"Error during main execution: {exc}")
        raise


if __name__ == "__main__":
    args = parse_args()

    ## Set logging level
    if args.debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    ## Add stream handler
    stream_handler: logging.StreamHandler = logging.StreamHandler()
    formatter: logging.Formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s:%(lineno)s :: %(message)s"
    )
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    try:
        main(args.db_file, args.json_file, args.json_str)
    except Exception as exc:
        log.error(f"Error converting JSON to SQLite: {exc}")

        exit(1)

```
