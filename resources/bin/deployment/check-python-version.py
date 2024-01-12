import logging
import os
import os.path
import subprocess
import sys
from pathlib import WindowsPath
from typing import Tuple, Union, List, Optional

PYTHON_REQUIRED_VERSION = (3, 10)

logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s  [%(levelname)-10s] %(funcName)-25s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
log = logging.getLogger('env-setup')

PYTHON_LOCATION = "D:\\Python"
INSTALLER_LOCATION = WindowsPath(os.path.abspath(__file__)).parent.parent.parent / "python" / "installer.exe"


def check_version_major_minor(version: Union[List, Tuple]) -> bool:
    major = version[0]
    minor = version[1]

    return major == PYTHON_REQUIRED_VERSION[0] and minor == PYTHON_REQUIRED_VERSION[1]


def install_required_version():
    flags = [
        "/passive",
        "AssociateFiles=0",
        "Shortcuts=0",
        "Include_launcher=0",
        "InstallLauncherAllUsers=0",
        "SimpleInstall=1",
        f"TargetDir={PYTHON_LOCATION}"
    ]
    command = f"{INSTALLER_LOCATION.absolute()} {' '.join(flags)}"

    log.info(f"Installing required python version: {command}")

    if os.system(command) == 0:
        log.info((
            f"Python {'.'.join([str(c) for c in PYTHON_REQUIRED_VERSION])} "
            f"interpreter successfully installed in: {PYTHON_LOCATION}"
        ))
    else:
        log.error("An unexpected error has occurred while installing the required python interpreter")
        sys.exit(2)


def check_for_binaries() -> Tuple[bool, Optional[WindowsPath]]:
    current_user = os.getlogin()
    required_version = "".join(str(c) for c in PYTHON_REQUIRED_VERSION)

    expected_python_locations = os.environ['PATH'].split(";")
    expected_python_locations.extend([
        PYTHON_LOCATION,
        f"C:\\Users\\{current_user}\\AppData\\Local\\Programs\\Python\\Python{required_version}"
    ])

    for path in expected_python_locations:
        path = WindowsPath(path) / "python.exe"
        if path.exists():
            command = f"{path} -c \"import sys; print(list(sys.version_info))\""
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
            process.wait()
            version = str(process.stdout.read(), 'utf-8').strip()
            version = eval(version)
            if check_version_major_minor(version):
                return True, path
    log.error("No binaries were found for required python version...")
    return False, None


def check_current_version() -> Tuple[bool, str]:
    same_version = True
    source = "version"

    current_version = sys.version_info
    if not check_version_major_minor(current_version):
        log.error(f"Difference in versions, expecting {PYTHON_REQUIRED_VERSION}, got: {current_version}")
        same_version = False

    if not same_version:
        log.info("Checking if exist binaries for required version in path...")
        same_version, source = check_for_binaries()

    return same_version, source


def main():
    is_required_version, source = check_current_version()
    if not is_required_version:
        install_required_version()
    else:
        log.info("Python version meets required version!")
    sys.exit(0)


if __name__ == '__main__':
    main()
