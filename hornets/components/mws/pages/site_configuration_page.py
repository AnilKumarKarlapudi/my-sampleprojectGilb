from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.exceptions import ConfigurationNotSavedException
from hornets.components.mws.mws_locators import SiteConfigurationLocators
from hornets.components.mws.navigation_urls import NETWORK_CONFIGURATION_PAGE_URL
from hornets.components.mws.pages.mws_page import MwsPage
from hornets.base import BaseOptions


class SiteConfigurationMwsPage(MwsPage):
    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=NETWORK_CONFIGURATION_PAGE_URL,
            element_to_wait_for=SiteConfigurationLocators.HEADER,
        )
        self.global_network_parameters = {
            "Network Connection Options": NetworkConnectionOptions(driver)
        }

    def get_network_connection_options(self):
        return self.global_network_parameters["Network Connection Options"].get_all_field_values()

    def edit_network_connection_options(self, values_to_modify: dict):
        """
        Modify values to fields
        Args:
            values_to_modify (dict): Values to modify
        Example:
            >>> self.edit_network_connection_options({
            >>>     SiteConfigurationLocators.COM_PORT: "0",
            >>>     SiteConfigurationLocators.BAUD_RATE: "4800",
                    .....
            >>> })
        """
        network_connection_options = self.global_network_parameters["Network Connection Options"]
        self.click(SiteConfigurationLocators.NETWORK_CONECTION_OPTIONS_TAB)
        network_connection_options.set_fields_value(values_to_modify)
        self.click(SiteConfigurationLocators.SAVE_BUTTON)
        if not self.information_has_been_saved(additional_message="Global Network Parameters"):
            raise ConfigurationNotSavedException("Global Network Parameters not edited")


class NetworkConnectionOptions(BaseOptions):
    def __init__(self, driver: WebDriver):
        fields = [
            SiteConfigurationLocators.COM_PORT,
            SiteConfigurationLocators.BAUD_RATE_DROP_DOWN,
            SiteConfigurationLocators.ACCESS_CODE,
            SiteConfigurationLocators.DOWNLOAD_PHONE_NUMBER,
            SiteConfigurationLocators.PRIMARY_PHONE_NUMBER,
            SiteConfigurationLocators.SECONDARY_PHONE_NUMBER,
            SiteConfigurationLocators.INIT_STRING,
            SiteConfigurationLocators.DIAL_HEADER,
            SiteConfigurationLocators.DIAL_TRAILER,
            SiteConfigurationLocators.DTMF_SPEED_DROP_DOWN,
            SiteConfigurationLocators.CONNECTION_TIMER,
            SiteConfigurationLocators.HOST_IP_ADDRESS,
            SiteConfigurationLocators.IP_PORT,
            SiteConfigurationLocators.KEEP_ALIVE_TIME_FRAME_MINUTES,
            SiteConfigurationLocators.DATAWIRE_REGISTRATION_URL
        ]
        super().__init__(driver, fields)
