from typing import Union, List

from libs.infra.db.errors import UnsupportedPythonTypeForFieldError

# Supported python types
SQLSupportedTypes = Union[str, int, float, bool, None]

# Supported comparison types
SQLComparisonTypes = Union[int, float]


def get_annotated_fields(cls) -> List[str]:
    """
    Get field annotated list from a class.

    :param cls: model class
    :returns: List[str] - list of annotated fields
    """
    fields = []
    for c in cls.__mro__:
        if '__annotations__' in c.__dict__:
            fields.extend(list(c.__annotations__.keys()))
    return fields


def prepare_statement(raw_query: str, *args, **kwargs) -> str:
    """
    Prepare a safe SQL statement (avoiding any SQL Injection risk).

    :param raw_query: str - sql raw query
    :param args: positional arguments
    :param kwargs: named arguments

    :raises ValueError: on any argument not being supported (str, int, float only)
    :returns: str - prepared sql statement
    """
    prepared_positional_args = []
    for arg in args:
        if isinstance(arg, str):
            prepared_positional_args.append(f'"{arg}"')
        elif isinstance(arg, (int, float)):
            prepared_positional_args.append(arg)
        elif isinstance(arg, bool):
            prepared_positional_args.append(1 if arg else 0)
        elif arg is None:
            prepared_positional_args.append("NULL")
        else:
            raise UnsupportedPythonTypeForFieldError(str(type(arg)))

    prepared_named_args = {}
    for name, value in kwargs.items():
        if isinstance(value, str):
            prepared_named_args[name] = f"'{value}'"
        elif isinstance(value, (int, float)):
            prepared_named_args[name] = value
        elif isinstance(value, bool):
            prepared_named_args[name] = 1 if value else 0
        elif value is None:
            prepared_named_args[name] = "NULL"
        else:
            raise UnsupportedPythonTypeForFieldError(str(type(value)))

    return raw_query.format(*prepared_named_args, **prepared_named_args)
