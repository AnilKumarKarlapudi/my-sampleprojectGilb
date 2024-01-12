import logging
import os
import os.path
import re
import shutil
import sys
import zipfile
from pathlib import WindowsPath
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService


import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d %(levelname)5s %(process)d --- [%(threadName)10.10s] %(name)-40.40s : %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger('chrome-driver-installer')

CHROME_DRIVER_DIR = WindowsPath(os.path.abspath(__file__)).parent.parent / "chrome" / "webdriver"

VERSION_RE = re.compile(r"^[0-9.]+$")
CHROME_DIR = WindowsPath("C:\\Program Files\\Google\\Chrome\\Application")
CHROME_X86_DIR = WindowsPath("C:\\Program Files (x86)\\Google\\Chrome\\Application")


def get_chrome_version() -> str:
    if CHROME_DIR.is_dir():
        dirs = [f.name for f in os.scandir(CHROME_DIR) if f.is_dir() and VERSION_RE.match(f.name)]
    elif CHROME_X86_DIR.is_dir():
        dirs = [f.name for f in os.scandir(CHROME_X86_DIR) if f.is_dir() and VERSION_RE.match(f.name)]
    version = max(dirs) if dirs else ''
    log.info(f"Current chrome version: {version}")
    return version


def is_webdriver_version_ok(suitable_version: str) -> bool:
    chrome_driver_fp = CHROME_DRIVER_DIR / "chromedriver.exe"
    ok = chrome_driver_fp.exists() and chrome_driver_fp.is_file()
    if ok:
        log.info(f"Checking if version for {chrome_driver_fp} is suitable with Chrome")

        service = ChromeService(executable_path=str(chrome_driver_fp.absolute()))
        driver = webdriver.Chrome(service=service)
        version = driver.capabilities['chrome']['chromedriverVersion'].split(' ')[0]
        if version != suitable_version:
            log.warning(f"Difference in version, expecting: {suitable_version}, got: {version}")
            ok = False
    return ok


def check_suitable_driver_version_for_chrome_version(chrome_version: str) -> str:
    version_range = chrome_version.split(".")[:-1]
    version_range = ".".join(version_range)

    url = f"https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_{version_range}"
    log.info(f"Checking suitable chromedriver in: {url}")
    response = requests.get(url)
    if response.ok:
        return response.text
    else:
        response.raise_for_status()


def check_suitable_driver_download(suitable_version: str) -> str:
    url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
    log.info(f"Checking for download for suitable version in: {url}")
    response = requests.get(url)
    if response.ok:
        json = response.json()
        for version in json['versions']:
            if version['version'] == suitable_version:
                for download in version['downloads']['chromedriver']:
                    if download['platform'] == sys.platform:
                        return download['url']
    else:
        response.raise_for_status()


def download_chromedriver_zip(download_url: str) -> bool:
    log.info(f"Downloading suitable chromedriver: {download_url}")

    response = requests.get(download_url)
    if response.ok:
        if CHROME_DRIVER_DIR.exists():
            shutil.rmtree(CHROME_DRIVER_DIR)
        
        # Handle ACCESS DENIED error
        # that sometimes occurs right after deleting the dir
        mkdir_attempts = 0
        while mkdir_attempts < 10:
            try:
                CHROME_DRIVER_DIR.mkdir()
                break
            except:
                mkdir_attempts += 1
        else:
            return False

        with open(CHROME_DRIVER_DIR / "chromedriver.zip", "wb") as fp_chromedriver:
            fp_chromedriver.write(response.content)
        return True

    return False


def install_chromedriver():
    chromedriver_zip = CHROME_DRIVER_DIR / "chromedriver.zip"
    if not chromedriver_zip.exists():
        raise FileNotFoundError(chromedriver_zip)

    is_unzipped = False
    with zipfile.ZipFile(chromedriver_zip) as fp_zip:
        for info in fp_zip.infolist():
            if os.path.basename(info.filename) == "chromedriver.exe":
                info.filename = "chromedriver.exe"
                log.info(f"Extracting {info.filename} from {chromedriver_zip}")
                fp_zip.extract(info, CHROME_DRIVER_DIR)
                is_unzipped = True
                break

    if is_unzipped:
        chromedriver_zip.unlink()
    else:
        raise OSError(f"cannot unzip {chromedriver_zip}")


def main():
    log.info("Start checking if chromedriver needs an update...")
    try:
        chrome_version = get_chrome_version()
        suitable_version = check_suitable_driver_version_for_chrome_version(chrome_version)

        if is_webdriver_version_ok(suitable_version):
            log.info("Chromedriver version is suitable with Chrome version, no need to download!")
            sys.exit(0)

        download_url = check_suitable_driver_download(suitable_version)
        if download_chromedriver_zip(download_url):
            install_chromedriver()
            log.info("New chromedriver has been successfully installed!")
            sys.exit(0)

        raise Exception("cannot download chromedriver")
    except Exception:
        log.exception("Something went wrong, cannot continue...")
        sys.exit(2)


if __name__ == '__main__':
    main()
