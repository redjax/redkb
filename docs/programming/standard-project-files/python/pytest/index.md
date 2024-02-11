# Pytest

!!!TODO

    - [ ] Describe how I configure `pytest` for my projects
    - [ ] Describe how to use the files in this section

## pytest.ini

Put the `pytest.ini` file in the root of the project to configure `pytest` executions

```ini title="pytest.ini" linenums="1"
[pytest]
# Filter unregistered marks. Suppresses all UserWarning
# messages, and converts all other errors/warnings to errors.
filterwarnings =
    error
    ignore::UserWarning
testpaths = tests

```

## Example/basic tests/main.py

!!!note
    
    These tests don't really do anything, but they are the basis for writing `pytest` tests.

```py title="test_dummy.py" linenums="1"
from __future__ import annotations

from pytest import mark, xfail

@mark.hello
def test_say_hello(dummy_hello_str: str):
    assert isinstance(
        dummy_hello_str, str
    ), f"Invalid test output type: ({type(dummy_hello_str)}). Should be of type str"
    assert (
        dummy_hello_str == "world"
    ), f"String should have been 'world', not '{dummy_hello_str}'"

    print(f"Hello, {dummy_hello_str}!")


@mark.always_pass
def test_pass():
    assert True, "test_pass() should have been True"


@mark.xfail
def test_fail():
    test_pass = False
    assert test_pass, "This test is designed to fail"


```

## conftest.py

Put `conftest.py` inside your `tests/` directory. This file configures `pytest`, like providing test fixture paths so they can be accessed by tests.

```py title="conftest.py" linenums="1"
import pytest

## Add fixtures as plugins
pytest_plugins = [
    "tests.fixtures.dummy_fixtures"
]
```
