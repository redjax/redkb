---
title: "Fixtures"
date: 2024-02-11T00:00:00-00:00
draft: false
weight: 10
keywords: []
tags:
  - python
  - testing
  - pytest
  - reference
lastmod: "2026-04-13T04:26:49Z"
---

Some templates/example of `pytest` [`fixtures`](https://docs.pytest.org/en/stable/how-to/fixtures.html)

## dummy_hello_str()

```py title="dummy_fixtures.py" linenums="1"
from pytest import fixture


@fixture
def dummy_hello_str() -> str:
    """A dummy str fixture for pytests."""
    return "hello, world"

```
