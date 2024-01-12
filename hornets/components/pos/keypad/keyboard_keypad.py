from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.pos.keypad.keypad import Keypad
from hornets.components.pos.pos_locators import KeyboardKeypadLocators


class KeyboardKeypad(Keypad):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver,
            keypad=KeyboardKeypadLocators,
            enter_button=KeyboardKeypadLocators.OK
        )
