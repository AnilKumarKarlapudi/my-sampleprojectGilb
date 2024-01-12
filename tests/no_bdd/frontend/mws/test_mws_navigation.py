import pytest

from hornets.components.mws.enums import FormalNameMwsPageEnum
from hornets.components.mws.pages.discounts_page import DiscountsMwsPage
from hornets.components.mws.pages.forecourt_installation_page.forecourt_installation_page import (
    ForecourtInstallationMwsPage
)
from hornets.components.mws.pages.items.items_page import ItemsMwsPage
from hornets.components.mws.pages.loyalty_page import LoyaltyMwsPage
from hornets.components.mws.pages.registers_page.registers_page import RegistersMwsPage
from hornets.components.mws.pages.site_configuration_page import SiteConfigurationMwsPage
from hornets.components.mws.pages.store_close_page import StoreCloseMwsPage
from hornets.components.mws.pages.pdl_download_page import PdlDownloadMwsPage
from hornets.components.mws.pages.tenders.tenders_page import TendersMwsPage


@pytest.mark.mws
@pytest.mark.frontend
class TestMwsNavigation:

    # Test a basic transaction through POS
    @classmethod
    def setup_class(cls):
        pass

    @pytest.fixture(scope="function")
    def cleanup(self, mws):
        yield
        if self.current_prompt_to_cancel:
            getattr(self.current_page_found, self.current_prompt_to_cancel)()
        mws.clean_up()

    @pytest.mark.parametrize("page_to_search, expected_page_found, prompt_to_cancel_mws_page", [
        (FormalNameMwsPageEnum.DISCOUNTS, DiscountsMwsPage, None),
        (FormalNameMwsPageEnum.ITEMS, ItemsMwsPage, None),
        (FormalNameMwsPageEnum.PDL_DOWNLOAD, PdlDownloadMwsPage, 'do_not_download_pdl'),
        (FormalNameMwsPageEnum.STORE_CLOSE, StoreCloseMwsPage, 'do_not_close_the_store'),
        (FormalNameMwsPageEnum.FORECOURT_INSTALLATION, ForecourtInstallationMwsPage, None),
        (FormalNameMwsPageEnum.REGISTERS, RegistersMwsPage, None),
        (FormalNameMwsPageEnum.TENDERS, TendersMwsPage, None),
        (FormalNameMwsPageEnum.LOYALTY, LoyaltyMwsPage, None),
        (FormalNameMwsPageEnum.SITE_CONFIGURATION, SiteConfigurationMwsPage, None)
    ])
    def test_mws_navigation(self, mws, page_to_search, expected_page_found, prompt_to_cancel_mws_page, cleanup):
        """
        Test that verifies POS login is successful when the POS button is selected
        """
        self.current_page_found = mws.navigate_through_search_display(page_to_search=page_to_search)
        self.current_prompt_to_cancel = prompt_to_cancel_mws_page

        assert self.current_page_found.wait_for_page_to_load()
        assert isinstance(self.current_page_found, expected_page_found)
