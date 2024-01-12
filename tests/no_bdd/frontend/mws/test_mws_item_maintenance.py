import os
import random

import pytest

from hornets.base import DropdownOption
from hornets.components.mws.mws_locators import ItemsMwsPageLocators
from hornets.components.mws.navigation_urls import ITEMS_PAGE_URL
from hornets.components.mws.pages.items.items_search import ItemSearchByDescription


@pytest.mark.mws
@pytest.mark.items
class TestSearchItems:

    def test_item_search_with_no_input(self, items_page):
        """
        Test item search with no input. Should bring all existing items.
        """
        results = items_page.search_items()
        assert results

    def test_item_search_with_no_input_but_with_filters(self, items_page):
        """
        Test item search with no input but with two filters for Dept 1 department and Regular Item type.
        """
        items_page.item_search_strategy.department_to_search = DropdownOption("Dept 1")
        items_page.item_search_strategy.item_type_to_search = DropdownOption("Regular Item")

        results = items_page.search_items()

        assert all([item.department.locator_value == "Dept 1" for item in results])

    def test_item_search_with_default_plu_strategy(self, items_page):
        """
        Test item search with default strategy (by PLU).
        """
        item_plu = "002"
        results = items_page.search_items(search_input_value=item_plu)

        assert all([item_plu in item_found.plu for item_found in results])

    def test_item_search_with_description_strategy(self, items_page):
        """
        Test item search with new strategy to search by Description with deparment ant type filters.
        """
        item_description_to_search = "Item 3"
        items_page.item_search_strategy = ItemSearchByDescription(
            department_to_search=DropdownOption("Dept 1"),
            item_type_to_search=DropdownOption("Regular Item")
        )

        results = items_page.search_items(search_input_value=item_description_to_search)

        assert all([item_description_to_search in item_found.description for item_found in results])


@pytest.mark.mws
@pytest.mark.items
class TestAddItems:

    @pytest.fixture(scope="function")
    def new_item_to_edit(self, items_page):
        item = items_page.add_item(
            plu=f"0000040{random.randint(0, 100000)}",
            description="Test Item",
            department=DropdownOption("Dept 1"),
            price_option=1,
            unit_price=1.5
        )
        yield item

    @pytest.fixture(scope="function")
    def teardown(self, items_page):
        yield
        if items_page.get_current_url != ITEMS_PAGE_URL:
            items_page.press_back()

    def test_create_item_with_several_options_in_mws_without_save(
            self,
            items_page,
            teardown
    ):
        """
        Test to verify the creation of a complex Item with options in MWS, but without saving.
        """
        additional_options = {
            ItemsMwsPageLocators.TYPE_DROPDOWN: DropdownOption("Regular Item"),
            ItemsMwsPageLocators.DISCOUNTABLE: True,
            ItemsMwsPageLocators.FEE: True,
            ItemsMwsPageLocators.ALLOW_REFUNDS: False,
            ItemsMwsPageLocators.RETURN_PRICE: "5.99",
            ItemsMwsPageLocators.RESTRICTION_GROUP: DropdownOption("Must be 18 (PDI)"),
            ItemsMwsPageLocators.CASH_SWITCH: True,
            ItemsMwsPageLocators.CHECK_SWITCH: True,
            ItemsMwsPageLocators.MONEY_ORDER_SWITCH: True,
            ItemsMwsPageLocators.FOODSTAMPS_SWITCH: True,
            ItemsMwsPageLocators.EBT_SWITCH: True,
            ItemsMwsPageLocators.GIFT_CERTIFICATES_SWITCH: True,
            ItemsMwsPageLocators.CREDIT_CARDS_SWITCH: True,
            ItemsMwsPageLocators.FLEET_CARDS_SWITCH: True,
            ItemsMwsPageLocators.DEBIT_CARDS_SWITCH: True,

        }

        item = items_page.add_item(
            plu=f"0000040{random.randint(0, 100000)}",
            description="Test Item",
            department=DropdownOption("Dept 8"),
            price_option=1,
            unit_price=5.99,
            additional_options=additional_options,
            save=False
        )

        assert items_page.is_save_enabled()
        assert not item

    @pytest.mark.skipif(
        os.getenv("environment") == "local",
        reason="We skip the test if we are running on local environment to avoid overloading "
               "our local configurations, since items cannot be deleted."
    )
    def test_create_item_in_mws(self, items_page):
        """
        Test to verify the creation of a basic Item in MWS.
        """
        additional_options = {
            ItemsMwsPageLocators.TYPE_DROPDOWN: DropdownOption("Regular Item"),
            ItemsMwsPageLocators.DISCOUNTABLE: True,
            ItemsMwsPageLocators.FEE: False,
            ItemsMwsPageLocators.ALLOW_REFUNDS: True,
            ItemsMwsPageLocators.RETURN_PRICE: "2.99",
            ItemsMwsPageLocators.RESTRICTION_GROUP: DropdownOption("Must be 18 (PDI)"),
            ItemsMwsPageLocators.CASH_SWITCH: True,
            ItemsMwsPageLocators.CHECK_SWITCH: True,
            ItemsMwsPageLocators.MONEY_ORDER_SWITCH: True,
            ItemsMwsPageLocators.FOODSTAMPS_SWITCH: True,
            ItemsMwsPageLocators.EBT_SWITCH: True,
            ItemsMwsPageLocators.GIFT_CERTIFICATES_SWITCH: True,
            ItemsMwsPageLocators.CREDIT_CARDS_SWITCH: False,
            ItemsMwsPageLocators.FLEET_CARDS_SWITCH: True,
            ItemsMwsPageLocators.DEBIT_CARDS_SWITCH: True,
        }
        random_plu = f"0000040{random.randint(0, 100000)}"
        item = items_page.add_item(
            plu=random_plu,
            description="Test Item",
            department=DropdownOption("Dept 8"),
            price_option=1,
            unit_price=3.99,
            additional_options=additional_options
        )

        assert item
        assert items_page.item_exists(item)

        assert item.plu == random_plu
        assert item.description == "Test Item"
        assert item.department == DropdownOption("Dept 8")
        assert item.price_option == 1
        assert item.unit_price == 3.99

        item_options = item.get_options()

        assert item_options[ItemsMwsPageLocators.TYPE_DROPDOWN] == DropdownOption("Regular Item")
        assert item_options[ItemsMwsPageLocators.DISCOUNTABLE] is True
        assert item_options[ItemsMwsPageLocators.FEE] is False
        assert item_options[ItemsMwsPageLocators.RETURN_PRICE] == "2.99"
        assert item_options[ItemsMwsPageLocators.RESTRICTION_GROUP] == DropdownOption("Must be 18 (PDI)")
        assert item_options[ItemsMwsPageLocators.CASH_SWITCH] is True
        assert item_options[ItemsMwsPageLocators.DEBIT_CARDS_SWITCH] is True

    @pytest.mark.skipif(os.getenv("environment") == "local",
                        reason="We skip the test if we are running on local environment to avoid overloading "
                               "our local configurations, since items cannot be deleted.")
    def test_edit_item_in_mws(self, items_page, new_item_to_edit):
        """
        Test to verify the edition of a basic Item in MWS.
        """
        options_to_edit = {
            ItemsMwsPageLocators.DESCRIPTION_INPUT: "Edited Item",
            ItemsMwsPageLocators.DEPARTMENT_DROPDOWN: DropdownOption("Dept 2"),
            ItemsMwsPageLocators.DISCOUNTABLE: True,
            ItemsMwsPageLocators.FEE: True,
            ItemsMwsPageLocators.CASH_SWITCH: True,
            ItemsMwsPageLocators.CHECK_SWITCH: True,
            ItemsMwsPageLocators.RETURN_PRICE: "5.5",
        }

        # Price options are handled separately due to some problematic behavior of the fields involved
        edited_price_options = {
            "price_option": 2,
            "unit_price": 9.99,
            "deal_quantity": 4
        }

        edited_item = items_page.edit_item(
            item_plu=new_item_to_edit.plu,
            options_to_edit=options_to_edit,
            price_options_to_edit=edited_price_options
        )

        assert edited_item

        assert edited_item.plu == new_item_to_edit.plu
        assert edited_item.price_option == 2
        assert edited_item.unit_price == 9.99
        assert edited_item.deal_quantity == 4

        edited_item_options = edited_item.get_options()

        assert edited_item_options[ItemsMwsPageLocators.DESCRIPTION_INPUT] == "Edited Item"
        assert edited_item_options[ItemsMwsPageLocators.DEPARTMENT_DROPDOWN] == DropdownOption("Dept 2")
        assert edited_item_options[ItemsMwsPageLocators.BASE_PLUS_ONE_RADIO] is True
        assert edited_item_options[ItemsMwsPageLocators.BASE_PLUS_ONE_UNITPRICE_INPUT] == "9.99"
        assert edited_item_options[ItemsMwsPageLocators.BASE_PLUS_ONE_DEALQUANTITY_INPUT] == "4"
        assert edited_item_options[ItemsMwsPageLocators.DISCOUNTABLE] is True
        assert edited_item_options[ItemsMwsPageLocators.FEE] is True
        assert edited_item_options[ItemsMwsPageLocators.RETURN_PRICE] == "5.5"
        assert edited_item_options[ItemsMwsPageLocators.CASH_SWITCH] is True
        assert edited_item_options[ItemsMwsPageLocators.CHECK_SWITCH] is True
