from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.pos.pos_section import PosSection


class PromptBox(PosSection):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
