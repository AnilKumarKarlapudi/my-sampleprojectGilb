from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.pos.pos_locators import SpeedKeysDisplayLocators
from hornets.components.pos.pos_section import PosSection
from hornets.models.display_element import DisplayItem
from hornets.utilities.log_config import logger


class SpeedKeysDisplay(PosSection):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)

    def select_item(self, item: DisplayItem):
        """
        Select an item from the items keypad
        Args:
            item (DisplayItem): Item to select
        """
        logger.info(f"Selecting item {item}")
        self.click(locator_enum=SpeedKeysDisplayLocators.KEY_BY_TEXT, additional_attribute=item.name)
