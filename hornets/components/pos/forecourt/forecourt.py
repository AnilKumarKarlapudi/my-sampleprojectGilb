from selenium.webdriver.chrome.webdriver import WebDriver
from typing import List

from hornets.components.pos.pos_locators import ForecourtLocators
from hornets.components.pos.forecourt.dispenser_display import DispenserDisplay
from hornets.components.pos.pos_section import PosSection
from hornets.models.dispenser import Dispenser


class Forecourt(PosSection):

    def __init__(self, driver: WebDriver, dispensers: List[DispenserDisplay] = None):
        super().__init__(driver)
        self.dispensers = dispensers or self.get_dispensers_list()

    def get_dispensers_list(self):
        """
        Get the list of dispensers
        Return:
            List[DispenserDisplay]: List of dispensers
        """
        dispensers = self.find_elements(ForecourtLocators.FORECOURT_DISPLAY)
        return [DispenserDisplay(self.driver, Dispenser(dispenser_id=dispenser.text)) for dispenser in dispensers]

    def select_dispenser(self, dispenser_id):
        """
        Select a dispenser
        Args:
            dispenser_id: Dispenser ID
        """
        self.click(ForecourtLocators.DISPENSER, additional_attribute=dispenser_id)

    def get_first_available_dispenser_id(self):
        # TODO: Implement this method
        pass

    def stop_all_dispensers(self):
        """
        Stop all dispensers
        """
        self.click(ForecourtLocators.ALL_STOP)
        self.click(ForecourtLocators.YES)

    def start_all_dispensers(self):
        """
        Start all dispensers
        """
        self.click(ForecourtLocators.CLEAR_ALL_STOP)
        self.click(ForecourtLocators.YES)
        self.click(ForecourtLocators.YES)
