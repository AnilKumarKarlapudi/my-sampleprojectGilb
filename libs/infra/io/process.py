import ctypes
from typing import AnyStr
from typing import Optional
from typing import Tuple

import win32con

from libs.infra.c.header import AD32DLL
from libs.infra.c.header import CAST
from libs.infra.c.header import FALSE
from libs.infra.c.header import K32DLL
from libs.infra.c.header import NULL
from libs.infra.c.header import STARTF_USESTDHANDLES
from libs.infra.c.header import SYSTEM32
from libs.infra.c.structs import c_process_info_t
from libs.infra.c.structs import c_startup_info_t
from libs.infra.io.pipe import IOPipe
from libs.infra.io.system.user import SystemUser


class IOProcess(object):
    """
    IOProcess interface
    """

    def __init__(self, command: AnyStr):
        """
        Constructor

        :param command: AnyStr - command string
        """
        # Pipes
        self._stdout = IOPipe()
        self._stderr = IOPipe()

        # Startup Info struct
        self.startup_info = c_startup_info_t()
        self.startup_info.dwFlags = STARTF_USESTDHANDLES
        self.startup_info.hStdOutput = self._stdout.writer
        self.startup_info.hStdError = self._stderr.writer

        # Process Info struct
        self.process_info = c_process_info_t()

        # Success flag
        self._success = None

        # Command string
        self.command = command

    def close(self):
        """
        Close pipes and pointers
        """
        # Close pipes
        self._stderr.close()
        self._stdout.close()

        # Close pointers
        K32DLL.CloseHandle(self.process_info.hThread)

    def read(self, ignore_stdout: bool = False, ignore_stderr: bool = False) -> Tuple[Optional[str], Optional[str]]:
        """
        Read from pipes

        :param ignore_stdout: bool - flag to ignore stdout result
        :param ignore_stderr: bool - flag to ignore stderr result
        :return: Tuple[Optional[str], Optional[str]] - tuple of stdout and stderr result
        """
        # Close pointers
        K32DLL.CloseHandle(self.process_info.hThread)
        K32DLL.CloseHandle(self._stdout.writer)
        K32DLL.CloseHandle(self._stderr.writer)

        output = None
        if not ignore_stdout:
            # Read from stdout
            output = self._stdout.read()

        error = None
        if not ignore_stderr:
            # Read from stderr
            error = self._stderr.read()

        return output, error

    @property
    def success(self) -> bool:
        """
        Check if the process has success

        :raises ValueError: on calling before call to .run()
        :return: bool - has success
        """
        if self._success is None:
            raise ValueError("process was not run yet")
        return self._success != FALSE

    @property
    def pid(self) -> int:
        """
        Get process identifier from the Process Info structure

        :return: int - process identifier
        """
        return self.process_info.dwProcessId

    def run(self):
        """
        Abstract method to be implemented: execute process
        """
        raise NotImplementedError("run has to be implemented")


class IOProcessWithCredentials(IOProcess):
    """
    IOProcess with credentials
    """

    def __init__(self, owner: SystemUser, command: AnyStr):
        """
        Constructor

        :param owner: SecureUser - owner of the process
        :param command: AnyStr - command
        """
        super().__init__(command)
        self._owner = owner

    def run(self):
        """
        Execute process for a certain user and domain.
        """
        username = CAST(self._owner.username, ctypes.c_wchar_p)
        domain = CAST(self._owner.domain, ctypes.c_wchar_p)
        password = CAST(self._owner.password, ctypes.c_wchar_p)
        command = ctypes.byref(CAST(self.command, ctypes.create_unicode_buffer))
        self._success = AD32DLL.CreateProcessWithLogonW(username,
                                                        domain,
                                                        password,
                                                        NULL,
                                                        NULL,
                                                        command,
                                                        win32con.CREATE_UNICODE_ENVIRONMENT,
                                                        NULL,
                                                        ctypes.c_wchar_p(SYSTEM32),
                                                        ctypes.byref(self.startup_info),
                                                        ctypes.byref(self.process_info))
