from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.exceptions import ElementNotFoundException
from hornets.components.mws.mws_locators import TendersMwsPageLocators
from hornets.components.mws.navigation_urls import TENDERS_PAGE_URL
from hornets.components.mws.pages.tenders.tenders import Tender, TendersOptions
from hornets.components.mws.pages.mws_page import MwsPage


class TendersMwsPage(MwsPage):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=TENDERS_PAGE_URL,
            element_to_wait_for=TendersMwsPageLocators.HEADER,
        )
        self.tenders = []

    def get_tender(self, tender_code):
        try:
            self.get_all_tenders()
            return next(
                tender for tender in self.tenders
                if tender.code == tender_code
            )
        except StopIteration:
            raise ElementNotFoundException(f"Tender #{tender_code} not found")

    def get_all_tenders(self):
        tenders = self.find_elements(TendersMwsPageLocators.TENDERS)
        for tender in tenders:
            tender_values = self.get_values_from_row(tender)
            self.tenders.append(
                Tender(
                    driver=self.driver,
                    description=tender_values[0],
                    code=tender_values[1],
                    status=tender_values[2],
                )
            )
        return tenders

    def add_tender(self, values_to_add: dict):
        self.click(TendersMwsPageLocators.ADD)
        tender_options = TendersOptions(self.driver)
        tender_options.set_fields_value(values_to_add)
        self.click(TendersMwsPageLocators.SAVE_BUTTON)

    def edit_tender(self, tender_code: str, values_to_edit: dict) -> Tender:
        tender = self.get_tender(tender_code)
        self.click(TendersMwsPageLocators.EDIT_TENDER, tender_code)
        tender.edit_tender(values_to_edit)
        self.click(TendersMwsPageLocators.SAVE_BUTTON)
        return tender
