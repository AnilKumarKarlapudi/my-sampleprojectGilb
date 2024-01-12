import random
import string
import pytest
from flaky import flaky

from hornets.components.mws.navigation_urls import DISCOUNTS_PAGE_URL


# from hornets.models.manual_discount.models import ManualDiscount, ManualDiscountMethod, ManualDiscountReason


@pytest.mark.frontend
@pytest.mark.discounts
@flaky(max_runs=2, min_passes=1)
class TestMwsDiscounts:
    # Test different operations inside MWS Discounts Screen
    DISCOUNTS_TO_SEARCH = [
        "Std_Item_Pct",
        "Std_Item_Amt",
    ]

    @classmethod
    def setup_class(cls):
        random_digits = "".join(random.choices(string.digits, k=3))
        cls.new_frontend_discount_name = f"FrontTestDisc{random_digits}"
        cls.new_backend_discount_name = f"BackTestDisc{random_digits}"

    @pytest.fixture(scope="class")
    def discounts_page(self, mws_go_to):
        discounts_page = mws_go_to(DISCOUNTS_PAGE_URL)
        yield discounts_page
        # Delete created discounts after tests class execution.
        discounts_page.delete_discount(self.new_frontend_discount_name)

    @pytest.mark.mws
    @pytest.mark.parametrize("discount_to_search", DISCOUNTS_TO_SEARCH)
    def test_search_discounts(self, discounts_page, discount_to_search):
        """
        Tests that verifies the correct functioning of the discount search feature, using
        the discounts pre-charged by the initial setup.
        """
        discount_search_result = discounts_page.search_discount(discount_to_search)
        assert discount_search_result, f"Discount {discount_to_search} was not found."

    '''
    def test_create_discount_through_mws_gui(self, discounts_page, discount_factory):
        """
        Test for creating a new Discount through the UI and verifying its presence
        on the discounts list.
        """
        discount_config = DiscountConfig(
            discount_name=self.new_frontend_discount_name,
            discount_method=ManualDiscountMethod.ITEM_PERCENTAGE_OFF,
            discount_reason=ManualDiscountReason.MANAGERS_GOODWILL,
            amount=50,
        )
        discounts_page.open_new_discount_section()
        created_discount = discounts_page.create_discount(discount_config)
        assert created_discount, "Discount cannot be created."
        discount_search_result = discounts_page.search_discount(created_discount.discount_name)
        assert discount_search_result, "Created discount was not found in search results."
    '''

    def test_create_discount_through_backend_and_verify_in_mws_gui(
            self,
            discounts_page,
            manual_discount_factory
    ):
        """
        Test for creating a new Discount through the backend and verifying its presence
        on the discounts list.
        """
        api_result = manual_discount_factory(discount_name=self.new_backend_discount_name)
        assert api_result.id > 0, "There was a problem creating the discount through backend API"

        discount_search_result = discounts_page.search_discount(discount_name=self.new_backend_discount_name, delay=5)
        assert discount_search_result, f"Discount {self.new_backend_discount_name} was not found."
