# Python Naming Conventions

## Modules
- Module names should be short, lowercase, and descriptive.
- Avoid using underscores in module names.

    ```python
    # Good
    import mymodule

    # Avoid
    import my_module
    ```

## Classes
- Class names should use the CapWords (CamelCase) convention.
- Make class names descriptive.

    ```python
    class MyClass:
        pass
    ```

## Functions and Variables
- Function and variable names should be lowercase, with words separated by underscores.
- Be descriptive with names.

    ```python
    def calculate_distance():
        pass

    total_count = 0
    ```

## Constants
- Constants should be in uppercase with underscores separating words.
- Use constants sparingly and only for values that are not meant to be changed.

    ```python
    MAX_RETRY = 3
    ```

## Global Variables
- If using global variables, follow the conventions for functions and variables.

    ```python
    global_variable = 42
    ```

## Arguments
- Function and method arguments should be lowercase, with words separated by underscores.
- Be descriptive with parameter names.

    ```python
    def calculate_sum(x, y):
        pass
    ```

## Instance Variables
- Instance variables in classes should be lowercase, with words separated by underscores.
- Prefix instance variables with an underscore if private.

    ```python
    class MyClass:
        def __init__(self):
            self._private_variable = 10
    ```

## Private Methods
- Prefix the name of a private method with a single leading underscore.

    ```python
    class MyClass:
        def _private_method(self):
            pass
    ```

## Class Attributes
- Class attributes should be in lowercase with words separated by underscores.

    ```python
    class MyClass:
        class_attribute = 42
    ```

## Method Names
- Use lowercase with words separated by underscores for method names.

    ```python
    def calculate_sum():
        pass
    ```

## Reference

These naming conventions have been written by ChatGPT on 01/24/2024.

---

_© 2023, [Nicolas Huber](https://nicolas-huber.ch). All rights reserved._