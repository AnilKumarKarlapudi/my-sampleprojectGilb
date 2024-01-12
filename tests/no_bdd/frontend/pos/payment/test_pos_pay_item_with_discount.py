import pytest

from hornets.components.exceptions import NotApplicableDiscountException
from hornets.components.pos.enums import WatermarkDisplayEnum
from hornets.models.display_element import DisplayItem


@pytest.mark.frontend
class TestPosPayItemWithDiscount:

    @classmethod
    def setup_class(cls):
        pass

    def test_pos_pay_with_applicable_discount(self, pos, manual_discount_factory):
        discount_created = manual_discount_factory()

        # After creating a new discount via backend, POS needs to be reloaded
        pos.reload()

        item_to_buy = DisplayItem(name="Item 3", amount=15.00)
        pos.select_item(item_to_buy)
        pos.apply_discount(discount_created)
        transaction = pos.pay()

        assert transaction["watermark"] == WatermarkDisplayEnum.TRANSACTION_COMPLETED
        assert transaction["total_transaction"] == {'total': 5, 'basket_count': 1}

    def test_pos_pay_raise_not_applicable_discount_exception(
            self,
            pos,
            manual_discount_factory
    ):
        discount_created = manual_discount_factory()

        # If a transaction is in progress, the discount is not visible and we need to avoid the transaction
        pos.return_to_idle()

        item_to_buy = DisplayItem(name="Item 7", amount=5.00)

        pos.select_item(item_to_buy)

        with pytest.raises(NotApplicableDiscountException):
            pos.apply_discount(discount_created)

        # Return to idle because there is an issue reported in PAU-828
        pos.return_to_idle()

    @classmethod
    def teardown_class(cls):
        pass
