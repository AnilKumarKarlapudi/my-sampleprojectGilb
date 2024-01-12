import random

import pytest

from hornets.components.exceptions import ElementNotFoundException
from hornets.components.mws.navigation_urls import FORECOURT_INSTALLATION_PAGE_URL
from hornets.components.mws.pages.forecourt_installation_page.forecourt_installation_page import \
    ForecourtInstallationMwsPage
from hornets.components.mws.pages.forecourt_installation_page.mws_product import MwsProduct


@pytest.mark.mws
class TestMwsForecourtInstallationProduct:

    @classmethod
    def setup_class(cls):
        cls.product_created = f"Test Product {random.randint(0, 1000)}"

    @pytest.fixture(scope="function")
    def forecourt_installation(self, mws_go_to):
        forecourt_installation: ForecourtInstallationMwsPage = mws_go_to(FORECOURT_INSTALLATION_PAGE_URL)
        yield forecourt_installation
        forecourt_installation.delete_product(mws_product_name=self.product_created)

    def test_add_product(self, forecourt_installation):
        """
        Test that verifies that a new product has been added
        """

        product_created = forecourt_installation.add_product(
            product_name=self.product_created
        )

        assert isinstance(product_created, MwsProduct)
        assert forecourt_installation.get_product(product_created.product_number)

    def test_delete_product(self, mws_go_to):
        """
        Test that verifies that a product has been deleted
        """
        forecourt_installation: ForecourtInstallationMwsPage = mws_go_to(FORECOURT_INSTALLATION_PAGE_URL)

        product_created = forecourt_installation.add_product(
            product_name=f"Test Product {random.randint(0, 1000)}"
        )

        forecourt_installation.delete_product(mws_product_name=product_created.product_name)

        with pytest.raises(ElementNotFoundException):
            forecourt_installation.get_product(product_created.product_name)
