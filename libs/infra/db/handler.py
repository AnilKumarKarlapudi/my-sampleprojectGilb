import logging
from typing import Any, Optional, List, Type

from libs.infra.db.command import SQLCommand
from libs.infra.db.command import SQLQueryCommand
from libs.infra.db.errors import CannotResolveStatementError, UnsupportedPythonTypeForFieldError
from libs.infra.db.models import Model
from libs.infra.db.queries import Q
from libs.infra.db.queries import QResolver
from libs.infra.db.queries import Select
from libs.infra.db.schemas import DatasourceProperties
from libs.infra.db.schemas import SQLRecord
from libs.infra.db.utils import prepare_statement


class DatasourceHandler:
    """
    Datasource Handler
    """

    properties: DatasourceProperties

    model: Type[Model]

    def __init__(self, enable_sql_logging: bool = True):
        self.enable_sql_logging = enable_sql_logging
        self.sql_logger = logging.getLogger("SQL Execution")
        self.log = logging.getLogger(DatasourceHandler.__name__)

    def find(self, pk: Any) -> Optional[Model]:
        """
        Find a Model by its primary key.

        :param pk: Any - model's primary key
        :returns: Optional[Model] - model if found
        """
        query = Q(self.model).select().eq(self.model.META.pk.field, pk).limit(1).resolve()
        result = self._query(query)
        if len(result) > 0:
            return self.model.loads(result[0])

    def query(self, query: Select) -> List[Model]:
        """
        Performs a SQL select by given query object.

        :param query: Select - query object
        :return: List[Model] - query set result mapped to Model
        """
        result = []
        for record in self._query(query.resolve()):
            result.append(self.model.loads(record))
        return result

    def execute(self, query: QResolver) -> bool:
        """
        Executes a SQL command by given query object.

        :param query: QResolver - query object
        :return: bool - statement result
        """
        return self._execute(query.resolve())

    def _query(self, query: str, *args, **kwargs) -> List[SQLRecord]:
        """
        Executes a query and then maps the result to a SQLRecord list.

        :param query: str - sql unsafe query
        :param args: positional args for query
        :param kwargs: named args for query
        :raises CannotResolveStatementError: on prepare_statement failure
        :raises SQLError: after executing the command
        :returns: List[SQLRecord] - list of SQLRecords (can be empty)
        """
        try:
            statement = prepare_statement(query, *args, **kwargs)

            self._log_statement(statement)

            command = SQLQueryCommand(statement, self.properties)
            return command.perform()

        except (IndexError, UnsupportedPythonTypeForFieldError) as ex:
            # Error while preparing the statement
            raise CannotResolveStatementError(query) from ex

    def _execute(self, statement: str, *args, **kwargs) -> bool:
        """
        Executes a SQL command (UPDATE, INSERT, CALL, DELETE) by a given statement

        :param statement: SQL raw and unsafe statement
        :param args: positional args for query
        :param kwargs: named args for query
        :raises CannotResolveStatementError: on prepare_statement failure
        :returns: bool - failure or success of the command
        """
        try:
            secure_statement = prepare_statement(statement, *args, **kwargs)

            self._log_statement(secure_statement)

            command = SQLCommand(secure_statement, self.properties)
            return command.execute()

        except (IndexError, UnsupportedPythonTypeForFieldError) as ex:
            # Error while preparing the statement
            raise CannotResolveStatementError(statement) from ex

    def _log_statement(self, statement: str):
        """
        Log (if enabled) the given statement.

        :param statement: raw sql statement to be logged
        """
        if self.enable_sql_logging:
            # Logs to INFO level, in case we disable the DEBUG level
            self.sql_logger.info(statement)


def get_datasource(model: Type[Model], properties: DatasourceProperties) -> DatasourceHandler:
    """
    Creates and get a new datasource for a given model and a given properties.

    :param model: Type[Model] - model class
    :param properties: DatasourceProperties - properties
    :return: DatasourceHandler - new datasource handler
    """
    ds = DatasourceHandler()
    ds.model = model
    ds.properties = properties
    return ds
