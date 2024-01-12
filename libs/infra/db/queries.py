from typing import Type, List

from libs.infra.db.errors import CannotResolveStatementError
from libs.infra.db.models import Model
from libs.infra.db.operations import EqualOperation
from libs.infra.db.predicates import QPredicate
from libs.infra.db.predicates import QResolver
from libs.infra.db.utils import SQLSupportedTypes


class F(QPredicate):
    """
    Handler for concatenate queries or sub queries.
    """
    pass


class Q(object):
    """
    Handler for Queries.
    """

    def __init__(self, model: Type[Model]):
        """
        Constructor
        """
        self._model = model

    def select(self) -> "Select":
        """
        Creates a Select object
        """
        return Select(self._model)

    def update(self) -> "Update":
        """
        Creates an Update object
        """
        return Update(self._model)

    def insert(self) -> "Insert":
        """

        """
        return Insert(self._model)


class Select(QPredicate):
    """
    Select QPredicate object
    """

    def __init__(self, model: Type[Model]):
        """
        Constructor
        """
        super().__init__()

        self._model = model
        self._limit = None

    def limit(self, count: int) -> "Select":
        """
        Sets a limit for retrieving records.
        """
        if count > 0:
            if self._limit is None:
                self._limit = count
            else:
                raise ValueError("limit has been already set, cannot override")
        else:
            raise ValueError("limit must be greater than 0")
        return self

    def resolve(self) -> str:
        """
        Generates a SQL SELECT
        """
        query = (
            f"SELECT {'TOP ' + str(self._limit) if self._limit != 0 else ''} * "
            f"FROM {self._model.META.table_name} "
            f"WHERE {super().resolve()}"
        )
        return self.build(self._model, query)


class Update(QResolver):
    """
    Update QResolver object
    """

    def __init__(self, model: Type[Model]):
        """
        Constructor
        """
        super().__init__()

        self._model = model
        self._fields = {}
        self._where = None

    def set(self, field: str, value: SQLSupportedTypes) -> "Update":
        """
        Set new value to field
        """
        if self._where is not None:
            raise ValueError("cannot set values after 'where'")

        if field in self._fields:
            raise ValueError(f"{field} field already set, cannot override")

        self._fields[field] = EqualOperation(field, value).resolve()
        return self

    def where(self, where: F) -> "Update":
        """
        Set where condition to predicate
        """
        if self._where is not None:
            # Can't override where
            raise ValueError("where has been already set, cannot override")

        if len(self._fields) == 0:
            # Can't create 'where' before setting fields
            raise ValueError("missing changes before 'where'")

        self._where = where
        return self

    def resolve(self) -> str:
        """
        Implement resolve
        """
        if len(self._fields) == 0:
            raise CannotResolveStatementError("fields are not set")

        if self._where is None:
            raise CannotResolveStatementError("where condition is not set")

        fields = ", ".join(list(self._fields.values()))
        condition = self._where.resolve()

        query = f"UPDATE {self._model.META.table_name} " f"SET {fields} " f"WHERE {condition}"
        return self.build(self._model, query)


class Delete(QResolver):
    """
    Delete QResolver object
    """

    def __init__(self, model: Type[Model]):
        """
        Constructor
        """
        super().__init__()

        self._model = model
        self._where = None

    def where(self, where: QPredicate) -> "Delete":
        """
        Set where condition to predicate
        """
        if self._where is not None:
            # Can't override where
            raise ValueError("where has been already set, cannot override")

        self._where = where
        return self

    def resolve(self) -> str:
        """
        Implement resolve
        """
        if self._where is None:
            raise CannotResolveStatementError("where condition is not set")

        condition = self._where.resolve()

        query = (
            f"DELETE FROM {self._model.META.table_name} WHERE {condition}"
        )

        return self.build(self._model, query)


class Insert(QResolver):
    """
    TODO: implement me
    Insert QResolver object
    """

    def __init__(self, model: Type[Model]):
        """
        Constructor
        """
        super().__init__()

        self._model = model
        self._values = []

    def values(self, values: List[Model]) -> "Insert":
        """
        Add values(models) to be inserted
        """
        for value in values:
            if not isinstance(value, self._model):
                raise ValueError(f"{value} is not an instance of {self._model}")
            self._values.append(value)
        return self

    def resolve(self) -> str:
        """
        TODO: implement this, keep in mind the PK auto incremental or if it's required the PK for the model
        """
        raise NotImplementedError("yet to implement")
