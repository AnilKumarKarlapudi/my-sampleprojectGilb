from typing import List
from typing import Optional
from typing import Union

from libs.infra.db.constants import FIELD_WRAPPER
from libs.infra.db.utils import prepare_statement


class SQLOperation(object):
    """
    SQL Operation interface
    """

    def resolve(self) -> str:
        """
        Resolve SQL operation
        """
        raise NotImplementedError("operation resolve must be implemented")


class EqualOperation(SQLOperation):
    """
    Equal operation (column = value)
    """

    def __init__(self, field: str, value: Optional[Union[int, float, str]]):
        """
        Constructor
        """
        self._field = FIELD_WRAPPER % field
        self._value = value

    def resolve(self) -> str:
        """
        Implemented resolve operation
        """
        operation = self._field + " = {value} "
        return prepare_statement(operation, value=self._value)


class GreaterThanOperation(SQLOperation):
    """
    Greater than operation (column > value)
    """

    def __init__(self, field: str, value: Union[int, float]):
        """
        Constructor
        """
        self._field = FIELD_WRAPPER % field

        # Value validation: null
        if value is None:
            raise ValueError("value cannot be null in 'greater than' operation")

        # Value validation: string
        if isinstance(value, str):
            raise ValueError("value cannot be a string in 'greater than' operation")

        self._value = value

    def resolve(self) -> str:
        """
        Implemented resolve operation
        """
        operation = self._field + " > {value} "
        return prepare_statement(operation, value=self._value)


class LowerThanOperation(SQLOperation):
    """
    Lower than operation (column < value)
    """

    def __init__(self, field: str, value: Union[int, float]):
        """
        Constructor
        """
        self._field = FIELD_WRAPPER % field

        # Value validation: null
        if value is None:
            raise ValueError("value cannot be null in 'lower than' operation")

        # Value validation: string
        if isinstance(value, str):
            raise ValueError("value cannot be a string in 'lower than' operation")

        self._value = value

    def resolve(self) -> str:
        """
        Implemented resolve operation
        """
        operation = self._field + " < {value} "
        return prepare_statement(operation, value=self._value)


class GreaterThanOrEqualOperation(SQLOperation):
    """
    Greater than or equal operation (column >= value)
    """

    def __init__(self, field: str, value: Union[int, float]):
        """
        Constructor
        """
        self._field = FIELD_WRAPPER % field

        # Value validation: null
        if value is None:
            raise ValueError("value cannot be null in 'greater than or equal' operation")

        # Value validation: string
        if isinstance(value, str):
            raise ValueError("value cannot be a string in 'greater than or equal' operation")

        self._value = value

    def resolve(self) -> str:
        """
        Implemented resolve operation
        """
        operation = self._field + " >= {value} "
        return prepare_statement(operation, value=self._value)


class LowerThanOrEqualOperation(SQLOperation):
    """
    Lower than or equal operation (column <= value)
    """

    def __init__(self, field: str, value: Union[int, float]):
        """
        Constructor
        """
        self._field = FIELD_WRAPPER % field

        # Value validation: null
        if value is None:
            raise ValueError("value cannot be null in 'lower than or equal' operation")

        # Value validation: string
        if isinstance(value, str):
            raise ValueError("value cannot be a string in 'lower than or equal' operation")

        self._value = value

    def resolve(self) -> str:
        """
        Implemented resolve operation
        """
        operation = self._field + " <= {value} "
        return prepare_statement(operation, value=self._value)


class LikeOperation(SQLOperation):
    """
    Like operation (column LIKE pattern)
    """

    def __init__(self, field: str, pattern: str):
        self._field = FIELD_WRAPPER % field
        self._pattern = pattern

    def resolve(self) -> str:
        return prepare_statement(self._field + " LIKE {pattern} ", pattern=self._pattern)


class InOperation(SQLOperation):
    """
    In operation (column in (...values))
    """

    def __init__(self, field: str, values: List[Union[int, float, str]]):
        """
        Constructor
        """
        self._field = FIELD_WRAPPER % field

        # values validation
        if len(values) == 0:
            raise ValueError("values must not be empty for 'in' operation")

        self._values = values

    def resolve(self) -> str:
        """
        Implemented resolve operation
        """
        query = []
        for _, value in enumerate(self._field):
            if isinstance(value, float):
                t = "%f"
            elif isinstance(value, int):
                t = "%d"
            elif isinstance(value, str):
                t = "%s"
            elif isinstance(value, bool):
                t = "%d"
            elif value is None:
                t = "%s"
            else:
                raise ValueError("unsupported value type in 'in' operation")

            query.append(t)

        query = ", ".join(query)
        query = f"{self._field} IN ({query}) "

        return prepare_statement(query, *self._values)


class YesNoOperation(SQLOperation):
    """
    YesNo operation (checks if column is true, in SQL Server the implementation is a BIT[1, 0]: column = 1)
    """

    def __init__(self, field: str, yes: bool = True):
        """
        Constructor
        """
        self._field = FIELD_WRAPPER % field
        self._yes = yes

    def resolve(self) -> str:
        """
        Implemented resolve operation
        """
        return f"{self._field} = {'1' if self._yes else '0'} "


class LogicalOperation(SQLOperation):
    """
    Logical operation interface
    """

    def __init__(self, operator: str, operation: str):
        """
        Constructor
        """
        self._operation = operation
        self._operator = operator

    def resolve(self) -> str:
        """
        Implemented resolver operation
        """
        return f"{self._operator} ({self._operation}) "


class NotOperation(LogicalOperation):
    """
    Not logical operation

    - field: NOT field = 1
    - operation: NOT (<operation>)
    """

    def __init__(self, operation: str):
        super().__init__("NOT", operation)


class AndOperation(LogicalOperation):
    """
    And logical operation

    - field: AND field = 1
    - operation: AND (<operation>)
    """

    def __init__(self, operation: str):
        super().__init__("AND", operation)


class OrOperation(LogicalOperation):
    """
    Or logical operation

    - field: OR field = 1
    - operation: OR (<operation>)
    """

    def __init__(self, operation: str):
        super().__init__("OR", operation)


class OrderOperation(SQLOperation):
    """
    Order operation (ORDER BY <field or fields> <ASC or DESC>)
    """

    def __init__(self, direction: str, fields: Union[str, List[str]]):
        """
        Constructor
        """
        self._direction = direction
        if isinstance(fields, str):
            self._fields = [FIELD_WRAPPER % fields if fields != "1" else fields]
        else:
            # fields validation
            if len(fields) == 0:
                self._fields = ["1"]
            else:
                self._fields = []
                for field in fields:
                    self._fields.append(FIELD_WRAPPER % field)

    def resolve(self) -> str:
        """
        Implemented resolver operation
        """
        return f"ORDER BY {', '.join(self._fields)} {self._direction} "
