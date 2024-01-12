import pytest

from hornets.base import DropdownOption
from hornets.components.mws.mws_locators import ForecourtInstallationMwsPageLocators
from hornets.components.mws.navigation_urls import FORECOURT_INSTALLATION_PAGE_URL
from hornets.components.mws.pages.forecourt_installation_page.forecourt_installation_page import (
    ForecourtInstallationMwsPage
)


@pytest.mark.mws
class TestMwsForecourtInstallationDispenser:

    def test_edit_mws_dispenser(self, mws_go_to):
        """
        Test that verifies that a dispenser has been edited
        """
        forecourt_installation: ForecourtInstallationMwsPage = mws_go_to(FORECOURT_INSTALLATION_PAGE_URL)
        forecourt_installation.edit_dispenser(
            mws_dispenser_number="1",
            dispenser_changes={
                ForecourtInstallationMwsPageLocators.DISPENSER_MANUFACTURER: "Gilbarco",
                ForecourtInstallationMwsPageLocators.DISPENSER_SERIAL_NUMBER: "12345",
                ForecourtInstallationMwsPageLocators.TDES_SWITCH: True,
                ForecourtInstallationMwsPageLocators.DISPENSER_TYPE: DropdownOption("SINGLE"),
                ForecourtInstallationMwsPageLocators.AUTO_ON: True,
                ForecourtInstallationMwsPageLocators.BAR_CODE: False
            }
        )
        current_dispenser_options = forecourt_installation.get_dispenser("1").mws_dispenser_options.fields

        assert current_dispenser_options[ForecourtInstallationMwsPageLocators.DISPENSER_MANUFACTURER] == "Gilbarco"
        assert current_dispenser_options[ForecourtInstallationMwsPageLocators.DISPENSER_SERIAL_NUMBER] == "12345"
        assert current_dispenser_options[ForecourtInstallationMwsPageLocators.TDES_SWITCH] is True
        assert (current_dispenser_options[ForecourtInstallationMwsPageLocators.DISPENSER_TYPE]
                == DropdownOption("SINGLE"))
        assert current_dispenser_options[ForecourtInstallationMwsPageLocators.AUTO_ON] is True
        assert current_dispenser_options[ForecourtInstallationMwsPageLocators.BAR_CODE] is False
