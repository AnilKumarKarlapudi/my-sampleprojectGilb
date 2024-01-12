from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.exceptions import ElementNotFoundException, ElementNotSavedException
from hornets.components.mws.mws_locators import ForecourtInstallationMwsPageLocators, MainMwsPageLocators
from hornets.components.mws.navigation_urls import FORECOURT_INSTALLATION_PAGE_URL
from hornets.components.mws.pages.forecourt_installation_page.mws_dispenser import MwsDispenser
from hornets.components.mws.pages.forecourt_installation_page.mws_product import MwsProduct
from hornets.components.mws.pages.mws_page import MwsPage
from hornets.utilities.log_config import logger


class ForecourtInstallationMwsPage(MwsPage):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=FORECOURT_INSTALLATION_PAGE_URL,
            element_to_wait_for=ForecourtInstallationMwsPageLocators.HEADER,
        )
        self.mws_dispensers = []
        self.mws_products = []

    def get_all_dispensers(self):
        logger.info("Getting all dispensers")
        self.click(ForecourtInstallationMwsPageLocators.DISPENSERS_SUBSECTION)
        dispensers = self.find_elements(ForecourtInstallationMwsPageLocators.DISPENSERS)
        for dispenser in dispensers:
            dispenser_values = self.get_values_from_row(dispenser)
            self.mws_dispensers.append(
                MwsDispenser(
                    driver=self.driver,
                    dispenser_number=dispenser_values[0],
                    pump_protocol=dispenser_values[1],
                    payment_terminal_type=dispenser_values[2],
                    dispenser_type=dispenser_values[3],
                    connection=dispenser_values[4]
                )
            )

    def get_all_products(self):
        logger.info("Getting all products")
        self.click(ForecourtInstallationMwsPageLocators.PRODUCTS_SUBSECTION)
        products = self.find_elements(ForecourtInstallationMwsPageLocators.PRODUCTS)
        for product in products:
            product_values = self.get_values_from_row(product)
            self.mws_products.append(
                MwsProduct(
                    driver=self.driver,
                    product_number=product_values[0],
                    product_name=product_values[1],
                )
            )

    def edit_dispenser(self, mws_dispenser_number: str, dispenser_changes: dict):
        logger.info(f"Editing dispenser #{mws_dispenser_number}")
        dispenser_selected = self.get_dispenser(mws_dispenser_number)
        self.click(ForecourtInstallationMwsPageLocators.EDIT_DISPENSER, mws_dispenser_number)
        dispenser_selected.edit_dispenser(dispenser_changes)

    def edit_product(self, mws_product_number: str, new_mws_product_name: str):
        logger.info(f"Editing product #{mws_product_number}")
        product_selected = self.get_product(mws_product_number)
        self.click(ForecourtInstallationMwsPageLocators.EDIT_PRODUCT, mws_product_number)
        product_selected.edit_product(new_mws_product_name)

    def get_dispenser(self, mws_dispenser_number: str) -> MwsDispenser:
        logger.info(f"Getting dispenser #{mws_dispenser_number}")
        try:
            self.get_all_dispensers()
            return next(
                mws_dispenser for mws_dispenser in self.mws_dispensers
                if mws_dispenser.dispenser_number == mws_dispenser_number
            )
        except StopIteration:
            raise ElementNotFoundException(f"Dispenser #{mws_dispenser_number} not found")

    def get_product(self, mws_product_name: str):
        logger.info(f"Getting product {mws_product_name}")
        try:
            self.get_all_products()
            return next(
                mws_product for mws_product in self.mws_products
                if mws_product.product_name == mws_product_name
            )
        except StopIteration:
            raise ElementNotFoundException(f"Product {mws_product_name} not found")

    def add_product(self, product_name):
        logger.info(f"Adding product {product_name}")
        self.click(ForecourtInstallationMwsPageLocators.PRODUCTS_SUBSECTION)
        self.click(ForecourtInstallationMwsPageLocators.ADD_PRODUCT)
        self.set_value(ForecourtInstallationMwsPageLocators.PRODUCT_NAME, product_name)
        self.click(ForecourtInstallationMwsPageLocators.PRODUCT_SAVE_BUTTON)
        self.click(MainMwsPageLocators.SAVE_BUTTON)
        if not self.information_has_been_saved(additional_message="Forecourt Installation"):
            raise ElementNotSavedException(f"Product {product_name} not created")
        logger.info(f"Product {product_name} was created")
        mws_product_created = MwsProduct(driver=self.driver, product_number=product_name, product_name=product_name)
        self.mws_products.append(mws_product_created)
        return mws_product_created

    def delete_product(self, mws_product_name: str):
        logger.info(f"Deleting product {mws_product_name}")
        self.click(ForecourtInstallationMwsPageLocators.PRODUCTS_SUBSECTION)
        self.click(ForecourtInstallationMwsPageLocators.DELETE_PRODUCT)
        self.click(MainMwsPageLocators.YES)
        self.click(MainMwsPageLocators.SAVE_BUTTON)
        self.mws_products.remove(self.get_product(mws_product_name))
        logger.info(f"Product {mws_product_name} was deleted")
