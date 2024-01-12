from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.pos.header.status_information import StatusInformation
from hornets.components.pos.pos_locators import HeaderLocators
from hornets.components.pos.pos_section import PosSection


class Header(PosSection):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def reload(self):
        """
        Reload the POS
        """
        self.click(HeaderLocators.RELOAD)

    def get_status_information(self):
        """
        Get the status information
        Return:
            StatusInformation: Status information page
        """
        self.click(HeaderLocators.INFORMATION_BUTTON)
        return StatusInformation(self.driver)
