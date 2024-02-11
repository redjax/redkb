# Pytest fixture templates

Some templates/example of `pytest` [`fixtures`](https://docs.pytest.org/en/stable/how-to/fixtures.html)

## dummy_hello_str()

```py title="dummy_fixtures.py" linenums="1"
from pytest import fixture


@fixture
def dummy_hello_str() -> str:
    """A dummy str fixture for pytests."""
    return "hello, world"

```
