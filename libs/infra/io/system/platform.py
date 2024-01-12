from libs.infra.io.system.constants import RegisterKeys
from winreg import HKEY_LOCAL_MACHINE, KEY_ALL_ACCESS
from winreg import OpenKey
from winreg import QueryValueEx


def get_brand() -> str:
    """
    Get the brand name from the Windows registry.
    """
    register = OpenKey(HKEY_LOCAL_MACHINE, RegisterKeys.PASSPORT, 0, KEY_ALL_ACCESS)
    return str(QueryValueEx(register, 'BrandSelected')[0]).upper()


def get_version() -> str:
    """
    Get the version of the system from the Windows registry.
    """
    key = OpenKey(HKEY_LOCAL_MACHINE, RegisterKeys.PASSPORT, 0, KEY_ALL_ACCESS)
    version = str(QueryValueEx(key, 'Version')[0])
    version = version.strip()

    try:
        maintenance = QueryValueEx(key, 'MaintenancePack')[0]
        if maintenance:
            version += f" {str(maintenance).strip()}"
    except (FileNotFoundError, IOError, WindowsError):
        pass

    return version
