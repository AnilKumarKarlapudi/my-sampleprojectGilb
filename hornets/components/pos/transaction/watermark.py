from hornets.components.pos.enums import WatermarkDisplayEnum
from hornets.components.pos.pos_locators import WatermarkDispayLocators
from hornets.components.pos.pos_section import PosSection
from hornets.utilities.constants import MAX_TIMEOUT_FOR_TRANSACTION


class Watermark(PosSection):

    def __init__(self, driver):
        super().__init__(driver)
        self.status = None

    def wait_for_transaction_to_be_completed(self):
        """
        Wait for the transaction to be completed
        Raise:
            TimeoutError: If the watermark is not displayed
        Return:
            str: Watermark status
        """
        if self.find_element(value_locator=WatermarkDispayLocators.TRANSACTION_COMPLETED,
                             custom_timeout=MAX_TIMEOUT_FOR_TRANSACTION):
            self.status = WatermarkDisplayEnum.TRANSACTION_COMPLETED
            return self.status
        raise TimeoutError(
            f"Transaction was not completed due that the watermark "
            f"'{WatermarkDisplayEnum.TRANSACTION_COMPLETED}' was not displayed"
        )

    def wait_for_transaction_to_be_voided(self):
        """
        Wait for the transaction to be voided
        Raise:
            TimeoutError: If the watermark is not displayed
        Return:
            str: Watermark status
        """
        if self.find_element(WatermarkDispayLocators.TRANSACTION_VOIDED):
            self.status = WatermarkDisplayEnum.TRANSACTION_VOIDED
            return self.status
        raise TimeoutError(
            f"Transaction was not completed due that the watermark "
            f"'{WatermarkDisplayEnum.TRANSACTION_VOIDED}' was not displayed"
        )
