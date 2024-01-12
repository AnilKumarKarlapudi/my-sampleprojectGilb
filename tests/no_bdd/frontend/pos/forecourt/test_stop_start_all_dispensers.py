import pytest

from hornets.components.pos.enums import DispenserStatusEnum


@pytest.mark.frontend
class TestStopAllDispensers:

    # Test a basic transaction through POS
    @classmethod
    def setup_class(cls):
        pass

    def test_stop_all_dispensers(self, pos):
        """
        Test that all dispensers can be stopped
        """
        pos.stop_all_dispensers()

        for dispenser_display in pos.forecourt.dispensers:
            pos.select_dispenser(dispenser_display.get_dispenser_id())

            assert dispenser_display.get_dispenser_status() in {
                DispenserStatusEnum.STOPPED,
                DispenserStatusEnum.INOPERATIVE
            }

    def test_start_all_dispensers(self, pos):
        """
        Test that all dispensers can be started
        """
        pos.start_all_dispensers()

        for dispenser_display in pos.forecourt.dispensers:
            pos.select_dispenser(dispenser_display.get_dispenser_id())

            assert dispenser_display.get_dispenser_status() in {
                DispenserStatusEnum.IDLE,
                DispenserStatusEnum.INOPERATIVE
            }
