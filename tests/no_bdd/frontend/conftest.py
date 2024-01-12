import pytest

from hornets.components.mws.pages.login_page import LoginMwsPage
from hornets.components.mws.pages.main_page import MainMwsPage
from hornets.components.mws.pages.mws_page import MwsPage
from hornets.utilities.log_config import logger


@pytest.fixture(scope="class")
def login_page(driver) -> LoginMwsPage:
    logger.info("Signing on MWS")
    logger.info("Entering credentials")
    login_page = LoginMwsPage(driver)
    driver.maximize_window()
    driver.get(login_page.url)
    login_page.wait_for_page_to_load()
    yield login_page


@pytest.fixture(scope="class")
def mws(login_page) -> MainMwsPage:
    mws_main_page = login_page.login_with_valid_credentials()
    mws_main_page.wait_for_page_to_load()
    yield mws_main_page


@pytest.fixture(scope="class")
def mws_go_to(mws):
    def _mws_go_to(url_to_go: str) -> MwsPage:
        return mws.navigate_through_url(url_to_go)
    yield _mws_go_to
