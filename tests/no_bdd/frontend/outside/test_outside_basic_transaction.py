import pytest
from flaky import flaky

from hornets.components.dispenser_with_crind import DispenserWithCrind
from hornets.models.credit_card.instances import VISA_MAGSTRIPE, MASTERCARD_MAGSTRIPE


@flaky(max_runs=5, min_passes=1)
@pytest.mark.outside
class TestOutsideBasicTransaction:

    @classmethod
    def setup_class(cls):
        pass

    @pytest.mark.parametrize("credit_card", [
        VISA_MAGSTRIPE,
        MASTERCARD_MAGSTRIPE
    ])
    def test_outside_basic_transaction(self, credit_card):
        """
        This test is a basic transaction using the crindsim
        """
        dispenser_with_crind = DispenserWithCrind(dispenser_id="1")
        dispenser_with_crind.fuel_transaction(credit_card=credit_card)

        assert dispenser_with_crind.check_receipt_for([credit_card.get_last_four_digits()])

    @classmethod
    def teardown_class(cls):
        pass
