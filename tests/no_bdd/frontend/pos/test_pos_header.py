import pytest

from hornets.components.pos.pos_locators import StatusInformationLocators


@pytest.mark.frontend
class TestPosHeader:
    """
    Test reload of POS page
    """

    @classmethod
    def setup_class(cls):
        pass

    def test_pos_reload(self, pos):
        pos.reload()

        assert pos.wait_for_page_to_load()

    def test_pos_status_information(self, pos):
        status_information = pos.get_status_information()
        pos.reload()

        # TODO: Verify that the PassportVersion is the one that is displayed in the POS
        assert status_information.find_element(StatusInformationLocators.DEVICE_STATUS).is_displayed()
        # TODO: Map device status and verify that the correct status is displayed
        assert status_information.find_element(StatusInformationLocators.STATUS_INFORMATION).is_displayed()

        status_information.return_to_pos()

    @classmethod
    def teardown_class(cls):
        pass
