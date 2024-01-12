from pytest_bdd import scenarios, parsers, given, when, then

from hornets.models.manual_discount.models import ManualDiscountReason, ManualDiscountMethod, ManualDiscount

scenarios("../features/mws/discounts_maintenance.feature")

CONVERTERS = {
    "discount_name": str,
    "discount_amount": str,
    "apply_discount_to": str,
    "discount_type": str,
    "amount": float,
}


@given("the user wants to find a discount")
def to_find_discount():
    pass


@when(
    parsers.parse("the user searches for {discount_name} discount"),
    target_fixture="search_result",
    converters=CONVERTERS,
)
def search_discount(discounts_page, discount_name, context):
    context["discount_name"] = discount_name
    return discounts_page.search_discount(discount_name)


@then("the discount should appear on the results")
def discount_search_result(search_result, context):
    assert search_result, f"Discount {context['discount_name']} was not found."


@given("the user adds a new discount", target_fixture="new_discount_config")
def generic(discounts_page):
    discounts_page.open_new_discount_section()
    new_discount_config = {}
    return new_discount_config


@when(parsers.parse("he sets the discount name to {discount_name}"), converters=CONVERTERS)
def set_discount_name(new_discount_config, discount_name):
    new_discount_config["discount_name"] = discount_name


@when(parsers.parse("he sets the discount amount type to be {discount_amount}"), converters=CONVERTERS)
def set_discount_amount_type(new_discount_config, discount_amount):
    new_discount_config["discount_amount"] = discount_amount


@when(parsers.parse("he sets the discount to be applied to {apply_discount_to}"), converters=CONVERTERS)
def set_discount_appy_to(new_discount_config, apply_discount_to):
    new_discount_config["apply_discount_to"] = apply_discount_to


@when(parsers.parse("he sets the discount type to be {discount_type}"), converters=CONVERTERS)
def set_discount_type(new_discount_config, discount_type):
    new_discount_config["discount_type"] = discount_type


@when(parsers.parse("he sets the discount amount to {amount}"), converters=CONVERTERS)
def set_discount_amount(new_discount_config, amount):
    new_discount_config["amount"] = amount


@then("the specified discount should be created")
def create_discount(discounts_page, new_discount_config, context):
    discount = ManualDiscount(
        name=new_discount_config["discount_name"],
        method=ManualDiscountMethod.get_method_from_options(
            discount_amount_type=new_discount_config["discount_amount"],
            apply_discount_to=new_discount_config["apply_discount_to"],
            discount_type=new_discount_config["discount_type"],
        ),
        reason=ManualDiscountReason.MANAGERS_GOODWILL,
        amount=new_discount_config["amount"],
    )
    created_discount = discounts_page.create_discount(discount)

    # Save discount to delete later
    context.setdefault("created_discounts", []).append(created_discount)

    discount_search_result = discounts_page.search_discount(created_discount.name)
    assert discount_search_result, "Created discount was not found in search results."
