from hornets.models.employee import Employee
from libs.common.template_model import ModelFilter
from operator import eq


def test_get_mandatory_owner_employee(owner_employee, employee_configuration_api):
    """
    Verifies if owner employee is configured in system
    """
    filters = [ModelFilter(field="id", value="91", operator=eq)]

    filtered_employees = Employee.filter(employee_configuration_api, filters)

    assert len(filtered_employees) == 1
    assert owner_employee in filtered_employees


def test_create_delete_employee(new_employee, employee_configuration_api):
    """
    Test employee create and delete.
    Is convenient to test both together because employee deletion is not immediately.
    Delete employee action marks as inactive and it will be deleted eventually during a purge
    """
    initial_count = Employee.count(employee_configuration_api)

    saved_employee = new_employee.save(employee_configuration_api)

    # Check area code to test compose field
    assert saved_employee.telephone.area_code == "123"

    assert Employee.count(employee_configuration_api) > initial_count

    # Delete employee
    assert saved_employee.delete(employee_configuration_api)

    # Get employee from system again
    filters = [ModelFilter(field="id", value=new_employee.id, operator=eq)]
    filtered_employees = Employee.filter(employee_configuration_api, filters)

    # It should be inactive to be marked for deletion
    assert filtered_employees[0].active is False
