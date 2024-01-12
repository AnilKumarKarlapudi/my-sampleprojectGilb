from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.mws.mws_locators import RegistersMwsPageLocators, MainMwsPageLocators
from hornets.components.mws.navigation_urls import REGISTERS_PAGE_URL
from hornets.components.mws.pages.registers_page.registers import MwsRegisters, RegisterOptions
from hornets.components.mws.pages.mws_page import MwsPage
from hornets.components.exceptions import ElementNotFoundException
from hornets.utilities.log_config import logger


class RegistersMwsPage(MwsPage):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=REGISTERS_PAGE_URL,
            element_to_wait_for=RegistersMwsPageLocators.HEADER
        )
        self.registers = []

    def get_all_registers(self):
        """
        Description: fetch all registers from screen
        Returns: Object
        Example:
            >>> get_all_registers()
        """
        registers = self.find_elements(RegistersMwsPageLocators.REGISTERS)
        for register in registers:
            register_values = self.get_values_from_row(register)
            self.registers.append(
                MwsRegisters(
                    driver=self.driver,
                    register_number=register_values[0],
                    machine_name=register_values[1],
                    personality=register_values[2]
                )
            )

    def add_register(self, register_config: dict):
        """
        Description: Add a new register.
        Args:
            register_config(dict): A dictionary of controls and values to add register.
        Example:
            register_config = {
                RegistersMwsPageLocators.REGISTER_NUMBER: "1",
                RegistersMwsPageLocators.PINPAD_TYPE: RegisterPinpadTypeOptions.VERIFONE_MX915,
                RegistersMwsPageLocators.IP_ADDRESS: "10.5.48.2",
                RegistersMwsPageLocators.MACHINE_NAME: RegisterMachineTypeOptions.POSSERVER,
                RegistersMwsPageLocators.REGISTER_GROUP: RegisterGroupOptions.POSGROUP1,
                RegistersMwsPageLocators.LINE_DISPLAY: RegisterLineDisplayOptions.POS_LINE_DISPLAY
            }
            >>> add_register(register_config)
        """

        add_register = RegisterOptions(self.driver)
        self.click(RegistersMwsPageLocators.ADD)
        add_register.set_fields_value(register_config)
        self.click(MainMwsPageLocators.SAVE_BUTTON)
        self.verify_success_banner()

    def edit_register(self, register_number: str, register_changes: dict):
        """
        Description: Change the configuration for an existing register.
        Args:
            register_number: (str) The number of the register to change.
            register_changes: (dict) A dictionary of controls and values.
        """
        register_edit = self.get_register(register_number)
        self.click(RegistersMwsPageLocators.EDIT, register_number)
        register_edit.edit_register(register_changes)
        self.verify_success_banner()

    def delete_register(self, register_number: str):
        """
        Description: Delete an existing register.
        Args:
            register_number: (str) The number of the register to delete.
        """
        self.click(RegistersMwsPageLocators.DELETE, register_number)
        if "you want to delete" in self.read_dialogue_box():
            self.click(MainMwsPageLocators.YES)
        self.verify_success_banner()

    def get_register(self, register_number: str):
        try:
            self.get_all_registers()
            return next(
                register for register in self.registers
                if register.register_number == register_number
            )
        except StopIteration:
            raise ElementNotFoundException(f"Register #{register_number} not found")

    def verify_success_banner(self):
        """
        This will verify if success banner appear after add/edit/delete register
        """
        if self.find_element(MainMwsPageLocators.SUCCESS_BANNER, "Registers"):
            logger.info("Success banner appeared")
            self.click(MainMwsPageLocators.BANNER_CLOSE)
        else:
            logger.error("Success banner not appeared")

    def verify_register_exist(self, register_number: str):
        """
        verify if register exists on screen
        """
        self.get_all_registers()
        for register in self.registers:
            if register.register_number == register_number:
                return True
        else:
            return False
