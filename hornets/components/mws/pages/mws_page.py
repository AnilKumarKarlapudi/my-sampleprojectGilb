from selenium.common import TimeoutException as SeleniumTimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions

from hornets.base import Base
from hornets.base_enum import BaseEnum
from hornets.utilities.log_config import logger
from hornets.components.mws.mws_locators import MainMwsPageLocators


class MwsPage(Base):

    def __init__(self, driver: WebDriver, url: str, element_to_wait_for: BaseEnum):
        super().__init__(driver)
        self.url = url
        self.element_to_wait_for = element_to_wait_for

    @staticmethod
    def get_values_from_row(row: WebElement):
        return row.text.split('\n')

    def wait_for_page_to_load(self) -> bool:
        """
        Wait for the page to load
        Raise:
            SeleniumTimeoutException: If the page is not found
        """
        try:
            self.wait.until(expected_conditions.presence_of_element_located(
                (By.XPATH, self.get_locator(self.element_to_wait_for))))
        except SeleniumTimeoutException:
            logger.error(f"Page {self.url} not found")
            return False
        return True

    def wait_for_element_to_load(self, element_to_wait_for: BaseEnum):
        """
        Wait for the element to load
        Args:
            element_to_wait_for(BaseEnum): Element to wait for
        Raise:
            SeleniumTimeoutException: If the element is not found
        """
        try:
            element_to_wait_for = self.get_locator(element_to_wait_for)
            self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, element_to_wait_for)))
        except SeleniumTimeoutException:
            logger.error(f"Element {element_to_wait_for} not found on page {self.url}")

    def wait_for_element_to_visible(self, element_to_wait_for: BaseEnum):
        """
        Wait for the element to be visible
        Args:
            element_to_wait_for(BaseEnum): Element to wait for
        Raise:
            SeleniumTimeoutException: If the element is not found
        """
        try:
            element_to_wait_for = self.get_locator(element_to_wait_for)
            self.wait.until(expected_conditions.visibility_of_element_located((By.XPATH, element_to_wait_for)))
        except SeleniumTimeoutException:
            logger.error(f"Element {element_to_wait_for} not found on page {self.url}")

    def get_current_url(self) -> str:
        """
        Get the current url
        Return:
            str: Current url
        """
        return self.driver.current_url

    def read_dialogue_box(self):
        """
        Read dialogue box's text.
        Returns:
            (str) The text in the dialogue box if it exists; None if no dialogue box exists.
        Examples:
            >>> read_dialogue_box()
            'We are unable to complete your request. Please try again. If the error continues, contact the helpdesk.'
            >>> read_dialogue_box()
            ""
        """
        if self.is_element_present(MainMwsPageLocators.DIALOGUE_BOX):
            return self.get_text(MainMwsPageLocators.DIALOGUE_BOX)
        else:
            logger.error("Dialogue box not appeared")

    def is_save_enabled(self) -> bool:
        """
        Check if button Save is enabled.
        Returns:
            _ (bool): True if button is enabled, False if button is disabled
        """
        save_button = self.find_element(value_locator=MainMwsPageLocators.SAVE_BUTTON)
        return save_button.get_attribute("disabled") != 'true'
