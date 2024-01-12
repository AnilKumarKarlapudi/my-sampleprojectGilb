import pytest

from libs.infra.io.command import Command
from libs.infra.io.command import CommandWithCredentials
from libs.infra.io.system.user import SystemUser

# OS Command
COMMAND_IPCONFIG = "ipconfig"

# System User
OWNER = SystemUser()


def test_command_not_implemented_error():
    """
    IO Command is not implemented error test
    """
    command = Command(COMMAND_IPCONFIG)
    with pytest.raises(NotImplementedError):
        command.run()


def test_command_with_credentials_ok():
    """
    IO Command with credentials OK test
    """
    command = CommandWithCredentials(COMMAND_IPCONFIG, OWNER)
    result = command.run()
    assert result.ok


def test_command_with_credentials_check_result_ok():
    """
    IO Command with credentials check result is OK test
    """
    command = CommandWithCredentials("echo 'OK'", OWNER)
    result = command.run()
    assert result.ok
