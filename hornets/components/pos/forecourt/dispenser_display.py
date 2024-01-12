from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.pos.enums import DispenserStatusEnum
from hornets.components.pos.pos_locators import DispenserLocators
from hornets.components.pos.pos_section import PosSection
from hornets.models.dispenser import Dispenser
from hornets.utilities.log_config import logger


class DispenserDisplay(PosSection, Dispenser):

    def __init__(self, driver: WebDriver, dispenser: Dispenser):
        PosSection.__init__(self, driver)
        self.dispenser = Dispenser(dispenser_id=dispenser.dispenser_id)

    def get_dispenser_status(self) -> DispenserStatusEnum:
        """
        Get the dispenser status
        Raise:
            AttributeError: If the dispenser status is not found
        Return:
            DispenserStatusEnum: Dispenser status
        """
        try:
            self.dispenser.dispenser_status = self.find_element(DispenserLocators.DISPENSER_STATUS).text
            logger.info(f"Dispenser status for Dispenser#{self.get_dispenser_id()}: {self.dispenser.dispenser_status}")
            return DispenserStatusEnum.from_string(self.dispenser.dispenser_status)
        except AttributeError:
            logger.info(f"Dispenser status for Dispenser #{self.get_dispenser_id()}: {DispenserStatusEnum.IDLE}")
            return DispenserStatusEnum.IDLE
        finally:
            self.click(DispenserLocators.BACK)

    def get_dispenser_id(self):
        return self.dispenser.dispenser_id
