from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.mws.navigation_urls import POS_PAGE_URL
from hornets.components.mws.mws_locators import PosMwsPageLocators
from hornets.components.mws.pages.mws_page import MwsPage


class PosMwsPage(MwsPage):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=POS_PAGE_URL,
            element_to_wait_for=PosMwsPageLocators.POS_HEADER,
        )
        # If the port used is the 7495, the POS will not detect the locators
        self.driver.get(self.url)
        self.wait_for_page_to_load()
