from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.mws.mws_locators import TendersMwsPageLocators
from hornets.components.mws.navigation_urls import TENDERS_PAGE_URL
from hornets.components.mws.pages.mws_page import MwsPage


class TendersMwsPage(MwsPage):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=TENDERS_PAGE_URL,
            element_to_wait_for=TendersMwsPageLocators.HEADER,
        )
