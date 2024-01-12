import pytest

from hornets.base import DropdownOption
from hornets.components.mws.mws_locators import RegistersMwsPageLocators


@pytest.mark.mws
@pytest.mark.skip(reason="EDH Restart is required")
class TestMwsRegisters:
    """
    Test different operations inside MWS Registers Screen
    """

    @classmethod
    def setup_class(cls):
        pass

    def test_delete_register(self, registers_page):
        """
        Test that verifies that a dispenser has been deleted
        """
        registers_page.delete_register(register_number="1")
        assert registers_page.verify_register_exist(register_number="1") is not True

    def test_add_register(self, registers_page):
        """
        Test that verifies that a new register has been added
        """
        registers_page.add_register(
            register_config={
                RegistersMwsPageLocators.REGISTER_NUMBER: "1",
                RegistersMwsPageLocators.PINPAD_TYPE: DropdownOption("Verifone MX 915"),
                RegistersMwsPageLocators.IP_ADDRESS: "10.5.50.5",
                RegistersMwsPageLocators.MACHINE_NAME: DropdownOption("POSSERVER01"),
                RegistersMwsPageLocators.REGISTER_GROUP: DropdownOption("POSGroup1"),
                RegistersMwsPageLocators.LINE_DISPLAY: DropdownOption("POS Line Display")
            }
        )
        current_register_options = registers_page.get_register("1")
        assert current_register_options.register_number == "1"
        assert current_register_options.machine_name == "POSSERVER01"

    def test_edit_register(self, registers_page):
        """
        Test that verifies that a register has been edited
        """
        registers_page.edit_register(
            register_number="1",
            register_changes={
                RegistersMwsPageLocators.ASSET_ID: "1",
                RegistersMwsPageLocators.MODEL_NUMBER: "123",
                RegistersMwsPageLocators.SERIAL_NUMBER: "123"
            }
        )
        current_register = registers_page.get_register("1")
        current_register.click(RegistersMwsPageLocators.EDIT, "1")
        assert current_register.register_options.fields[RegistersMwsPageLocators.ASSET_ID] == "1"
        assert current_register.register_options.fields[RegistersMwsPageLocators.MODEL_NUMBER] == "123"
        assert current_register.register_options.fields[RegistersMwsPageLocators.SERIAL_NUMBER] == "123"
