import pytest

from hornets.components.mws.navigation_urls import LOYALTY_PAGE_URL


@pytest.mark.mws
@pytest.mark.frontend
class TestMwsGoToFixture:

    def test_mws_go_to_fixture(self, mws_go_to):
        """
        Test that verifies that the go_to_fixture is working as expected
        """
        page = mws_go_to(LOYALTY_PAGE_URL)

        assert page.get_current_url() == LOYALTY_PAGE_URL
        assert page.wait_for_page_to_load()
