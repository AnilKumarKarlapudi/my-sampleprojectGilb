import re
from typing import List

from libs.infra.db.errors import SQLError
from libs.infra.db.schemas import DatasourceProperties, SQLRecord
from libs.infra.io.command import CommandResult
from libs.infra.io.command import CommandWithCredentials


class SQLCommand(CommandWithCredentials):
    """
    SQL Command interface
    """

    ds_props: DatasourceProperties
    statement: str
    use_shell: bool = False

    @classmethod
    def ok(cls, result: CommandResult) -> bool:
        """
        Check if result is OK (has affected rows)

        :param result: CommandResult - execution result
        :return: bool - if command has affected rows
        """
        has_affected_rows = re.search(r"(\(\d+ rows affected\)\n)", result.output)
        return result.ok and has_affected_rows is not None

    def __init__(self, statement: str, ds_properties: DatasourceProperties, shell: bool = False):
        """
        Constructor

        :param statement: str - sql statement
        :param ds_properties: DatasourceProperties - datasource properties
        :param shell: flag to use shell on command
        """
        self.shell = shell
        self.statement = statement
        self.ds_properties = ds_properties
        super().__init__(self.create_command(), ds_properties.user)

    def create_command(self) -> str:
        """
        Create the SQL command

        :return: str - full command to be executed
        """
        command = f"sqlcmd.exe -S {self.ds_properties.server} -l 50 -E -Q "
        if self.shell:
            command += f"\"xp_cmdshell '{self.statement}'\""
        else:
            if not self.ds_properties.database:
                raise ValueError("database is mandatory when not using xp_cmdshell")
            command += f'-d {self.ds_properties.database} -E -Q "{self.statement}"'
        return command

    def run(self, *args, **kwargs) -> CommandResult:
        """
        Disabled method
        """
        raise NotImplementedError("use execute() instead")

    def execute(self) -> bool:
        """
        Execute command

        :return: bool - is
        """
        result = super().run()
        return self.ok(result)

    def perform(self) -> CommandResult:
        return super().run()


class SQLQueryCommand(SQLCommand):
    """
    SQL Query Command implementation
    """

    # Override
    def create_command(self) -> str:
        """
        Create the SQL command

        :return: str - full command to be executed
        """
        command = f"sqlcmd.exe -S {self.ds_properties.server} -l 50 -W -s ~ "
        if self.shell:
            command += f"-E -Q \"xp_cmdshell '{self.statement}'\""
        else:
            if not self.ds_properties.database:
                raise ValueError("database is mandatory when not using xp_cmdshell")
            command += f'-d {self.ds_properties.database} -E -Q "{self.statement}"'
        return command

    # Override
    def execute(self) -> bool:
        """
        Disable method
        """
        raise NotImplementedError("use .perform() instead for SQLQueryCommand")

    def perform(self) -> List[SQLRecord]:
        """
        Execute and converts result to a list of SQLRecord

        :return:
        """
        return self._convert(super().perform())

    def _convert(self, result: CommandResult) -> List[SQLRecord]:
        """
        Convert CommandResult to a List of SQLRecord

        :param result: CommandResult - command result
        :return: List[SQLRecord] - records
        """
        if not self.ok(result):
            self.log.error(f"Execution has errors: {result}")
            raise SQLError("execution has errors")

        start = result.output.find("\n--")
        end = result.output.find("--\n") + 2

        output = str(result.output[:start]) + str(result.output[end:])
        output = output.split("\n")

        columns = output[0].split("~")

        records = []
        for row in output[1:][:-3]:
            row = row.split("~")
            records.append(SQLRecord(columns, dict(zip(columns, row))))

        return records
