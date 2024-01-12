from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.mws.mws_locators import LoyaltyMwsPageLocators
from hornets.components.mws.navigation_urls import LOYALTY_PAGE_URL
from hornets.components.mws.pages.mws_page import MwsPage


class LoyaltyMwsPage(MwsPage):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=LOYALTY_PAGE_URL,
            element_to_wait_for=LoyaltyMwsPageLocators.HEADER,
        )
