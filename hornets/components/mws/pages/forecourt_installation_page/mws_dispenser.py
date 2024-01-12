from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.base import Base, BaseOptions
from hornets.components.mws.mws_locators import ForecourtInstallationMwsPageLocators, MainMwsPageLocators
from hornets.components.mws.pages.forecourt_installation_page.mws_grade import MwsGrade
from hornets.components.mws.pages.forecourt_installation_page.mws_product import MwsProduct


class MwsDispenser(Base):

    def __init__(
            self,
            driver: WebDriver,
            dispenser_number,
            pump_protocol,
            payment_terminal_type,
            dispenser_type,
            connection,
    ):
        super().__init__(driver)
        self.dispenser_number = dispenser_number
        self.pump_protocol = pump_protocol
        self.payment_terminal_type = payment_terminal_type
        self.dispenser_type = dispenser_type
        self.connection = connection
        self.mws_dispenser_options = MwsDispenserOptions(driver)
        self.products: list[MwsProduct] = []
        self.grades: list[MwsGrade] = []

    def edit_dispenser(self, dispenser_changes: dict):
        self.mws_dispenser_options.set_fields_value(dispenser_changes)
        self.click(ForecourtInstallationMwsPageLocators.DISPENSER_SAVE_BUTTON)
        self.click(MainMwsPageLocators.SAVE_BUTTON)


class MwsDispenserOptions(BaseOptions):

    def __init__(self, driver: WebDriver):
        fields = [
            ForecourtInstallationMwsPageLocators.DISPENSER_MANUFACTURER,
            ForecourtInstallationMwsPageLocators.DISPENSER_SERIAL_NUMBER,
            ForecourtInstallationMwsPageLocators.DISPENSER_TYPE,
            ForecourtInstallationMwsPageLocators.PUMP_PROTOCOL,
            ForecourtInstallationMwsPageLocators.PAYMENT_TERMINAL_TYPE,
            ForecourtInstallationMwsPageLocators.USE_IP_ADDRESS_FOR_PUMP,
            ForecourtInstallationMwsPageLocators.PUMP_IP_ADDRESS,
            ForecourtInstallationMwsPageLocators.TDES_SWITCH,
            ForecourtInstallationMwsPageLocators.BILL_ACCEPTOR,
            ForecourtInstallationMwsPageLocators.BAR_CODE,
            ForecourtInstallationMwsPageLocators.AUTO_ON,
            ForecourtInstallationMwsPageLocators.DOOR_ALARM,
            ForecourtInstallationMwsPageLocators.COMMERCIAL_DIESEL,
            ForecourtInstallationMwsPageLocators.REFER
        ]
        super().__init__(driver, fields)
