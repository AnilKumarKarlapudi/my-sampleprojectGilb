"""
import pytest

from hornets.models.credit_card.instances import VISA_MAGSTRIPE, MASTERCARD_MAGSTRIPE, VISA_EMV
from hornets.models.display_element import DisplayItem


# from hornets.components.edh.domain.network.message_checker import MessageCheckerEnum


from hornets.components.pos.payment_method import CreditCardPaymentMethod

@pytest.mark.frontend
class TestPosNetworkMessages:
    @classmethod
    def setup_class(cls):
        pass

    @pytest.mark.parametrize("credit_card", [VISA_MAGSTRIPE, MASTERCARD_MAGSTRIPE, VISA_EMV])
    def test_pos_network_messages_valid_transaction_using_bank_card(
        self, pos, last_known_message, message_validator, credit_card
    ):
        item_to_buy = DisplayItem(name="Item 7", amount=5.00)
        pos.select_item(item_to_buy)
        credit_card_payment_method = CreditCardPaymentMethod(credit_card)
        pos.pay(credit_card_payment_method)

        assert message_validator(MessageCheckerEnum.DRY_STOCK_TRANSACTION_USING_BANK_CARD(credit_card=credit_card))

    @classmethod
    def teardown_class(cls):
        pass
"""
