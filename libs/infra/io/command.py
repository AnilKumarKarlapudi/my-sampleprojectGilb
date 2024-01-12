import ctypes
import logging
from typing import AnyStr
from typing import Optional

from libs.infra.io.process import IOProcess
from libs.infra.io.process import IOProcessWithCredentials
from libs.infra.io.system.user import SystemUser


class CommandResult(object):
    """
    Command Result object
    """
    pid: int
    output: Optional[str] = None
    error: Optional[str] = None

    def __init__(self, pid: int, output: Optional[str] = None, error: Optional[str] = None):
        """
        Constructor

        :param pid: int - process identifier
        :param output: Optional[str] - output result text
        :param error: Optional[str] - error result text
        """
        self.pid = pid
        self.output = output
        self.error = error

    @property
    def ok(self) -> bool:
        """
        Check if result is ok (PID has to be greater than 0)

        :return: bool - success of the process
        """
        return self.pid > 0

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)


class Command(object):
    """
    Command interface
    """
    command: str

    def __init__(self, command: AnyStr):
        """
        Constructor

        :param command: AnyStr - string command
        """
        self.command = command
        self.log = logging.getLogger(Command.__name__)

    def run(self, ignore_stdout: bool = False, ignore_stderr: bool = False) -> CommandResult:
        """
        Execute command

        :param ignore_stdout: bool - flag to ignore the stdout result
        :param ignore_stderr: bool - flag to ignore the stderr result
        :raises ConnectionError: on any exception while running the command
        :return: CommandResult
        """
        process = self.process()
        try:
            self.log.debug(f"Executing command: {self.command}")

            process.run()

            if not process.success:
                # If the process fails, then windows will get the last error and raises it
                raise ctypes.WinError()

        except OSError as ex:
            if process:
                process.close()

            self.log.error(f"Unable to execute command: {self.command}")

            # If an exception was raise, then re-raise the exception
            raise ConnectionError(f"cannot execute command: {self.command}") from ex

        output, error = process.read(ignore_stdout=ignore_stdout, ignore_stderr=ignore_stderr)
        if process:
            process.close()

        self.log.debug(f"Command has been executed: {self.command}")
        return CommandResult(process.pid, output, error)

    def process(self, *args, **kwargs) -> IOProcess:
        """
        Abstract create process with arguments

        :param args: positional arguments
        :param kwargs: named arguments
        :return: IOProcess - process
        """
        raise NotImplementedError("process has to be implemented")


class CommandWithCredentials(Command):
    """
    Command With Credentials implementation
    """

    def __init__(self, command: AnyStr, owner: SystemUser):
        """
        Constructor

        :param command: AnyStr - command string
        :param owner: SecureUser - owner
        """
        super().__init__(f"cmd.exe /C {command}")
        self._owner = owner

    def process(self, *args, **kwargs) -> IOProcess:
        """
        Create process for IOProcessWithCredentials

        :param args: positional arguments
        :param kwargs: named arguments
        :return: IOProcessWithCredentials - process with owner
        """
        return IOProcessWithCredentials(self._owner, self.command)
