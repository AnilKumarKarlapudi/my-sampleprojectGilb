import pytest

from hornets.components.mws.mws_locators import SiteConfigurationLocators


@pytest.mark.mws
@pytest.mark.frontend
@pytest.mark.siteConfiguration
class TestSiteConfiguration:

    def test_site_configuration_page(self, site_configuration_page):
        """
        Test that verifies that network configuration option site has been updated
        """
        # Define test data for the values to modify
        test_values_to_modify = {
            SiteConfigurationLocators.COM_PORT: "0",
            SiteConfigurationLocators.ACCESS_CODE: "123",
            SiteConfigurationLocators.DOWNLOAD_PHONE_NUMBER: "18001111111",
            SiteConfigurationLocators.PRIMARY_PHONE_NUMBER: "18002222222",
            SiteConfigurationLocators.SECONDARY_PHONE_NUMBER: "18003333333",
            SiteConfigurationLocators.INIT_STRING: "AT&F0V0E0&K0&Q6&CX4S37=5&Z0",
            SiteConfigurationLocators.DIAL_HEADER: "HEADER",
            SiteConfigurationLocators.DIAL_TRAILER: "TRAILER",
            SiteConfigurationLocators.CONNECTION_TIMER: "30",
            SiteConfigurationLocators.KEEP_ALIVE_TIME_FRAME_MINUTES: "15",
            SiteConfigurationLocators.DATAWIRE_REGISTRATION_URL: "https://support.datawire.net/nocportal/SRS.do"
        }
        # Perform the edit operation and verify success banner
        site_configuration_page.edit_network_connection_options(test_values_to_modify)
