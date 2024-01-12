from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.pos.pos_locators import FunctionKeysLocators
from hornets.components.pos.pos_section import PosSection


class FunctionKeys(PosSection):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def pay_with_cash(self):
        """
        Pay with cash
        """
        self.click(FunctionKeysLocators.PAY)
        self.click(FunctionKeysLocators.EXACT_AMOUNT)

    def pay_with_credit_card(self):
        """
        Pay with credit card
        """
        self.click(FunctionKeysLocators.PAY)
        self.click(FunctionKeysLocators.CREDIT_CARD)
