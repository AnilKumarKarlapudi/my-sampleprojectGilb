from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.pos.pos_locators import StatusInformationLocators
from hornets.components.pos.pos_section import PosSection


class StatusInformation(PosSection):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def return_to_pos(self):
        """
        Return to POS
        """
        self.click(StatusInformationLocators.BACK)
