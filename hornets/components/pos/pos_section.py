from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.base import Base


class PosSection(Base):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
