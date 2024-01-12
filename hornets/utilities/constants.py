import os.path
import platform
import hornets
from pathlib import WindowsPath

BASE_DIR = WindowsPath(os.path.abspath(hornets.__file__)).parent.parent

RESOURCES_DIR = BASE_DIR / "resources"
HORNETS_DIR = BASE_DIR / "hornets"
SECURITY_DIR = RESOURCES_DIR / "security"
SECURITY_CERTS_DIR = SECURITY_DIR / "certs"
SECURITY_GRPC_DIR = SECURITY_CERTS_DIR / "grpc"

TIME_BETWEEN_FIELDS = 0.1
TIME_BETWEEN_KEY = 0.1
TIME_BETWEEN_CLICK = 0.2
MAX_IMPLICIT_TIME_TO_WAIT = 8
MAX_EXPLICIT_TIME_TO_WAIT = 4
MAX_TIMEOUT_FOR_TRANSACTION = 20

# Valid Credentials
CREDENTIALS = {'username': '91', 'password': '91'}

# Chrome
CHROME_SELECTORS_HUB_EXTENSION = RESOURCES_DIR / "chrome" / "chrome_extension" / "extension_5_1_0_0.crx"
CHROME_WEBDRIVER_EXECUTABLE = RESOURCES_DIR / "chrome" / "webdriver" / "chromedriver.exe"

# Registry
if '7' in platform.release():
    PASSPORT_SUBKEY = r"SOFTWARE\Gilbarco\Passport"
else:
    PASSPORT_SUBKEY = r"SOFTWARE\WOW6432Node\Gilbarco\Passport"
