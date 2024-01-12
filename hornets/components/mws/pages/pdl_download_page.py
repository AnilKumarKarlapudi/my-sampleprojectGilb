from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.mws.navigation_urls import PDL_DOWNLOAD_PAGE_URL
from hornets.components.mws.pages.mws_page import MwsPage
from hornets.components.mws.mws_locators import PdlDownloadMwsPageLocators


class PdlDownloadMwsPage(MwsPage):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=PDL_DOWNLOAD_PAGE_URL,
            element_to_wait_for=PdlDownloadMwsPageLocators.HEADER,
        )

    def do_not_download_pdl(self):
        """
        Do not download the PDL
        """
        self.click(PdlDownloadMwsPageLocators.NO)

    def download_pdl(self):
        """
        Download the PDL
        """
        self.click(PdlDownloadMwsPageLocators.YES)
        self.wait_for_element_to_load(PdlDownloadMwsPageLocators.SUCCEEDED_MESSAGE)
        self.click(PdlDownloadMwsPageLocators.OK)
