from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.base import Base
from hornets.components.exceptions import ElementNotSavedException
from hornets.components.mws.mws_locators import ForecourtInstallationMwsPageLocators, MainMwsPageLocators
from hornets.utilities.log_config import logger


class MwsProduct(Base):

    def __init__(
            self,
            driver: WebDriver,
            product_number,
            product_name
    ):
        super().__init__(driver)
        self.product_number = product_number
        self.product_name = product_name

    def edit_product(self, new_product_name: str):
        self.clear_and_set_value(ForecourtInstallationMwsPageLocators.PRODUCT_NAME, new_product_name)
        self.click(ForecourtInstallationMwsPageLocators.PRODUCT_SAVE_BUTTON)
        self.click(MainMwsPageLocators.SAVE_BUTTON)
        if not self.information_has_been_saved(additional_message="Forecourt Installation"):
            raise ElementNotSavedException(f"Product #{self.product_number} not edited")
        logger.info(f"Product #{self.product_number} edited successfully")
