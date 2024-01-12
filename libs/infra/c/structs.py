import ctypes

from libs.infra.c.header import DWORD
from libs.infra.c.header import HANDLE
from libs.infra.c.header import LPWSTR
from libs.infra.c.header import LPBYTE
from libs.infra.c.header import WORD


class _StartupInfo(ctypes.Structure):
    """
    Wrapper for startup_info c structure:

    #pragma pack(1)
    struct startup_info
    {
        DWORD cb;
        DWORD lpReserved;
        LPSTR lpDesktop;
        LPSTR lpTitle;
        DWORD dwX;
        DWORD dwY;
        DWORD dwXSize;
        DWORD dwYSize;
        DWORD dwXCountChars;
        DWORD dwYCountChars;
        DWORD dwFillAttribute;
        DWORD dwFlags;
        DWORD wShowWindow;
        WORD cbReserved2;
        DWORD lpReserved2;
        DWORD hStdInput;
        DWORD hStdOutput;
        DWORD hStdError;
    }
    """
    _fields_ = (
        ('cb', DWORD),
        ('lpReserved', LPWSTR),
        ('lpDesktop', LPWSTR),
        ('lpTitle', LPWSTR),
        ('dwX', DWORD),
        ('dwY', DWORD),
        ('dwXSize', DWORD),
        ('dwYSize', DWORD),
        ('dwXCountChars', DWORD),
        ('dwYCountChars', DWORD),
        ('dwFillAttribute', DWORD),
        ('dwFlags', DWORD),
        ('wShowWindow', WORD),
        ('cbReserved2', WORD),
        ('lpReserved2', LPBYTE),
        ('hStdInput', HANDLE),
        ('hStdOutput', HANDLE),
        ('hStdError', HANDLE)
    )

    def __init__(self, *args, **kwargs):
        self.cb = ctypes.sizeof(self)
        super().__init__(*args, **kwargs)


class _ProcessInfo(ctypes.Structure):
    """
    Wrapper for process_info c struct

    #pragma pack(1)
    struct process_info
    {
        HANDLE hProcess;
        HANDLE hThread;
        DWORD dwProcessId;
        DWORD dwThreadId;
    }
    """
    _fields_ = (
        ('hProcess', HANDLE),
        ('hThread', HANDLE),
        ('dwProcessId', DWORD),
        ('dwThreadId', DWORD)
    )


# struct startup_info alias
c_startup_info_t = _StartupInfo

# struct startup_info alias
c_process_info_t = _ProcessInfo
