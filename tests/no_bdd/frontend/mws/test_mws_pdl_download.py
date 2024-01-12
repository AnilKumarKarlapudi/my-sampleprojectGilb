import pytest

from hornets.components.mws.pages.main_page import MainMwsPage


@pytest.mark.mws
@pytest.mark.frontend
class TestMwsPdlDownload:

    @classmethod
    def setup_class(cls):
        pass

    def test_reject_downloading_pdl(self, pdl_download_page):
        """
        Test that verifies that PDL Download is not downloaded when the NO button is selected
        """
        pdl_download_page.do_not_download_pdl()

        assert MainMwsPage(pdl_download_page.driver).wait_for_page_to_load()

    def test_accept_downloading_pdl(self, pdl_download_page):
        """
        Test that verifies that PDL Download is downloaded when the YES button is selected
        """
        pdl_download_page.download_pdl()

        assert MainMwsPage(pdl_download_page.driver).wait_for_page_to_load()

    @classmethod
    def teardown_class(cls):
        pass
