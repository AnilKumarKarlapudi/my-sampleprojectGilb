import pytest


@pytest.mark.frontend
class TestPOSTransaction:

    # Test a basic transaction through POS
    @classmethod
    def setup_class(cls):
        pass

    def test_pos_login(self, mws):
        """
        Test that verifies POS login is successful when the POS button is selected
        """
        pos = mws.navigate_to_pos()

        assert pos.wait_for_page_to_load()
