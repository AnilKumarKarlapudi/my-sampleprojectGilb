import ctypes
import msvcrt
import os

from libs.infra.c.header import FALSE
from libs.infra.c.header import HANDLE
from libs.infra.c.header import HANDLE_FLAG_INHERIT
from libs.infra.c.header import K32DLL


class IOPipe(object):
    def __init__(self):
        writer = HANDLE()
        reader = HANDLE()

        # void CreatePipe(void*, void*, void*, uint_t)
        if K32DLL.CreatePipe(ctypes.byref(reader), ctypes.byref(writer), None, 0) == FALSE:
            raise WindowsError("unable to create pipe")

        if K32DLL.SetHandleInformation(writer, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT) == FALSE:
            raise WindowsError("unable to set handle information to pipe")

        self._reader = reader
        self._writer = writer

    def close(self):
        K32DLL.CloseHandle(self._reader.value)
        K32DLL.CloseHandle(self._writer.value)

    @property
    def writer(self):
        return self._writer

    @property
    def reader(self):
        return self._reader

    def read(self):
        fd = msvcrt.open_osfhandle(self._reader.value, os.O_RDONLY | os.O_TEXT)
        with os.fdopen(fd, 'r') as out:
            return out.read()
