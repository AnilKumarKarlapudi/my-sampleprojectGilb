from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.mws.enums import FormalNameMwsPageEnum
from hornets.components.mws.mws_locators import MainMwsPageLocators
from hornets.components.mws.navigation_urls import (
    MWS_PAGE_URL,
    LOYALTY_PAGE_URL,
    DISCOUNTS_PAGE_URL,
    ITEMS_PAGE_URL,
    PDL_DOWNLOAD_PAGE_URL,
    STORE_CLOSE_PAGE_URL,
    FORECOURT_INSTALLATION_PAGE_URL,
    REGISTERS_PAGE_URL,
    TENDERS_PAGE_URL,
    NETWORK_CONFIGURATION_PAGE_URL
)
from hornets.components.mws.pages.forecourt_installation_page.forecourt_installation_page import (
    ForecourtInstallationMwsPage
)
from hornets.components.mws.pages.loyalty_page import LoyaltyMwsPage
from hornets.components.mws.pages.mws_page import MwsPage
from hornets.components.mws.pages.discounts_page import DiscountsMwsPage
from hornets.components.mws.pages.items.items_page import ItemsMwsPage
from hornets.components.mws.pages.registers_page.registers_page import RegistersMwsPage
from hornets.components.mws.pages.site_configuration_page import SiteConfigurationMwsPage
from hornets.components.mws.pages.store_close_page import StoreCloseMwsPage
from hornets.components.mws.pages.pdl_download_page import PdlDownloadMwsPage
from hornets.components.mws.pages.pos_page import PosMwsPage
from hornets.components.mws.pages.tenders.tenders_page import TendersMwsPage
from hornets.utilities.log_config import logger


class MainMwsPage(MwsPage):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=MWS_PAGE_URL,
            element_to_wait_for=MainMwsPageLocators.SEARCH_BUTTON,
        )
        self.page_mapping_through_formal_name = {
            "Discounts": DiscountsMwsPage,
            "Items": ItemsMwsPage,
            "PDL Download": PdlDownloadMwsPage,
            "Store Close": StoreCloseMwsPage,
            "Forecourt Installation": ForecourtInstallationMwsPage,
            "Registers": RegistersMwsPage,
            "Tenders": TendersMwsPage,
            "Loyalty": LoyaltyMwsPage,
            "Site Configuration": SiteConfigurationMwsPage,
        }
        self.page_mapping_through_url = {
            DISCOUNTS_PAGE_URL: DiscountsMwsPage,
            ITEMS_PAGE_URL: ItemsMwsPage,
            PDL_DOWNLOAD_PAGE_URL: PdlDownloadMwsPage,
            STORE_CLOSE_PAGE_URL: StoreCloseMwsPage,
            FORECOURT_INSTALLATION_PAGE_URL: ForecourtInstallationMwsPage,
            REGISTERS_PAGE_URL: RegistersMwsPage,
            TENDERS_PAGE_URL: TendersMwsPage,
            LOYALTY_PAGE_URL: LoyaltyMwsPage,
            NETWORK_CONFIGURATION_PAGE_URL: SiteConfigurationMwsPage,
        }

    def clean_up(self):
        """
        Clean up MWS
        """
        logger.info("Cleaning up MWS")
        self.click(MainMwsPageLocators.LOGO)
        self.wait_for_page_to_load()

    def navigate_through_search_display(self, page_to_search: FormalNameMwsPageEnum) -> MwsPage:
        """
        Navigate through the application using the search display
        """
        self.click(MainMwsPageLocators.SEARCH_BUTTON)
        logger.info(f"Searching for {page_to_search}")
        self.set_value(MainMwsPageLocators.MENU_SEARCH, value=page_to_search.value)
        self.click(MainMwsPageLocators.SEARCH_RESULT, additional_attribute=page_to_search.value)
        result = self.page_mapping_through_formal_name.get(page_to_search.value)
        if not result:
            logger.info(f"Page {page_to_search} not found")
            raise Exception(f"Page {page_to_search} not found")
        return result(self.driver)

    def navigate_through_url(self, url: str) -> MwsPage:
        """
        Navigate through the application using the url
        """
        self.driver.get(url)
        result = self.page_mapping_through_url.get(url)
        if not result:
            logger.info(f"Page {url} not found")
            raise Exception(f"URL: {url} not loaded")
        return result(self.driver)

    def navigate_to_pos(self) -> PosMwsPage:
        """
        Navigate to POS
        Return:
            PosMwsPage: PosMwsPage object
        """
        self.click(MainMwsPageLocators.POS_BUTTON)
        return PosMwsPage(self.driver)
