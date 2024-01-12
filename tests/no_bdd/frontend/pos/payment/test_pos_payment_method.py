import pytest

from hornets.components.pos.enums import WatermarkDisplayEnum
from hornets.components.pos.payment_method import CashPaymentMethod, CreditCardPaymentMethod
from hornets.models.credit_card.instances import VISA_MAGSTRIPE, VISA_EMV, MASTERCARD_MAGSTRIPE
from hornets.models.display_element import DisplayItem


@pytest.mark.frontend
class TestPosPaymentMethod:
    @classmethod
    def setup_class(cls):
        pass

    @pytest.mark.parametrize(
        "payment_method",
        [
            CashPaymentMethod(),
            CreditCardPaymentMethod(VISA_MAGSTRIPE),
            CreditCardPaymentMethod(MASTERCARD_MAGSTRIPE),
            CreditCardPaymentMethod(VISA_EMV),
        ],
    )
    def test_pay_payment_method(self, pos, payment_method):
        item_to_buy = DisplayItem(name="Item 7", amount=5.00)
        pos.select_item(item_to_buy)
        transaction = pos.pay(payment_method)

        assert transaction["watermark"] == WatermarkDisplayEnum.TRANSACTION_COMPLETED
        assert transaction["payment_method"] == payment_method

    @classmethod
    def teardown_class(cls):
        pass
