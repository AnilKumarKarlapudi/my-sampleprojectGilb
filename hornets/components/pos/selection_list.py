from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.pos.pos_locators import SelectionListLocators
from hornets.components.pos.pos_section import PosSection


class SelectionList(PosSection):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def select_discount(self, discount_name: str):
        """
        Select a discount from the selection list
        Args:
            discount_name (str): Discount name to select
        """
        self.click(SelectionListLocators.KEY_BY_TEXT, additional_attribute=discount_name)
