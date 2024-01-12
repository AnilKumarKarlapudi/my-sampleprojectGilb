import pytest

from libs.infra.db.command import SQLQueryCommand
from libs.infra.db.schemas import DatasourceProperties
from libs.infra.db.errors import SQLError
from libs.infra.io.system.user import SystemUser


OK_QUERY = "SELECT 'OK' as MESSAGE"
ERR_QUERY = "SELECT * FROM TABLE_DOES_NOT_EXIST"
USER = SystemUser(username="PassportTech", password="911Tech", domain="passport")


def get_ds_properties():
    """
    Datasource Properties
    """
    properties = DatasourceProperties()
    properties.user = USER
    properties.server = "POSSERVER01"
    properties.database = "GlobalSTORE"
    return properties


def test_sql_query_command_use_bad_contract_error():
    """
    DB SQL Query command bad contract error
    """
    command = SQLQueryCommand(OK_QUERY, get_ds_properties())
    with pytest.raises(NotImplementedError):
        command.run()


def test_sql_query_command_ok():
    """
    DB SQL Query command OK
    """
    command = SQLQueryCommand(OK_QUERY, get_ds_properties())
    result = command.perform()

    assert len(result) > 0
    assert result[0].record['MESSAGE'] == 'OK'


def test_sql_query_command_error():
    """
    DB SQL Query command error
    """
    command = SQLQueryCommand(ERR_QUERY, get_ds_properties())
    with pytest.raises(SQLError):
        command.perform()
