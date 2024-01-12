from operator import eq
import pytest

from libs.common.template_model import ModelFilter

from hornets.models.register.models import Register

pytest.skip("Running these tests make POS void transaction to stop working", allow_module_level=True)


def test_create_register(register_factory, register_configuration_api):
    """
    Test register create
    """
    initial_count = Register.count(register_configuration_api)

    # Create a new register object, do not save in factory function, it will be done here!
    new_register = register_factory(id=2, save_model=False)

    # Check if save returns the same saved register
    result = new_register.save(register_configuration_api)
    assert result == new_register

    # It should increase register count
    assert Register.count(register_configuration_api) > initial_count

    # Get register from system again
    filters = [ModelFilter(field="id", value=new_register.id, operator=eq)]
    filtered = Register.filter(register_configuration_api, filters)

    # It should get only one
    assert len(filtered) == 1

    # That one should be equal to the original
    assert filtered[0] == new_register


def test_update_register(register_factory, register_configuration_api):
    """
    Test register update
    """

    original_asset_id = "123"

    # Use new register
    new_register = register_factory(id=2, asset_id=original_asset_id)

    # Change some value
    new_asset_id = "456"
    new_register.asset_id = new_asset_id

    # Save change
    result = new_register.save(register_configuration_api)
    assert result.asset_id == new_asset_id


def test_delete_register(register_factory, register_configuration_api):
    """
    Test register delete
    """

    # Use new register
    new_register = register_factory(id=2, force_delete=False)  # New register is going to be deleted here

    # Delete object
    assert new_register.delete(register_configuration_api)

    # Get register from system again
    filters = [ModelFilter(field="id", value=new_register.id, operator=eq)]
    filtered = Register.filter(register_configuration_api, filters)

    # It shouldn't get anyone
    assert len(filtered) == 0
