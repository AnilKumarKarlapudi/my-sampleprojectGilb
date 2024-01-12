import ctypes
from typing import Any
from typing import Optional
from ctypes import wintypes
import win32con

# Kernel32 DLL object
K32DLL: ctypes.WinDLL = ctypes.windll.kernel32

# ADVAPI32 DLL object
AD32DLL: ctypes.WinDLL = ctypes.windll.advapi32

# #define SYSTEM32 "C:\\Windows\\System32"
SYSTEM32 = "C:\\Windows\\System32"

# #define NULL  (void*) 0L
NULL = 0

# #define TRUE 1
TRUE = 1

# #define FALSE 0
FALSE = 0


def _cast(value: Optional[Any], st):
    if value is None:
        return NULL
    return st(value)


# #define CAST(val, st) (val == NULL ? NULL : (st) val)
CAST = _cast

# typedef unsigned short WORD;
WORD = wintypes.WORD

# typedef unsigned int DWORD;
DWORD = wintypes.DWORD

# typedef char* LPSTR;
LPSTR = wintypes.LPSTR

LPWSTR = wintypes.LPWSTR

# typedef LPSTR LPBYTE;
LPBYTE = wintypes.LPBYTE


# typedef unsigned int HANDLE;
class HANDLE(wintypes.HANDLE):
    def detach(self):
        handle, self.value = self.value, None
        return wintypes.HANDLE(handle)

    def close(self):
        if self:
            K32DLL.CloseHandle(self.detach())

    def __del__(self):
        self.close()


# ?
HANDLE_FLAG_INHERIT = win32con.HANDLE_FLAG_INHERIT

# ?
STARTF_USESTDHANDLES = win32con.STARTF_USESTDHANDLES
