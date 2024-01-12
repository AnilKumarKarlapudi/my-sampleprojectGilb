from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.mws.navigation_urls import STORE_CLOSE_PAGE_URL
from hornets.components.mws.pages.mws_page import MwsPage
from hornets.components.mws.mws_locators import StoreCloseMwsPageLocators


class StoreCloseMwsPage(MwsPage):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=STORE_CLOSE_PAGE_URL,
            element_to_wait_for=StoreCloseMwsPageLocators.HEADER,
        )

    def do_not_close_the_store(self):
        """
        Do not close the Store
        """
        self.click(StoreCloseMwsPageLocators.NO)

    def close_the_store(self):
        """
        Close the Store
        """
        pass
