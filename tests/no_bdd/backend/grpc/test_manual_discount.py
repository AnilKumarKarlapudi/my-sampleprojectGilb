from hornets.models.manual_discount.models import ManualDiscount
from libs.common.template_model import ModelFilter
from operator import eq


def test_create_delete_manual_discount(manual_discount, manual_discount_configuration_api):
    initial_count = ManualDiscount.count(manual_discount_configuration_api)

    saved_discount = manual_discount.save(manual_discount_configuration_api)
    assert saved_discount.id > 0

    assert ManualDiscount.count(manual_discount_configuration_api) > initial_count

    assert saved_discount.delete(manual_discount_configuration_api)

    assert ManualDiscount.count(manual_discount_configuration_api) == initial_count


def test_exists(manual_discount, manual_discount_configuration_api):
    saved_discount = manual_discount.save(manual_discount_configuration_api)
    assert saved_discount.exists(manual_discount_configuration_api)

    assert saved_discount.delete(manual_discount_configuration_api)

    assert not saved_discount.exists(manual_discount_configuration_api)


def test_filter(manual_discount, manual_discount_configuration_api):
    filters = [ModelFilter(field="name", value="GRPC Manual Discount", operator=eq)]

    saved_discount = manual_discount.save(manual_discount_configuration_api)

    assert saved_discount in ManualDiscount.filter(manual_discount_configuration_api, filters)
