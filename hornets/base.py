import logging
from abc import ABC
from dataclasses import dataclass
from typing import Union

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common import TimeoutException as SeleniumTimeoutException
from selenium.common.exceptions import StaleElementReferenceException

from hornets.base_enum import BaseEnum
from hornets.components.exceptions import ElementNotFoundException
from hornets.components.mws.mws_locators import MainMwsPageLocators
from hornets.utilities.log_config import logger
from hornets.utilities.constants import MAX_EXPLICIT_TIME_TO_WAIT
from hornets.utilities.selenium_wrapper import SeleniumWrapper


@dataclass
class DropdownOption:
    locator_value: str
    locator_dropdown_values: BaseEnum = MainMwsPageLocators.DROPDOWN_VALUE


class Base(ABC):

    def __init__(self, driver: WebDriver):
        self.selenium_wrapper = SeleniumWrapper()
        self.driver = driver
        self.log = logging.getLogger()
        self.wait = WebDriverWait(self.driver, timeout=MAX_EXPLICIT_TIME_TO_WAIT)

    def get_locator(self, locator_name: BaseEnum):
        """
        Get locator from locator enum
        Arg:
            locator_name (BaseEnum): Locator name
        Return:
            str: Locator value
        """
        return locator_name.value

    def set_value(self, locator_enum: BaseEnum, value: str):
        """
        Set value to a field
        Args:
            locator_enum (BaseEnum): Locator name
            value (str): Value to set
        """
        locator = self.get_locator(locator_enum)
        return self.selenium_wrapper.set_value(
            driver=self.driver,
            locator=locator,
            value=value
        )

    def clear_and_set_value(self, locator_enum: BaseEnum, value: str, force_clear: bool = False):
        """
        Clear and set value to a field
        Args:
            locator_enum (BaseEnum): Locator name
            value (str): Value to set
        """
        locator = self.get_locator(locator_enum)
        return self.selenium_wrapper.clear_and_set_value(
            driver=self.driver,
            locator=locator,
            value=value,
            force_clear=force_clear
        )

    def click(self, locator_enum: BaseEnum, additional_attribute: Union[str, BaseEnum] = None):
        """
        Click on a button
        Args:
            locator_enum (BaseEnum): Locator name
            additional_attribute (str, BaseEnum): Additional attribute to add to the locator
        Raise:
            SeleniumTimeoutException: If element not found
        """
        try:
            value_to_click = self.get_locator(locator_enum)
            if additional_attribute:
                value_to_click = value_to_click.format(additional_attribute)
            return self.selenium_wrapper.click_button(
                driver=self.driver,
                value_to_click=value_to_click
            )
        except SeleniumTimeoutException:
            logger.error(f"Element {locator_enum.name} not found")
            raise ElementNotFoundException(f"Element {locator_enum.name} not found")

    def find_element(self, value_locator: BaseEnum, additional_attribute: str = None, custom_timeout: int = None):
        """
        Find element
        Args:
            value_locator (BaseEnum): Locator name
            additional_attribute (str): Additional attribute to add to the locator
            custom_timeout (int): Custom timeout to wait for the element
        Return:
            WebElement: Element found
        """
        try:
            value_to_find = self.get_locator(value_locator)
            return self.selenium_wrapper.find_element(
                driver=self.driver,
                value_to_find=value_to_find,
                additional_attribute=additional_attribute,
                custom_timeout=custom_timeout
            )
        except Exception:
            element_found = None
        return element_found

    def find_elements(self, value_locator: BaseEnum, additional_attribute: str = None):
        """
        Find elements
        Args:
            value_locator (BaseEnum): Locator name
            additional_attribute (str): Additional attribute to add to the locator
        Return:
            List[WebElement]: Elements found
        """
        try:
            value_to_find = self.get_locator(value_locator)
            return self.selenium_wrapper.find_elements(
                driver=self.driver,
                value_to_find=value_to_find,
                additional_attribute=additional_attribute
            )
        except Exception:
            element_found = None
        return element_found

    def toggle_switch(self, locator_enum: BaseEnum, value: bool):
        """
        Toggle checkbox
        Args:
            locator_enum (BaseEnum): Locator name
            value (bool): Value to set
        """
        locator = self.get_locator(locator_enum)
        return self.selenium_wrapper.toggle_checkbox(
            driver=self.driver,
            locator=locator,
            value=value
        )

    def is_element_present(self, locator_enum: BaseEnum, additional_attribute: str = None, custom_timeout: int = None):
        """
        Helper function. Checks if the element is present on the screen.
        Args:
            locator_enum (BaseEnum): Locator name
            additional_attribute (str): Additional attribute to add to the locator
            custom_timeout (int): Custom timeout to wait for the element
        Returns:
            bool: True if success, False if failure
        Examples:
            >>> is_element_present(MainMwsPageLocators.DIALOGUE_BOX)
            True
            >>> is_element_present(SOME_INVALID_LOCATOR)
            False
        """
        try:
            element = self.get_locator(locator_enum)
            if additional_attribute:
                element = element.format(additional_attribute)
            return self.selenium_wrapper.is_element_present(
                driver=self.driver,
                locator=element,
                custom_timeout=custom_timeout
            )
        except SeleniumTimeoutException:
            logger.error(f"Element {locator_enum.name} not found")
            raise

    def get_text(self, locator_enum: BaseEnum, additional_attribute: str = None, custom_timeout: int = None):
        """
        Helper function. Returns the element's text.
        Args:
            locator_enum: (BaseEnum) Element's locator.
            additional_attribute (str): Additional attribute to add to the locator
            custom_timeout (int): Custom timeout to wait for the element
        Returns:
            Returns string/list with text of the element upon success, or blank string otherwise.
        Examples:
            >>> get_text(MainMwsPageLocators.DIALOGUE_BOX)
            'Do you want to delete'
        """
        logger.debug(f"Fetching value of {locator_enum}.")
        element = self.find_element(locator_enum, additional_attribute, custom_timeout)

        if element:
            try:
                classname = element.get_attribute('class')
                if ('textbox' in classname) or ('inputtext' in classname):
                    value = element.get_attribute('value')
                    if not value:
                        value = element.text
                elif 'textarea' in classname:
                    texts = element.get_attribute('value')
                    value = texts.split('\n')
                elif 'listbox' in classname:
                    texts = element.text
                    value = texts.split('/n')
                else:
                    value = element.text
            except StaleElementReferenceException as e:  # Element changed after we found it.
                #  Try again
                logger.info(e)
                return self.get_text(locator_enum, additional_attribute, custom_timeout)
            except Exception as e:
                logger.warning(f"Unable to read text: {e}")
                value = ""
        else:
            value = ""
        return value

    def select_dropdown_option(self, locator_enum: BaseEnum, dropdown_option: DropdownOption):
        """
        Select option from a dropdown
        Args:
            locator_enum (BaseEnum): Dropdown locator name
            dropdown_option (DropdownOption): Dropdown value to select
        """
        self.click(locator_enum)
        option_selected = self.find_element(dropdown_option.locator_dropdown_values, dropdown_option.locator_value)
        return self.selenium_wrapper.select_dropdown_option(
            driver=self.driver,
            option_selected=option_selected
        )

    def information_has_been_saved(self, additional_message: str):
        return bool(self.find_element(MainMwsPageLocators.SUCCESS_BANNER, additional_attribute=additional_message))

    def expand_all_page_sections(self, plus_buttons: BaseEnum = MainMwsPageLocators.SECTION_EXPAND_PLUS_BUTTONS):
        """
        Expand all the different sections within a page.
        Example:
        >>> items_add_page.expand_all_page_sections()
        Will expand Scan Codes/Linked Items/Options/Qualifiers/Tender Restrictions sections to
        show all the fields previously hidden when the user just enters the Items Add page.
        """
        plus_buttons = self.get_locator(plus_buttons)
        return self.selenium_wrapper.click_all_buttons_located_by(
            driver=self.driver,
            values_to_click=plus_buttons
        )


class BaseOptions(Base):

    def __init__(self, driver: WebDriver, fields):
        super().__init__(driver)
        self.driver = driver
        self.fields = dict.fromkeys(fields)

    def get_field_value(self, field_name):
        """
        Get value from a field
        Args:
            field_name (BaseEnum): Value to get
        Return:
            str: Value from the field
        Example:
            >>> self.get_field_value(DiscountsMwsPageLocators.DISCOUNT_NAME)
            'Test'
        """
        logger.info(f"Getting value from field {field_name}")
        return self.find_element(field_name).get_attribute("value")

    def get_all_field_values(self):
        """
        Get all field values from the fields
        Return:
            dict: All field values from the fields
        Example:
            >>> self.get_all_field_values()
            {
                DiscountsMwsPageLocators.DISCOUNT_NAME: 'Test',
                DiscountsMwsPageLocators.DISCOUNT_METHOD: 'Amount',
                DiscountsMwsPageLocators.DISCOUNT_REASON: 'Test',
            }
        """
        logger.info("Getting all field values")
        for field in self.fields:
            self.fields[field] = self.get_field_value(field)
        return self.fields

    def set_field_value(self, field_name, new_value):
        """
        Set value to a field
        Args:
            field_name (BaseEnum): Field name
            new_value: New value to set
        Example:
            >>> self.set_field_value(DiscountsMwsPageLocators.DISCOUNT_NAME, 'Test')
        """
        logger.info(f"Setting value {new_value} to field {field_name.name}")
        self.wait_for_options_to_load(field_name)
        if isinstance(new_value, str):
            self.clear_and_set_value(field_name, new_value)
        elif isinstance(new_value, bool):
            self.toggle_switch(field_name, new_value)
        elif isinstance(new_value, DropdownOption):
            self.select_dropdown_option(field_name, new_value)
        else:
            raise TypeError(f"Type {type(new_value)} not supported")
        self.fields[field_name] = new_value

    def set_fields_value(self, fields_value):
        """
        Set value to fields
        Args:
            fields_value (dict): Values to set
        Example:
            >>> self.set_fields_value({
            >>>     DiscountsMwsPageLocators.DISCOUNT_NAME: 'Test',
            >>>     DiscountsMwsPageLocators.DISCOUNT_METHOD: 'Amount',
            >>>     DiscountsMwsPageLocators.DISCOUNT_REASON: 'Test',
            >>> })
        """
        logger.info(f"Setting values {fields_value} to fields")
        for field_name, new_value in fields_value.items():
            self.set_field_value(field_name, new_value)

    def is_element_selected(self, locator_enum: BaseEnum):
        """
        Check if a field is selected
        Args:
            locator_enum (BaseEnum): Locator name
        Return:
            bool: True if selected, False otherwise
        Example:
            >>> self.is_selected(DiscountsMwsPageLocators.DISCOUNT_METHOD)
            True
        """
        logger.info(f"Checking if field {locator_enum} is selected")
        element_to_verify = self.get_locator(locator_enum)
        return self.selenium_wrapper.is_element_selected(
            driver=self.driver,
            locator=element_to_verify
        )

    def is_element_displayed(self, locator_enum: BaseEnum):
        """
        Check if an element is displayed
        Args:
            locator_enum (BaseEnum): Locator name
        Return:
            bool: True if displayed, False otherwise
        Example:
            >>> self.is_element_displayed(DiscountsMwsPageLocators.DISCOUNT_NAME)
            True
        """
        logger.info(f"Checking if element {locator_enum} is displayed")
        element_to_verify = self.get_locator(locator_enum)
        return self.selenium_wrapper.is_element_displayed(
            driver=self.driver,
            locator=element_to_verify
        )

    def is_element_enabled(self, locator_enum: BaseEnum):
        """
        Check if an element is enabled
        Args:
            locator_enum (BaseEnum): Locator name
        Return:
            bool: True if displayed, False otherwise
        Example:
            >>> self.is_element_displayed(DiscountsMwsPageLocators.DISCOUNT_NAME)
            True
        """
        logger.info(f"Checking if element {locator_enum} is displayed")
        element_to_verify = self.get_locator(locator_enum)
        return self.selenium_wrapper.is_element_enabled(
            driver=self.driver,
            locator=element_to_verify
        )

    def wait_for_options_to_load(self, field_name: BaseEnum):
        """
        Wait for options to load
        Args:
            field_name (BaseEnum): Field name
        """
        field_locator = self.get_locator(field_name)
        return self.selenium_wrapper.wait_for_options_to_load(
            driver=self.driver,
            field_locator=field_locator
        )
