import pytest


@pytest.mark.frontend
class TestPosSignOn:

    # Test a basic transaction through POS
    @classmethod
    def setup_class(cls):
        pass

    def test_pos_sign_on(self, pos):
        """
        Test that verifies POS sign on
        """
        pos.logout()
        pos.logged_in()

        assert pos.wait_for_page_to_load()
