import logging

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException as SeleniumTimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from hornets.base_enum import BaseEnum
from hornets.utilities.constants import (
    TIME_BETWEEN_KEY,
    MAX_IMPLICIT_TIME_TO_WAIT,
    TIME_BETWEEN_CLICK,
    TIME_BETWEEN_FIELDS
)

log = logging.getLogger()


class SeleniumWrapper:

    def clear_and_set_value(self, driver: WebDriver, locator: str, value: str, force_clear: bool = False):
        """
        Clear and set value to a field
        Args:
            driver (WebDriver): Web driver
            locator (str): Locator to find the element
            value (str): Value to set
            force_clear (bool): Sometimes selenium's clear method does not work properly with MWS inputs. For these
                                scenarios the flag force_clear=True will emulate a keyboard action to clear the input.
        """
        driver.find_element(By.XPATH, locator).clear()
        if force_clear:
            driver.find_element(By.XPATH, locator).send_keys(Keys.CONTROL, "a")
            driver.find_element(By.XPATH, locator).send_keys(Keys.DELETE)
        return self.set_value(
            driver=driver,
            locator=locator,
            value=value
        )

    def set_value(self, driver: WebDriver, locator: str, value: str):
        """
        Set value to a field
        Args:
            driver (WebDriver): Web driver
            locator (str): Locator to find the element
            value (str): Value to set
        """
        self.click_button(driver, locator)
        for single_key in value:
            ActionChains(driver).send_keys(single_key).pause(TIME_BETWEEN_KEY).perform()

    def click_button(self, driver: WebDriver, value_to_click: str):
        """
        Click on a button
        Args:
            driver (WebDriver): Web driver
            value_to_click (str): Value to click
        Raise:
            SeleniumTimeoutException
        """
        try:
            wait = WebDriverWait(driver, MAX_IMPLICIT_TIME_TO_WAIT)
            wait.until(expected_conditions.element_to_be_clickable((By.XPATH, value_to_click)))
            ActionChains(driver).click(driver.find_element(By.XPATH, value_to_click)).pause(
                TIME_BETWEEN_CLICK).perform()
        except SeleniumTimeoutException:
            raise

    def click_all_buttons_located_by(self, driver: WebDriver, values_to_click: str):
        """
        Click on several buttons
        Args:
            driver (WebDriver): Web driver
            value_to_click (str): Value to click
        """
        wait = WebDriverWait(driver, MAX_IMPLICIT_TIME_TO_WAIT)
        wait.until(expected_conditions.element_to_be_clickable((By.XPATH, values_to_click)))
        buttons = driver.find_elements(By.XPATH, values_to_click)
        try:
            for button in buttons:
                ActionChains(driver).click(button).pause(TIME_BETWEEN_CLICK).perform()
        except SeleniumTimeoutException:
            raise

    def navigate_to(self, web_driver: WebDriver, url: str, wait_for_element: BaseEnum):
        """
        Navigate to a url
        Args:
            web_driver (WebDriver): Web driver
            url (str): Url to navigate to
            wait_for_element (BaseEnum): Element to wait for
        """
        web_driver.get(url)
        wait = WebDriverWait(web_driver, MAX_IMPLICIT_TIME_TO_WAIT)
        wait.until(expected_conditions.visibility_of_element_located((By.XPATH, wait_for_element.value)))

    @staticmethod
    def toggle_is_checked(checkbox: WebElement):
        return "checked" in checkbox.get_attribute("class")

    def toggle_checkbox(self, driver: WebDriver, locator: str, value: bool):
        """
        Toggle checkbox
        Args:
            driver (WebDriver): Web driver
            locator (str): Locator to find the element
            value (bool): Value to set
        """
        checkbox = driver.find_element(By.XPATH, locator)
        if SeleniumWrapper.toggle_is_checked(checkbox) != value:
            checkbox.click()

    def is_element_present(
            self,
            driver: WebDriver,
            locator: str,
            custom_timeout: int = None,
            type=By.XPATH,
            visible_only=True
    ):
        """
        Helper function. Waits for the element to be present on the screen.
        Args:
            driver (WebDriver): Web driver
            locator (str): Element's CSS locator
            custom_timeout (int): How long to wait for element to be available.
            type: the locator type (By.CSS_SELECTOR or By.XPATH)
            visible_only (Bool): Pass to selenium function to grab non displayed items or not
        Returns:
            bool: True if success, False if failure
        Examples:
            >>> _is_element_present(SOME_VALID_LOCATOR)
            True
            >>> _is_element_present(SOME_INVALID_LOCATOR)
            False
        """
        timeout = custom_timeout or MAX_IMPLICIT_TIME_TO_WAIT
        try:
            WebDriverWait(driver, timeout).until(expected_conditions.visibility_of_element_located((type, locator)))
            return True
        except SeleniumTimeoutException:
            return False
        # Sometimes raised if the DOM is modified while we check visibility. Just try again
        except StaleElementReferenceException:
            self.is_element_present(driver, locator, timeout, type, visible_only)
        except Exception:
            return False

    def find_element(
            self,
            driver: WebDriver,
            value_to_find: str,
            additional_attribute: str = None,
            custom_timeout: int = None
    ):
        """
        Find element
        Args:
            driver (WebDriver): Web driver
            value_to_find (str): Value to find
            additional_attribute (str): Additional attribute to add to the locator
            custom_timeout (int): Custom timeout to wait for the element
        Return:
            WebElement: Element found
        """
        try:
            if additional_attribute:
                value_to_find = value_to_find.format(additional_attribute)
            if custom_timeout:
                wait = WebDriverWait(driver, custom_timeout)
            else:
                wait = WebDriverWait(driver, MAX_IMPLICIT_TIME_TO_WAIT)
            wait.until(expected_conditions.visibility_of_element_located((By.XPATH, value_to_find)))
            element_found = driver.find_element(by=By.XPATH, value=value_to_find)
        except Exception:
            element_found = None
        return element_found

    def find_elements(self, driver: WebDriver, value_to_find: str, additional_attribute: str = None):
        """
        Find elements
        Args:
            driver (WebDriver): Web driver
            value_to_find (str): Value to find
            additional_attribute (str): Additional attribute to add to the locator
        Return:
            List[WebElement]: Elements found
        """
        try:
            if additional_attribute:
                value_to_find = value_to_find.format(additional_attribute)
            wait = WebDriverWait(driver, MAX_IMPLICIT_TIME_TO_WAIT)
            wait.until(expected_conditions.visibility_of_element_located((By.XPATH, value_to_find)))
            elements_found = driver.find_elements(by=By.XPATH, value=value_to_find)
        except Exception:
            elements_found = []
        return elements_found

    def is_element_selected(self, driver: WebDriver, locator: str) -> bool:
        return driver.find_element(By.XPATH, locator).is_selected()

    def is_element_displayed(self, driver: WebDriver, locator: str) -> bool:
        return driver.find_element(By.XPATH, locator).is_displayed()

    def is_element_enabled(self, driver: WebDriver, locator: str) -> bool:
        return driver.find_element(By.XPATH, locator).is_enabled()

    def select_dropdown_option(self, driver: WebDriver, option_selected: WebElement):
        """
        Select dropdown option
        Args:
            driver (WebDriver): Web driver
            option_selected (str): Option to be clicked
        """
        ActionChains(driver).move_to_element(option_selected).click().pause(TIME_BETWEEN_CLICK).perform()

    def wait_for_options_to_load(self, driver: WebDriver, field_locator: str):
        """
        Wait for options to load
        Args:
            driver (WebDriver): Web driver
            field_locator (str): Field locator
        """
        ActionChains(driver).move_to_element(driver.find_element(By.XPATH, field_locator)).pause(
            TIME_BETWEEN_FIELDS).perform()
