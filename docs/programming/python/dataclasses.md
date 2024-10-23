---
tags:
    - python
    - stdlib
    - dataclasses
---

# Dataclasses

## What is a `dataclass`?

A Python data class is a regular Python class that has the `@dataclass` decorator. It is specifically created to hold data (from [python.land](https://python.land/python-data-classes)).

Dataclasses reduce the boilerplate code when creating a Python class. As an example, below are 2 Python classes: the first is written with Python's standard class syntax, and the second is the simplified dataclass:

```py title="Standard class vs dataclass" linenums="1"
from dataclasses import dataclass

## Standard Python class
class User:
    def __init__(self, name: str, age: int, enabled: bool):
        self.name = name
        self.age = age
        self.enabled = enabled


## Python dataclass
@dataclass
class User:
    user: str
    age: int
    enabled: bool

```

With a regular Python class, you must write an `__init__()` method, define all your parameters, and assign the values to the `self` object. The dataclass removes the need for this `__init__()` method and simplifies writing the class.

This example is so simple, it's hard to see the benefits of using a dataclass over a regular class. Dataclasses are a great way to quickly write a "data container," i.e. if you're passing results back from a function:

```py title="Example dataclass function return" linenums="1"
from dataclasses import dataclass

@dataclass
class FunctionResults:
    original_value: int
    new_value: int


def some_function(x: int = 0, _add: int = 15) -> FunctionResults:
    y = x + _add

    return FunctionResults(original_value=x, new_value=y)

function_results: FunctionResults = some_function(x=15)

print(function_results.new_value)  # = 30

```

Instead of returning a `dict`, returning a `dataclass` allows for accessing parameters using `.dot.notation`, like `function_results.original_value`, instead of `function_results["original_value"].

## Dataclass Mixins

A `mixin` class is a pre-defined class you define with certain properties/methods, where any class inheriting from this class will have access to those methods.

For example, the `DictMixin` dataclass below adds a method `.as_dict()` to any dataclass that inherits from `DictMixin`.

### DictMixin class

Adds a `.as_dict()` method to any dataclass inheriting from this class. This is an alternative to `dataclasses.asdict(_dataclass_instance)`, but also not as flexible.

```py title="DictMixin" linenums="1"
from dataclasses import dataclass
from typing import Generic, TypeVar

## Generic type for dataclass classes
T = TypeVar("T")


@dataclass
class DictMixin:
    """Mixin class to add "as_dict()" method to classes. Equivalent to .__dict__.

    Adds a `.as_dict()` method to classes that inherit from this mixin. For example,
    to add `.as_dict()` method to a parent class, where all children inherit the .as_dict()
    function, declare parent as:

    # ``` py linenums="1"
    # @dataclass
    # class Parent(DictMixin):
    #     ...
    # ```

    # and call like:

    # ```py linenums="1"
    # p = Parent()
    # p_dict = p.as_dict()
    # ```
    """

    def as_dict(self: Generic[T]):
        """Return dict representation of a dataclass instance.

        Description:
            self (Generic[T]): Any class that inherits from `DictMixin` will automatically have a method `.as_dict()`.
                There are no extra params.

        Returns:
            A Python `dict` representation of a Python `dataclass` class.

        """
        try:
            return self.__dict__.copy()

        except Exception as exc:
            raise Exception(
                f"Unhandled exception converting class instance to dict. Details: {exc}"
            )

## Demo inheriting from DictMixin
@dataclass
class ExampleDictClass(DictMixin):
    x: int
    y: int
    z: str


example: ExampleDictclass = ExampleDictClass(x=1, y=2, z="Hello, world!")
example_dict: dict = example.as_dict()

print(example_dict)  # {"x": 1, "y": 2, "z": "Hello, world!"}
```

### JSONEncodeMixin

Inherit from the `json.JSONEncoder` class to allow returning a DataClass as a JSON encode-able dict.

```py title="JSONEncoder class inheritance" linenums="1"
import json
from dataclasses import asdict

class DataclassEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, '__dict__'):
            return obj.__dict__
        elif hasattr(obj, '__dataclass_fields__'):
            return asdict(obj)
        return super().default(obj)

person = Person(name="Alice", age=25)
json.dumps(person, cls=DataclassEncoder)  # Returns '{"name": "Alice", "age": 25}'
```

## Validating a Dataclass

Python dataclasses do not have built-in validation, like a `Pydantic` class. You can still use type hints to define variables, like `name: str = None`, but it has no actual effect on the dataclass.

You can use the `__post_init__(self)` method of a dataclass to perform data validation. A few examples below:

```py title="Dataclass validation" linenums="1"
from dataclasses import dataclass
import typing as t
from pathlib import Path


def validate_path(p: t.Union[str, Path] = None) -> Path:
    assert p, ValueError("Missing an input path to validate.")
    assert isinstance(p, str) or isinstance(p, Path), TypeError(f"p must be a str or Path. Got type: ({type(p)})")
    
    p: Path = Path(f"{p}")
    if "~" in f"{p}":
        p = p.expanduser()

    return p


@dataclass
class ComputerDirectory:
    ## Use | None in the annotation to denote an optional value
    dir_name: str | None = None
    dir_path: t.Union[str, Path] = None

    def __post_init__(self):
        if self.dir_name is None:
            ## self.dir_name is allowed to be None
            pass
        else:
            if not isinstance(self.dir_name, str):
                raise TypeError("dir_name should be a string.")

        if self.dir_path is None:
            raise ValueError("Missing required parameter: dir_path")
        else:
            ## Validate self.dir_path with the validate_path() function
            self.dir_path = validate_path(p=self.dir_path)

```

## Links & Extra Reading

- [Python docs: dataclasses](https://docs.python.org/3/library/dataclasses.html)
- [RealPython: Python Dataclasses](https://realpython.com/python-data-classes/)
- [JSON encoding Python dataclasses](https://www.bruceeckel.com/2018/09/16/json-encoding-python-dataclasses/)
