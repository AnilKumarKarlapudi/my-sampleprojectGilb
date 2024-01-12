import pytest
from unittest import mock

from flaky import flaky

from hornets.components.pos.pos_locators import FunctionKeysLocators, PosMainLocators, SelectionListLocators
from hornets.models.credit_card.instances import VISA_MAGSTRIPE, MagstripeCreditCard
from hornets.models.display_element import DisplayItem


from hornets.components.pos.payment_method import CreditCardPaymentMethod
from hornets.components.pos.pos_state import (
    InTransactionPosState,
    IdlePosState,
    LogoutPosState,
    InTransactionAfterPaymentPosState,
    SelectingDiscountPosState,
)
from hornets.components.pos.selection_list import SelectionList


@pytest.mark.frontend
@flaky(max_runs=5, min_passes=1)
class TestGetToIdlePosState:
    @classmethod
    def setup_class(cls):
        pass

    def test_verify_when_an_item_is_selected_in_transaction_pos_state_is_set(self, pos):
        """
        Test that verifies POS can return to idle from transaction in progress
        """
        item_to_buy = DisplayItem(name="Item 7", amount=5.00)
        pos.select_item(item_to_buy)

        assert isinstance(pos.pos_state, InTransactionPosState)
        assert pos.function_keys.find_element(FunctionKeysLocators.VOID_TRANSACTION)

    def test_return_from_in_transaction_pos_state_to_idle(self, pos):
        """
        Test that verifies POS can return to idle from transaction in progress
        """
        pos.return_to_idle()

        assert isinstance(pos.pos_state, IdlePosState)
        assert pos.function_keys.find_element(FunctionKeysLocators.CLOSE_TILL)

    def test_verify_when_the_user_is_not_logged_in_the_pos_state_should_be_logout_pos_state(self, pos):
        """
        Test that verifies POS state is LogoutPosState when the user is not logged in
        """
        pos.logout()

        assert isinstance(pos.pos_state, LogoutPosState)
        assert pos.function_keys.find_element(FunctionKeysLocators.SIGN_ON)

    def test_logged_in_if_the_pos_state_is_logout_pos_state(self, pos):
        """
        Test that verifies POS can log in from logout state
        """
        pos.return_to_idle()

        assert isinstance(pos.pos_state, IdlePosState)
        assert pos.function_keys.find_element(FunctionKeysLocators.CLOSE_TILL)

    def test_verify_when_the_payment_is_processed_that_the_pos_state_is_in_transaction_after_payment(self, pos):
        """
        Test that verifies POS state is InTransactionAfterPaymentPosState when the payment is processed
        """
        pos.select_item(DisplayItem(name="Item 7", amount=5.00))
        with mock.patch.object(
            target=MagstripeCreditCard, attribute="process_payment", side_effect=Exception("Some custom exception")
        ):
            try:
                pos.pay(CreditCardPaymentMethod(VISA_MAGSTRIPE))
            except Exception:
                assert isinstance(pos.pos_state, InTransactionAfterPaymentPosState)
                assert pos.find_element(PosMainLocators.PINPAD_DISPLAY)

    def test_return_to_idle_when_the_payment_could_not_be_processed(self, pos):
        """
        Test that verifies POS can return to idle from transaction in progress after payment
        """
        pos.return_to_idle()

        assert isinstance(pos.pos_state, IdlePosState)
        assert pos.function_keys.find_element(FunctionKeysLocators.CLOSE_TILL)

    def test_verify_when_the_discount_is_selected_the_pos_state_is_selecting_discount(
            self,
            pos,
            manual_discount_factory
    ):
        """
        Test that verifies POS state is SelectingDiscountPosState when the discount is selected
        """
        discount_created = manual_discount_factory()

        pos.reload()
        pos.return_to_idle()

        pos.select_item(DisplayItem(name="Item 3", amount=15.00))

        with mock.patch.object(
            target=SelectionList, attribute="select_discount", side_effect=Exception("Some custom exception")
        ):
            try:
                pos.apply_discount(discount_created)
            except Exception:
                assert isinstance(pos.pos_state, SelectingDiscountPosState)
                assert pos.selection_list.find_element(
                    SelectionListLocators.KEY_BY_TEXT, additional_attribute=discount_created.name
                )

    def test_return_to_idle_from_selecting_discount(self, pos):
        """
        Test that verifies POS can return to idle from transaction in progress after payment
        """
        pos.return_to_idle()

        assert isinstance(pos.pos_state, IdlePosState)
        assert pos.function_keys.find_element(FunctionKeysLocators.CLOSE_TILL)
