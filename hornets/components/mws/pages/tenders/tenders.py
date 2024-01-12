from selenium.webdriver.chrome.webdriver import WebDriver
from hornets.components.mws.mws_locators import TendersMwsPageLocators

from hornets.base import Base, BaseOptions


class Tender(Base):
    def __init__(self, description, code, status, driver: WebDriver):
        super().__init__(driver)
        self.tender_description = description
        self.code = code
        self.status = status
        self.tender_options = TendersOptions(self.driver)

    def get_tender_options(self):
        return self.tender_options.fields

    def edit_tender(self, values_to_edit):
        self.tender_options.set_fields_value(values_to_edit)


class TendersOptions(BaseOptions):

    def __init__(self, driver: WebDriver):
        fields = [
            TendersMwsPageLocators.TENDER_DESCRIPTION,
            TendersMwsPageLocators.TENDER_GROUP,
            TendersMwsPageLocators.TENDER_ENABLE_SAFE_DROPS,
            TendersMwsPageLocators.TENDER_PRINT_TAX_INVOICE,
            TendersMwsPageLocators.TENDER_RECEIPT_DESCRIPTION,
            TendersMwsPageLocators.TENDER_BUTTON_DESCRIPTION,
            TendersMwsPageLocators.NACS_TENDER_CODE,
        ]

        super().__init__(driver, fields)
