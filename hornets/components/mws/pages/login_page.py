from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from hornets.components.mws.navigation_urls import MWS_PAGE_URL
from hornets.components.mws.pages.mws_page import MwsPage
from hornets.components.mws.pages.main_page import MainMwsPage
from hornets.components.mws.mws_locators import LoginMwsPageLocators

from hornets.utilities.log_config import logger
from hornets.utilities.constants import CREDENTIALS


class LoginMwsPage(MwsPage):

    def __init__(self, driver: WebDriver):
        super().__init__(
            driver=driver,
            url=MWS_PAGE_URL,
            element_to_wait_for=LoginMwsPageLocators.USERNAME,
        )

    def get_login_error_message(self) -> str:
        """
        Get the login error message
        Returns:
            str: Login error message
        """
        login_error_message = self.find_element(LoginMwsPageLocators.LOGIN_ERROR_MESSAGE)
        return login_error_message.text

    def login_with_valid_credentials(self) -> MainMwsPage:
        """
        Login with valid credentials
        Return:
            MainMwsPage: MwsMainMwsPage object
        """
        self.wait.until(expected_conditions.element_to_be_clickable((By.XPATH, LoginMwsPageLocators.USERNAME.value)))
        self.click(locator_enum=LoginMwsPageLocators.USERNAME)
        self.__enter_credentials(CREDENTIALS["username"], CREDENTIALS["password"])
        logger.info("Valid credentials entered")
        logger.info("Clicking on Sign On button")
        self.click(LoginMwsPageLocators.SIGN_ON)
        return MainMwsPage(self.driver)

    def login_with_custom_credentials(self, username: str, password: str):
        """
        Login with custom credentials
            Args:
                username(str): Username to login
                password(str): Password to login
        """
        self.__enter_credentials(username, password)
        logger.info("Valid credentials entered")
        logger.info("Clicking on Sign On button")
        self.click(LoginMwsPageLocators.SIGN_ON)

    def __enter_credentials(self, username: str, password: str):
        """
        Enter credentials
        Args:
            username(str): Username to login
            password(str): Password to login
        """
        self.set_value(
            LoginMwsPageLocators.USERNAME,
            value=username
        )
        self.set_value(LoginMwsPageLocators.PASSWORD,
                       value=password
                       )
