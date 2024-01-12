import pytest
from unittest import mock

from flaky import flaky

from hornets.models.display_element import DisplayItem
from hornets.components.exceptions import DataInconsistencyException
from hornets.components.pos.transaction.transaction_display import TransactionDisplay


@flaky(max_runs=5, min_passes=1)
@pytest.mark.frontend
class TestValidateConsistencyInTransactions:
    @classmethod
    def setup_class(cls):
        pass

    def test_that_sum_of_items_are_equal_to_the_total_transaction_display(self, pos):
        """
        Test that the sum of items are equal to the total transaction display
        """
        item_to_buy = DisplayItem(name="Item 3", amount=15.00)
        pos.select_item(item_to_buy)
        values_from_transaction_display = pos.transaction.get_values_from_transaction_display()

        assert values_from_transaction_display["total"] == pos.transaction.total_transaction.total
        assert values_from_transaction_display["basket_count"] == pos.transaction.total_transaction.basket_count

    def test_that_applying_a_discount_the_total_transaction_is_equal_to_the_transaction_display(
            self,
            pos,
            manual_discount_factory
    ):
        """
        Test that applying a discount the total transaction is equal to the transaction display
        """
        discount_created = manual_discount_factory()

        # If a transaction is in progress, the discount is not visible and we need to avoid the transaction
        pos.return_to_idle()

        item_to_buy = DisplayItem(name="Item 3", amount=15.00)
        pos.select_item(item_to_buy)
        pos.apply_discount(discount_created)

        values_from_transaction_display = pos.transaction.get_values_from_transaction_display()
        assert values_from_transaction_display["total"] == pos.transaction.total_transaction.total
        assert values_from_transaction_display["basket_count"] == pos.transaction.total_transaction.basket_count

    def test_when_a_payment_has_a_difference_with_the_display_it_has_to_raise_an_exception(self, pos):
        """
        Test that when a payment has a difference with the display it has to raise an exception
        """
        pos.select_item(DisplayItem(name="Item 7", amount=5.00))
        with mock.patch.object(
            target=TransactionDisplay,
            attribute="get_values_from_transaction_display",
            return_value={"total": 99, "basket_count": 3},
        ):
            with pytest.raises(DataInconsistencyException):
                pos.pay()

    @classmethod
    def teardown_class(cls):
        pass
