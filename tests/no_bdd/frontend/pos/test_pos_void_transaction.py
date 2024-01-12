import pytest

from hornets.models.display_element import DisplayItem


@pytest.mark.frontend
class TestPosVoidTransaction:
    # Test a basic transaction through POS
    @classmethod
    def setup_class(cls):
        pass

    @pytest.mark.parametrize(
        "item_to_select", [DisplayItem(name="Item 7", amount=5.00), DisplayItem(name="Item 3", amount=15.00)]
    )
    def test_pos_void_transaction(self, pos, item_to_select):
        """
        Test voiding a transaction after selecting an item
        """
        pos.select_item(item_to_select)
        pos.void_transaction()

        assert pos.wait_for_page_to_load()
