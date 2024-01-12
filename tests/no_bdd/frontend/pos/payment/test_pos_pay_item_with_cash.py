import pytest

from hornets.components.pos.enums import WatermarkDisplayEnum
from hornets.models.display_element import DisplayItem


@pytest.mark.frontend
class TestPosPayItemWithCash:

    @classmethod
    def setup_class(cls):
        pass

    @pytest.mark.parametrize("item_to_buy", [
        DisplayItem(name="Item 7", amount=5.00),
        DisplayItem(name="Item 3", amount=15.00)
    ])
    def test_pay_with_cash(self, pos, item_to_buy):
        pos.select_item(item_to_buy)
        transaction = pos.pay()

        assert transaction["watermark"] == WatermarkDisplayEnum.TRANSACTION_COMPLETED
        assert transaction["total_transaction"] == {'total': item_to_buy.amount, 'basket_count': 1}

    @classmethod
    def teardown_class(cls):
        pass
