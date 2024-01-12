import datetime
import pytest

from hornets.models.employee import Employee
from hornets.models.manual_discount.enums import ManualDiscountMethod, ManualDiscountReason
from hornets.models.manual_discount.models import ManualDiscount
from hornets.models.speedkey import SpeedKey
from hornets.models.telephone import Telephone


# Manual Discount
@pytest.fixture(scope="class")
def manual_discount(manual_discount_configuration_api):
    discount_created = ManualDiscount(
        name="GRPC Manual Discount",
        method=ManualDiscountMethod.ITEM_AMOUNT_OFF,
        reason=ManualDiscountReason.MANAGERS_GOODWILL,
        amount=5.0,
    )
    yield discount_created
    discount_created.delete(manual_discount_configuration_api)


# SpeedKeys
@pytest.fixture(scope="class")
def speedkey_13():
    return SpeedKey(
        plu="1",
        caption="GRPC_13",
        position=13,
    )


@pytest.fixture(scope="class")
def speedkey_14():
    return SpeedKey(
        plu="1",
        caption="GRPC_14",
        position=14,
    )


@pytest.fixture(scope="class")
def new_employee(employee_configuration_api):
    # Get all employees id numbers
    used_ids = [
        int(emp.id)
        for emp in Employee.all(employee_configuration_api)
        if emp.id.isnumeric()
    ]

    # Create a new employee using the next id number available
    new_obj = Employee(
        id=str(max(used_ids) + 1),
        first_name="Name",
        last_name="Test",
        date_of_birth=datetime.datetime(1980, 1, 1),
        telephone=Telephone(area_code="123", number="1234567"),
        active=True,
        security_group=10005  # TODO: ensure valid security group
    )
    yield new_obj
    new_obj.delete(employee_configuration_api)


@pytest.fixture(scope="class")
def owner_employee():
    yield Employee(id="91")  # TODO: find any owner employee?
