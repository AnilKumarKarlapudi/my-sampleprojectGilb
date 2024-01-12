import pytest
from pytest_bdd import given
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service as ChromeService

from hornets.components.mws.enums import FormalNameMwsPageEnum
from hornets.utilities.log_config import logger

from hornets.components.mws.pages.login_page import LoginMwsPage
from hornets.components.mws.pages.main_page import MainMwsPage
from hornets.utilities.constants import CHROME_WEBDRIVER_EXECUTABLE, CHROME_SELECTORS_HUB_EXTENSION, \
    MAX_IMPLICIT_TIME_TO_WAIT


# Fixture to share needed context between different tests steps
@pytest.fixture(scope='module')
def context():
    return {}


@pytest.fixture(scope="module")
def driver() -> WebDriver:
    logger.info("Initializing Chrome driver. Scope: Module")
    service = ChromeService(executable_path=CHROME_WEBDRIVER_EXECUTABLE)
    options = webdriver.ChromeOptions()
    options.add_extension(CHROME_SELECTORS_HUB_EXTENSION)
    driver = webdriver.Chrome(options=options, service=service)
    driver.implicitly_wait(time_to_wait=MAX_IMPLICIT_TIME_TO_WAIT)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def login_page(driver) -> LoginMwsPage:
    logger.info("Signing on MWS. Scope: Module")
    login_page = LoginMwsPage(driver)
    driver.get(login_page.url)
    login_page.wait_for_page_to_load()
    yield login_page


@pytest.fixture(scope="module")
def mws(login_page) -> MainMwsPage:
    mws_main_page = login_page.login_with_valid_credentials()
    mws_main_page.wait_for_page_to_load()
    logger.info("Entering credentials... Scope: Module")
    yield mws_main_page


@pytest.fixture(scope="module")
def discounts_page(mws, context) -> MainMwsPage:
    discounts_page = mws.navigate_through_search_display(FormalNameMwsPageEnum.DISCOUNTS)
    yield discounts_page
    # Delete created discounts by former tests
    if context.get('created_discounts'):
        for discount in context['created_discounts']:
            discounts_page.delete_discount(discount.name)


# --------------------------REUSABLE STEPS---------------------------------------------------

@given('the discount was already created by the initial setup')
def initial_setup():
    pass
