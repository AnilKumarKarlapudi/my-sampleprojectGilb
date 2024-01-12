from pytest_bdd import scenarios, parsers, when, then, given

from hornets.components.pos.enums import WatermarkDisplayEnum
from hornets.components.pos.payment_method import CashPaymentMethod, CreditCardPaymentMethod
from hornets.models.credit_card.instances import VISA_MAGSTRIPE, MASTERCARD_MAGSTRIPE, VISA_EMV
from hornets.models.display_element import DisplayItem

scenarios("../features/pos/drystock_sale.feature")

CONVERTERS = {
    "item_name": str,
    "item_price": float,
    "payment_method": str,
    "card_name": str,
    "discount_amount": int,
    "total_with_discount": float,
}

# Pay with cash and credit card---------------------------------------------


@when(parsers.parse("he selects the item {item_name} with price {item_price}"), converters=CONVERTERS)
def select_item(pos, item_name, item_price):
    item_to_buy = DisplayItem(name=item_name, amount=item_price)
    pos.select_item(item_to_buy)


@when(
    parsers.parse("he pays with {payment_method} - {card_name}"), target_fixture="transaction", converters=CONVERTERS
)
def pay_with_selected_payment_method(pos, payment_method, card_name, context):
    credit_cards = {
        "Visa": CreditCardPaymentMethod(VISA_MAGSTRIPE),
        "MasterCard": CreditCardPaymentMethod(MASTERCARD_MAGSTRIPE),
        "Emv Visa": CreditCardPaymentMethod(VISA_EMV),
    }
    if payment_method == "Cash":
        context["payment_method"] = CashPaymentMethod()
    elif payment_method == "Credit Card":
        context["payment_method"] = credit_cards[card_name]
    else:
        assert False, "Invalid payment method"
    transaction = pos.pay(context["payment_method"])
    return transaction


@then(
    parsers.parse("the transaction display should have 1 item with {item_price} as total result"),
    converters=CONVERTERS,
)
def transaction_display_info(transaction, item_price):
    assert transaction["total_transaction"] == {"total": item_price, "basket_count": 1}


@then("the transaction should be completed with the selected payment method", converters=CONVERTERS)
def transaction_display_watermark(transaction, context):
    assert transaction["watermark"] == WatermarkDisplayEnum.TRANSACTION_COMPLETED
    assert transaction["payment_method"] == context["payment_method"]


# Pay with cash and applied discount---------------------------------------------
@given(
    parsers.parse("a fixed discount of {discount_amount} amount off is available for {item_name}"),
    converters=CONVERTERS,
)
def created_backend_discount(manual_discount_factory, discount_amount, context):
    discount_created = manual_discount_factory(amount=discount_amount)
    context["discount_created"] = discount_created


@when("he applies the discount", converters=CONVERTERS)
def apply_discount(pos, context):
    pos.apply_discount(context["discount_created"])


@when("he pays the exact amount with Cash", target_fixture="discounted_transaction", converters=CONVERTERS)
def pay_with_cash(pos):
    discounted_transaction = pos.pay()
    return discounted_transaction


@then(
    parsers.parse("the discounted transaction display should have 1 item with {total_with_discount} as total result"),
    converters=CONVERTERS,
)
def discounted_transaction_display_info(discounted_transaction, total_with_discount):
    assert discounted_transaction["total_transaction"] == {"total": total_with_discount, "basket_count": 1}


@then("the discounted transaction should be completed", converters=CONVERTERS)
def discounted_transaction_display_watermark(discounted_transaction):
    assert discounted_transaction["watermark"] == WatermarkDisplayEnum.TRANSACTION_COMPLETED
