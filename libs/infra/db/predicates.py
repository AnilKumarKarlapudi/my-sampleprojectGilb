from typing import List
from typing import Type
from typing import Union
from typing import Optional

from libs.infra.db.constants import FIELD_WRAPPER_RE
from libs.infra.db.models import Model
from libs.infra.db.operations import AndOperation
from libs.infra.db.operations import EqualOperation
from libs.infra.db.operations import GreaterThanOperation
from libs.infra.db.operations import GreaterThanOrEqualOperation
from libs.infra.db.operations import InOperation
from libs.infra.db.operations import LikeOperation
from libs.infra.db.operations import LowerThanOperation
from libs.infra.db.operations import LowerThanOrEqualOperation
from libs.infra.db.operations import NotOperation
from libs.infra.db.operations import OrOperation
from libs.infra.db.operations import OrderOperation
from libs.infra.db.operations import SQLOperation
from libs.infra.db.operations import YesNoOperation
from libs.infra.db.utils import SQLComparisonTypes
from libs.infra.db.utils import SQLSupportedTypes


class QResolver(object):
    """
    QResolver stands for an interface to force implementations to implement a resolve method
    """

    def resolve(self) -> str:
        """
        Resolve unimplemented method.
        """
        raise NotImplementedError()

    def build(self, model: Type[Model], query: Optional[str] = None) -> str:
        """
        Replace all wrapped fields in the given token by using their column name from the given Model class.

        :param model: Type[Model] - Model class
        :param query: Optional[str] - override query
        :return: str - query built
        """
        if query is None:
            query = self.resolve()

        for wrapped_field, field in FIELD_WRAPPER_RE.findall(query):
            query = query.replace(wrapped_field, model.META.get_column_name(field))

        return query


class QPredicate(QResolver):
    """
    QPredicate is a subclass implementation of QResolver
    """

    def __init__(self):
        """
        Constructor of QPredicate
        """
        self._chain = []

    def eq(self, field_name: str, value: SQLSupportedTypes) -> "QPredicate":
        """
        Equals operation

        Does not get inserted in the chain if it's not the first operation in the chain.
        """
        if len(self._chain) == 0:
            self._chain.append(EqualOperation(field_name, value))
        return self

    def gt(self, field_name: str, value: SQLComparisonTypes) -> "QPredicate":
        """
        Greater than operation

        Does not get inserted in the chain if it's not the first operation in the chain.
        """
        if len(self._chain) == 0:
            self._chain.append(GreaterThanOperation(field_name, value))
        return self

    def lt(self, field_name: str, value: SQLComparisonTypes) -> "QPredicate":
        """
        Lower than operation

        Does not get inserted in the chain if it's not the first operation in the chain.
        """
        if len(self._chain) == 0:
            self._chain.append(LowerThanOperation(field_name, value))
        return self

    def gte(self, field_name: str, value: SQLComparisonTypes) -> "QPredicate":
        """
        Greater than or equal operation

        Does not get inserted in the chain if it's not the first operation in the chain.
        """
        if len(self._chain) == 0:
            self._chain.append(GreaterThanOrEqualOperation(field_name, value))
        return self

    def lte(self, field_name: str, value: SQLComparisonTypes) -> "QPredicate":
        """
        Lower than or equal operation

        Does not get inserted in the chain if it's not the first operation in the chain.
        """
        if len(self._chain) == 0:
            self._chain.append(LowerThanOrEqualOperation(field_name, value))
        return self

    def like(self, field_name: str, pattern: str) -> "QPredicate":
        """
        Like operation

        Does not get inserted in the chain if it's not the first operation in the chain.
        """
        if len(self._chain) == 0:
            self._chain.append(LikeOperation(field_name, pattern))
        return self

    def in_(self, field_name: str, values: List[SQLSupportedTypes]) -> "QPredicate":
        """
        In operation

        Does not get inserted in the chain if it's not the first operation in the chain.
        """
        if len(self._chain) == 0:
            self._chain.append(InOperation(field_name, values))
        return self

    def true(self, field_name: str) -> "QPredicate":
        """
        Is true operation

        Does not get inserted in the chain if it's not the first operation in the chain.
        """
        if len(self._chain) == 0:
            self._chain.append(YesNoOperation(field_name))
        return self

    def false(self, field_name: str) -> "QPredicate":
        """
        Is false operation

        Does not get inserted in the chain if it's not the first operation in the chain.
        """
        if len(self._chain) == 0:
            self._chain.append(YesNoOperation(field_name, yes=False))
        return self

    def not_(self, predicate: "QPredicate") -> "QPredicate":
        """
        Not operation

        Does not get inserted in the chain if it's not the first operation in the chain.
        """
        if len(self._chain) == 0:
            self._chain.append(NotOperation(predicate.resolve()))
        return self

    def and_(self, predicate: "QPredicate") -> "QPredicate":
        """
        AND operator

        Does not get inserted in the chain if it's the first operation in the chain.
        """
        if len(self._chain) > 0:
            last_operation = self._chain[-1]
            if not isinstance(last_operation, OrderOperation):
                self._chain.append(AndOperation(predicate.resolve()))
        return self

    def or_(self, predicate: "QPredicate") -> "QPredicate":
        """
        OR operator

        Does not get inserted in the chain if it's the first operation in the chain.
        """
        if len(self._chain) > 0:
            last_operation = self._chain[-1]
            if not isinstance(last_operation, OrderOperation):
                self._chain.append(OrOperation(predicate.resolve()))
        return self

    def asc(self, field_names: Union[str, List[str]] = "1") -> "QPredicate":
        """
        ORDER BY [ASC] operation

        Does not get inserted in the chain if it's the first operation in the chain or if there is already another
        ordering operator in the chain.
        """
        if len(self._chain) == 0:
            return self

        if not any([isinstance(op, OrderOperation) for op in self._chain]):
            self._chain.append(OrderOperation("ASC", field_names))
        return self

    def desc(self, field_names: Union[str, List[str]] = "1") -> "QPredicate":
        """
        ORDER BY [ASC] operation

        Does not get inserted in the chain if it's the first operation in the chain or if there is already another
        ordering operator in the chain.
        """
        if len(self._chain) == 0:
            return self

        if not any([isinstance(op, OrderOperation) for op in self._chain]):
            self._chain.append(OrderOperation("DESC", field_names))
        return self

    def resolve(self) -> str:
        """
        Creates a predicate from the inner chain of operations.
        """
        where = ""
        while len(self._chain) > 0:
            op: SQLOperation = self._chain.pop(0)
            where += op.resolve()
        return where
