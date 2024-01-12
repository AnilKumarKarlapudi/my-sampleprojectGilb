import pytest

from libs.infra.io.process import IOProcess
from libs.infra.io.process import IOProcessWithCredentials
from libs.infra.io.system.user import SystemUser

OWNER = SystemUser()

COMMAND_IPCONFIG = "ipconfig"


def test_run_process_no_implemented_error():
    """
    IO Process no implemented error test
    """
    process = IOProcess(COMMAND_IPCONFIG)
    with pytest.raises(NotImplementedError):
        process.run()


def test_run_process_with_credentials_ask_for_success_before_run_error():
    """
    IO Process with credentials success test
    """
    process = IOProcessWithCredentials(OWNER, COMMAND_IPCONFIG)
    with pytest.raises(ValueError):
        assert process.success


def test_run_process_ipconfig_locally_ok():
    """
    IO Process with credentials run success test
    """
    process = IOProcessWithCredentials(OWNER, COMMAND_IPCONFIG)
    process.run()
    assert process.success
