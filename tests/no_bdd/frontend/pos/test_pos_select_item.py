import pytest

from hornets.models.display_element import DisplayItem


@pytest.mark.frontend
class TestPosSelectItem:
    # Test a basic transaction through POS
    @classmethod
    def setup_class(cls):
        pass

    @pytest.mark.parametrize(
        "item_to_select", [DisplayItem(name="Item 7", amount=5.00), DisplayItem(name="Item 3", amount=15.00)]
    )
    def test_select_item_by_text(self, pos, item_to_select):
        """
        Test that an item can be selected by text
        """
        pos.select_item(item_to_select)
        item_selected = pos.transaction.get_last_item_added()

        assert item_selected.name == item_to_select.name
        assert item_selected.amount == item_to_select.amount
