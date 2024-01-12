import pytest

from hornets.components.pos.enums import WatermarkDisplayEnum
from hornets.models.display_element import DisplayItem


@pytest.mark.frontend
class TestPosPaySeveralItemsWithCash:

    @classmethod
    def setup_class(cls):
        cls.items_to_buy = [DisplayItem(name="Item 7", amount=5.00), DisplayItem(name="Item 3", amount=15.00)]

    def test_pos_pay_several_items_with_cash(self, pos):
        for item_to_buy in self.items_to_buy:
            pos.select_item(item_to_buy)
        transaction = pos.pay()

        item_sum = sum([item.amount for item in self.items_to_buy])
        item_quantity = len(self.items_to_buy)

        assert transaction["watermark"] == WatermarkDisplayEnum.TRANSACTION_COMPLETED
        assert transaction["total_transaction"] == {'total': item_sum, 'basket_count': item_quantity}

    @classmethod
    def teardown_class(cls):
        pass
