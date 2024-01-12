import pytest

from hornets.utilities.log_config import logger


@pytest.mark.mws
@pytest.mark.frontend
class TestMWSLogin:

    # Tests for MWS Login Screen
    @classmethod
    def setup_class(cls):
        cls.invalid_login_URL_parameter = "?error=Invalid%20operator%20ID%20or%20password"
        cls.expected_login_error_message = "Error Invalid operator ID or password"
        cls.expected_successful_login_url = "https://posserver01:7495/"

    @pytest.mark.parametrize("username, password", [("11", "11"), ("22", "23")])
    def test_login_failed(self, login_page, username, password):
        """
        Test that verifies MWS login is failing when we entered a set of invalid credentials
        """
        logger.info("Testing MWS login failed")
        login_page.login_with_custom_credentials(username, password)
        current_login_error_message = login_page.get_login_error_message()

        assert self.invalid_login_URL_parameter in login_page.get_current_url()
        assert current_login_error_message == self.expected_login_error_message

    def test_login_success(self, login_page):
        """
        Test that verifies MWS login is successful when we entered a set of valid credentials
        """
        logger.info("Testing MWS login success")
        mws_main_page = login_page.login_with_valid_credentials()

        assert mws_main_page.wait_for_page_to_load()
        assert mws_main_page.get_current_url() == self.expected_successful_login_url
