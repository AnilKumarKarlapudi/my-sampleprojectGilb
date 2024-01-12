from selenium.common import TimeoutException as SeleniumTimeoutException
from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.components.mws.pages.pos_page import PosMwsPage
from hornets.components.exceptions import NotApplicableDiscountException, DataInconsistencyException
from hornets.components.pos.forecourt.forecourt import Forecourt
from hornets.components.pos.function_keys import FunctionKeys
from hornets.components.pos.pos_locators import FunctionKeysLocators, PosMainLocators, PromptBoxLocators, \
    NumberKeypadLocators
from hornets.components.pos.header.header import Header
from hornets.components.pos.speedkeys_display import SpeedKeysDisplay
from hornets.components.pos.keypad.keyboard_keypad import KeyboardKeypad
from hornets.components.pos.keypad.number_keypad import NumberKeyPad
from hornets.components.pos.payment_method import CashPaymentMethod, PaymentMethod
from hornets.components.pos.pos_state import (
    UnknownPosState,
    IdlePosState,
    InTransactionPosState,
    PosState,
    LogoutPosState,
    InTransactionAfterPaymentPosState,
    SelectingDiscountPosState
)
from hornets.components.pos.prompt_box import PromptBox
from hornets.components.pos.selection_list import SelectionList
from hornets.components.pos.transaction.transaction_display import TransactionDisplay
from hornets.models.credit_card.models import CreditCard
from hornets.models.display_element import DisplayItem
from hornets.models.manual_discount.models import ManualDiscount
from libs.simulators_interface.pinpadsim import PinPad
from hornets.utilities.log_config import logger
from hornets.utilities.constants import CREDENTIALS


class Pos(PosMwsPage):
    def __init__(self, driver: WebDriver, return_to_idle: bool = True):
        super().__init__(driver)
        self.printer_installed = False
        self.number_keypad = NumberKeyPad(self.driver)
        self.keyboard = KeyboardKeypad(self.driver)
        self.speedkeys_display = SpeedKeysDisplay(self.driver)
        self.function_keys = FunctionKeys(self.driver)
        self.transaction = TransactionDisplay(self.driver)
        self.prompt_box = PromptBox(self.driver)
        self.selection_list = SelectionList(self.driver)
        self.forecourt = Forecourt(self.driver)
        self.pinpad_sim = PinPad()
        self.header = Header(self.driver)
        self.pos_state = UnknownPosState()  # TODO: pos_state should be a value given by TinyDB
        self._reset_transaction_values()
        if return_to_idle:
            self.return_to_idle()

    def return_to_idle(self):
        """
        Return to the idle state
        """
        self.pos_state.return_to_idle(self)

    def reload(self):
        """
        Reload the POS
        """
        self.header.reload()

    def get_status_information(self):
        """
        Get the status information from the header
        Return:
            StatusInformation: Status information page
        """
        return self.header.get_status_information()

    def get_pos_state(self) -> PosState:
        """
        Get the current state of the POS
        Return:
            PosState: Current state of the POS
        """
        logger.info("Getting POS state")
        if self.function_keys.find_element(FunctionKeysLocators.CLOSE_TILL):
            return IdlePosState()
        if self.function_keys.find_element(FunctionKeysLocators.VOID_TRANSACTION):
            return InTransactionPosState()
        if self.function_keys.find_element(FunctionKeysLocators.SIGN_ON):
            return LogoutPosState()
        if self.find_element(PosMainLocators.PINPAD_DISPLAY):
            return InTransactionAfterPaymentPosState()

    def logged_in(self):
        """
        Check if the user is logged in, if not, log in
        """
        logger.info("User is not logged in")
        self.connect()
        self._set_idle_pos_state()

    def logout(self):
        """
        Check if the user is logged in, if so, log out
        """
        logger.info("Logging out")
        self.function_keys.click(FunctionKeysLocators.SIGN_OFF)
        self.prompt_box.click(PromptBoxLocators.YES)
        self.pos_state = LogoutPosState()

    def connect(self):
        """
        Connect to the POS
        """
        logger.info("Connecting to POS")
        self.function_keys.click(FunctionKeysLocators.SIGN_ON)
        self.number_keypad.enter_value(CREDENTIALS["username"])
        self.keyboard.enter_value(CREDENTIALS["password"])

    def select_item(self, item: DisplayItem):
        """
        Select an item from the items keypad
        """
        self.speedkeys_display.select_item(item)
        self.transaction.add_item(item)
        self.pos_state = InTransactionPosState()

    def apply_discount(self, discount: ManualDiscount):
        """
        Apply a discount to the transaction or the item
        Raise:
            NotApplicableDiscountException: If the discount is not applicable
        """
        try:
            self.function_keys.click(FunctionKeysLocators.DISCOUNT)
            self.pos_state = SelectingDiscountPosState()
            self.selection_list.select_discount(discount.name)
            self.number_keypad.click(NumberKeypadLocators.ENTER)
            self.transaction.add_discount(discount)
        except SeleniumTimeoutException:
            raise NotApplicableDiscountException

    def pay(self, payment_method: PaymentMethod = None) -> dict:
        """
        Pay the transaction with the given payment method
        Return:
            dict: Transaction completed
        """
        self._validate_data_consistency()
        payment_method = payment_method or CashPaymentMethod()
        payment_method.pay_with(self)
        self._wait_for_transaction_to_be_completed()
        transaction_completed = self.transaction.to_dict(payment_method=payment_method)
        self._reset_transaction_values()
        self._set_idle_pos_state()
        return transaction_completed

    def cancel_transaction(self):
        """
        Press Cancel in the payment screen during a transaction
        """
        self.number_keypad.click(NumberKeypadLocators.CANCEL)

    def void_transaction(self):
        """
        Void the transaction
        """
        logger.info("Voiding transaction")
        self.function_keys.click(FunctionKeysLocators.VOID_TRANSACTION)
        self.number_keypad.click(NumberKeypadLocators.ENTER)
        self._set_idle_pos_state()
        self._reset_transaction_values()

    def accept_that_the_cashier_will_not_open(self):
        """
        Accept that the cashier will not open
        """
        self.prompt_box.click(PromptBoxLocators.OK)

    def select_dispenser(self, dispenser_id):
        """
        Select a dispenser
        Args:
            dispenser_id (str): Dispenser ID
        """
        self.forecourt.select_dispenser(dispenser_id)

    def stop_all_dispensers(self):
        """
        Stop all the dispensers
        """
        self.forecourt.stop_all_dispensers()

    def start_all_dispensers(self):
        """
        Start all the dispensers
        """
        self.forecourt.start_all_dispensers()

    def _process_payment_with_cash(self):
        """
        Process the payment with cash
        """
        self.function_keys.pay_with_cash()
        if not self.printer_installed:
            self.accept_that_the_cashier_will_not_open()

    def _process_payment_with_credit_card(self, credit_card: CreditCard):
        """
        Process the payment with a credit card
        Args:
            credit_card (CreditCard): Credit card to use
        """
        self.function_keys.pay_with_credit_card()
        self.pos_state = InTransactionAfterPaymentPosState()
        credit_card.process_payment(self)

    def _wait_for_transaction_to_be_completed(self):
        """
        Wait for the transaction to be completed
        """
        self.transaction.wait_for_transaction_to_be_completed()

    def _process_payment_with_magstripe_credit_card(self, credit_card: CreditCard):
        """
        Process the payment with a magstripe credit card
        Args:
            credit_card (CreditCard): Credit card to use
        """
        self.pinpad_sim.swipe_card(credit_card)

    def _process_payment_with_emv_credit_card(self, credit_card: CreditCard):
        """
        Process the payment with an EMV credit card
        Args:
            credit_card (CreditCard): Credit card to use
        """
        self.pinpad_sim.insert_card(credit_card)

    def _process_payment_with_contactless_credit_card(self, credit_card: CreditCard):
        """
        Process the payment with a contactless credit card
        Args:
            credit_card (CreditCard): Credit card to use
        """
        self.pinpad_sim.tap_card(credit_card)

    def _verify_that_the_pinpad_is_working(self):
        """
        Verify that the pinpad is working
        Return:
            bool: True if the pinpad is working, False otherwise
        """
        return self.prompt_box.find_element(PromptBoxLocators.OK)

    def _set_idle_pos_state(self):
        """
        Set the POS state to idle
        """
        self.pos_state = IdlePosState()

    def _validate_data_consistency(self):
        """
        Validate that the data from the transaction display is consistent with the transaction calculated
        Raise:
            DataInconsistencyException: If the data is not consistent
        """
        if self.transaction.get_values_from_transaction_display() != self.transaction.to_dict()["total_transaction"]:
            logger.exception(
                f"The transaction display is getting the next values: "
                f"{self.transaction.get_values_from_transaction_display()} and the transaction calculated is: "
                f"{self.transaction.to_dict()['total_transaction']}"
            )
            raise DataInconsistencyException()

    def _reset_transaction_values(self):
        """
        Reset the transaction values
        """
        self.transaction = TransactionDisplay(self.driver)

    def _cancel_transaction_after_payment(self):
        """
        Cancel the transaction after the payment
        """
        if self._verify_that_the_pinpad_is_working():
            self.prompt_box.click(PromptBoxLocators.OK)
            self.number_keypad.click(NumberKeypadLocators.CANCEL)
        else:
            self.number_keypad.click(NumberKeypadLocators.CANCEL)
            self.prompt_box.click(PromptBoxLocators.OK)
            self.number_keypad.click(NumberKeypadLocators.CANCEL)

    def _cancel_transaction_when_the_discount_is_selected(self):
        """
        Cancel the transaction when the discount is selected
        """
        self.number_keypad.click(NumberKeypadLocators.CANCEL)
