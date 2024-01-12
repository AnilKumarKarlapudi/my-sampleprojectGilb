from pytest_bdd import given, when, parsers, then

from hornets.components.pos.enums import WatermarkDisplayEnum
from hornets.models.credit_card.instances import VISA_MAGSTRIPE, MASTERCARD_MAGSTRIPE, VISA_EMV
from hornets.models.display_element import DisplayItem
from hornets.components.pos.payment_method import CreditCardPaymentMethod

CONVERTERS = {
    "item_name": str,
    "item_price": float,
    "payment_method": str,
    "card_name": str,
    "discount_amount": int,
    "total_with_discount": float,
}


# GIVEN common step definitions--------------------------------------------------------------------------------
@given("a cashier is signed on the POS", target_fixture="pos")
def sign_on_pos(pos):
    return pos


# WHEN common step definitions--------------------------------------------------------------------------------
@when(parsers.parse("the cashier selects the item {item_name}"), converters=CONVERTERS)
def select_item(pos, item_name):
    item_to_buy = DisplayItem(name=item_name, amount=1.0)
    pos.select_item(item_to_buy)


@when("the cashier pays with cash exact amount", target_fixture="transaction", converters=CONVERTERS)
def pay_transaction_with_cash(pos):
    transaction = pos.pay()
    return transaction


@when(
    parsers.parse("the cashier pays with {credit_card} credit card"),
    target_fixture="transaction",
    converters=CONVERTERS,
)
def pay_transaction_with_credit_card(pos, credit_card):
    credit_cards = {
        "Visa": CreditCardPaymentMethod(VISA_MAGSTRIPE),
        "MasterCard": CreditCardPaymentMethod(MASTERCARD_MAGSTRIPE),
        "Emv Visa": CreditCardPaymentMethod(VISA_EMV),
    }
    payment_method = credit_cards[credit_card]
    transaction = pos.pay(payment_method)
    return transaction


# THEN common step definitions--------------------------------------------------------------------------------
@then("the transaction should be completed", converters=CONVERTERS)
def transaction_completed_watermark(transaction):
    assert transaction["watermark"] == WatermarkDisplayEnum.TRANSACTION_COMPLETED
