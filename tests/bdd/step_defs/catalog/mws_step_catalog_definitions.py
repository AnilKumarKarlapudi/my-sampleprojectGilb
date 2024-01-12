from pytest_bdd import given, when, then, parsers

CONVERTERS = {
    'discount_name': str,
}


# GIVEN common step definitions--------------------------------------------------------------------------------
@given('an admin user is on the MWS Login screen', target_fixture="login_page")
def login_page(login_page):
    yield login_page


@given('an admin user is signed on the MWS Discounts Maintenance Page', target_fixture="discounts_page")
@given('an admin user is on the MWS Discounts Page', target_fixture="discounts_page")
def discounts_page(discounts_page):
    yield discounts_page


# WHEN common step definitions--------------------------------------------------------------------------------
@when(
    parsers.parse("the user searches for {discount_name} discount"),
    target_fixture="search_result",
    converters=CONVERTERS
)
def search_discount(discounts_page, discount_name):
    return discounts_page.search_discount(discount_name)


# THEN common step definitions--------------------------------------------------------------------------------
@then(parsers.parse("the discount {discount_name} should appear on the results"),
      converters=CONVERTERS)
def discount_search_result(search_result, discount_name):
    assert search_result, f"Discount {discount_name} was not found."
