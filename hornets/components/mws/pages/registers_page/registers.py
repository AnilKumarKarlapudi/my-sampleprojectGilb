from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.base import Base, BaseOptions
from hornets.components.mws.mws_locators import RegistersMwsPageLocators, MainMwsPageLocators


class MwsRegisters(Base):

    def __init__(self, driver: WebDriver, register_number, machine_name, personality):
        super().__init__(driver)
        self.register_number = register_number
        self.machine_name = machine_name
        self.personality = personality
        self.register_options = RegisterOptions(driver)

    def edit_register(self, register_changes: dict):
        self.register_options.set_fields_value(register_changes)
        self.click(MainMwsPageLocators.SAVE_BUTTON)


class RegisterOptions(BaseOptions):

    def __init__(self, driver: WebDriver):
        fields = [
            RegistersMwsPageLocators.REGISTER_NUMBER,
            RegistersMwsPageLocators.MACHINE_NAME,
            RegistersMwsPageLocators.REGISTER_GROUP,
            RegistersMwsPageLocators.PERSONALITY,
            RegistersMwsPageLocators.ASSET_ID,
            RegistersMwsPageLocators.MODEL_NUMBER,
            RegistersMwsPageLocators.SERIAL_NUMBER,
            RegistersMwsPageLocators.LINE_DISPLAY,
            RegistersMwsPageLocators.PINPAD_TYPE,
            RegistersMwsPageLocators.IP_ADDRESS,
            RegistersMwsPageLocators.PRINTER_TYPE,
            RegistersMwsPageLocators.ELECTRONIC_SIGNATURE,
            RegistersMwsPageLocators.REBOOT_PINPAD
        ]
        super().__init__(driver, fields)
