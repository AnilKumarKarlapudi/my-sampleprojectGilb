import time
from typing import Union

from selenium.common import ElementClickInterceptedException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from hornets.components.mws.mws_locators import DiscountsMwsPageLocators
from hornets.components.mws.navigation_urls import DISCOUNTS_PAGE_URL
from hornets.components.mws.pages.mws_page import MwsPage
from hornets.models.manual_discount.models import ManualDiscount
from hornets.utilities.log_config import logger


class DiscountsMwsPage(MwsPage):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=DISCOUNTS_PAGE_URL,
            element_to_wait_for=DiscountsMwsPageLocators.SEARCH_DISCOUNTS,
        )

    def search_discount(self, discount_name: str, delay: int = None) -> Union[WebElement, None]:
        """
        Search for a discount by name
        Args:
            discount_name(str): Name of the discount to search
            delay(int): Time to wait before searching
        Return:
            WebElement: First row of the search results
        """
        if delay:
            logger.info("Waiting for search...")
            time.sleep(delay)
        self.driver.refresh()
        logger.info(f"Searching '{discount_name}' discount...")
        search_input = self.find_element(DiscountsMwsPageLocators.SEARCH_DISCOUNTS)
        search_input.clear()
        self.set_value(DiscountsMwsPageLocators.SEARCH_DISCOUNTS, value=discount_name)
        from selenium.common import TimeoutException

        try:
            # Interpolate the generic locator with the discount name to search
            first_row_results_element = self.find_element(
                DiscountsMwsPageLocators.DISCOUNT_NAME_SEARCH_RESULT, additional_attribute=discount_name
            )
        # TODO: Do not return None, raise an exception instead or return a NoDiscountFound
        except TimeoutException:
            logger.info(f"Discount {discount_name} was not found.")
            return None
        logger.info(f"Discount {discount_name} found!")
        return first_row_results_element

    def open_new_discount_section(self):
        """
        Open the new discount section
        """
        logger.info("Opening new discount section")
        add_btn = self.find_element(DiscountsMwsPageLocators.ADD)
        add_btn.click()

    def create_discount(self, discount: ManualDiscount):
        """
        Create a discount with the given configuration
        Args:
            discount(ManualDiscount): Discount to create
        Return:
            Discount: Discount created
        """
        logger.info("Creating discount with the following configuration:")
        logger.info(discount)

        # Set Discount Name
        discount_name = self.find_element(DiscountsMwsPageLocators.DISCOUNT_NAME)
        discount_name.click()
        self.set_value(locator_enum=DiscountsMwsPageLocators.DISCOUNT_NAME, value=str(discount.name))

        if discount.amount == "variable":
            self.click(DiscountsMwsPageLocators.DISCOUNT_AMOUNT)

        if discount.apply_discount_to == "transaction":
            self.click(DiscountsMwsPageLocators.APPLY_DISCOUNT_TO)

        if discount.discount_type == "amount_off":
            self.click(DiscountsMwsPageLocators.DISCOUNT_TYPE)

        # Set Discount Amount
        amount = self.find_element(DiscountsMwsPageLocators.AMOUNT)
        amount.click()
        self.set_value(locator_enum=DiscountsMwsPageLocators.AMOUNT, value=str(discount.amount))

        try:
            save = self.find_element(DiscountsMwsPageLocators.SAVE)
            save.click()
        except ElementClickInterceptedException:
            self.log.info("There was a problem. Discount cannot be saved.")
            return None

        self.driver.refresh()

        return discount

    def delete_discount(self, discount_name: str):
        """
        Delete a discount by name
        Args:
            discount_name(str): Name of the discount to delete
        """
        try:
            self.search_discount(discount_name)
            delete_btn = self.find_element(DiscountsMwsPageLocators.DELETE, additional_attribute=discount_name)
            delete_btn.click()
            yes_popup_btn = self.find_element(DiscountsMwsPageLocators.POPUP_YES_DELETE)
            yes_popup_btn.click()
        except Exception:
            self.log.info(f"Discount {discount_name} could not be deleted.")
