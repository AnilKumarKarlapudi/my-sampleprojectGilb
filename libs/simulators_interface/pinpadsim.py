import logging
import time
from typing import Optional


from hornets.models.credit_card.models import CreditCard
from libs.simulators_interface.basesim import Simulator
from libs.simulators_interface.enums import SimulatorResource, PinpadSimMode

log = logging.getLogger("pinpadsim")

# Disable logging for HTTP Requests
selenium_logger = logging.getLogger("selenium.webdriver.remote.remote_connection")
selenium_logger.propagate = False
urllib_logger = logging.getLogger("urllib3.connectionpool")
urllib_logger.propagate = False
requests_logger = logging.getLogger("requests")
requests_logger.propagate = False


class PinPad(Simulator):
    def __init__(self, ip: Optional[str] = None, pinpad_mode: PinpadSimMode = PinpadSimMode.MANUAL):
        """
        Initializes the PinPad class.
        """
        super().__init__(SimulatorResource.PINPAD, ip)
        self.running_mode(mode=pinpad_mode)
        self.pinpad_mode = pinpad_mode

    def insert_card(
        self, credit_card: CreditCard, debit_fee=False, cashback_amount=None, zip_code=None, cvn=None, custom=None
    ):
        """
        Sends a POST request to the PIN Pad Simulator that will simulate inserting a card with the
        card name you passed in.
        Args:
            credit_card: (CreditCard) CreditCard object
            debit_fee : (bool) If Debit Fee is prompted and set to True, we click OK; otherwise, we click No.
            cashback_amount: (str) The cashback amount you wish to enter
            zip_code : (str) The ZIP code value you wish to enter
            cvn      : (str) The CVN value you wish to enter
            custom : (str) The Custom prompt value you wish to enter
        Returns:
            dict: Dictionary containing a success message and a payload of the data you sent.
        Examples:
            > insert_card(
                credit_card=VISA_MAGSTRIPE,
                debit_fee=True,
                cashback_amount='10.00'
            )
        """
        status = self._validate_to_proceed()
        if status == "success":
            action = "/insert"

            try:
                # Arguments given by scripter that will be sent in POST request.
                if debit_fee is not None:
                    credit_card.card_data_raw["DebitFee"] = debit_fee
                if cashback_amount is not None:
                    credit_card.card_data_raw["CashBackAmount"] = cashback_amount
                if zip_code is not None:
                    credit_card.card_data_raw["ZipCode"] = zip_code
                if custom is not None:
                    credit_card.card_data_raw["Custom"] = custom
                if cvn is not None:
                    credit_card.card_data_raw["CVN"] = cvn

                # Keys in JSON file that will be sent in the POST request.
                if "VehicleID" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["VehicleID"] = None
                if "Odometer" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["Odometer"] = None
                if "DriverID" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["DriverID"] = None
                if "Fuel" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["Fuel"] = None
                if "EmployeeID" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["EmployeeID"] = None
                if "AID" not in credit_card.card_data_raw:  # This should always be in the card - should have error.
                    credit_card.card_data_raw["AID"] = None
                if "CVM" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["CVM"] = None
                status = self.post(action, credit_card.card_data_raw)
                status = status["payload"]["message"].lower()
            except Exception as e:
                log.warning(e)
        return status

    def tap_card(
        self, credit_card: CreditCard, debit_fee=False, cashback_amount=None, zip_code=None, cvn=None, custom=None
    ):
        """
        Sends a POST request to the PIN Pad Simulator that will simulate tapping a contactless card with the
        card name you passed in.
        Args:
            credit_card: (CreditCard) CreditCard object
            debit_fee : (bool) If Debit Fee is prompted and set to True, we click OK; otherwise, we click No.
            cashback_amount: (str) The cashback amount you wish to enter
            zip_code : (str) The ZIP code value you wish to enter
            cvn      : (str) The CVN value you wish to enter
            custom : (str) The Custom prompt value you wish to enter
        Returns:
            dict: Dictionary containing a success message and a payload of the data you sent.
        Examples:
            > tap_card(
                credit_card=VISA_CONTACTLESS,
                debit_fee=True,
                cashback_amount='10.00'
            )
        """
        status = self._validate_to_proceed()
        if status == "success":
            action = "/msdTap"
            try:
                # Arguments given by scripter that will be sent in POST request.
                if debit_fee is not None:
                    credit_card.card_data_raw["DebitFee"] = debit_fee
                if cashback_amount is not None:
                    credit_card.card_data_raw["CashBackAmount"] = cashback_amount
                if zip_code is not None:
                    credit_card.card_data_raw["ZipCode"] = zip_code
                if custom is not None:
                    credit_card.card_data_raw["Custom"] = custom
                if cvn is not None:
                    credit_card.card_data_raw["CVN"] = cvn

                # Keys in JSON file that will be sent in the POST request.
                if "VehicleID" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["VehicleID"] = None
                if "Odometer" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["Odometer"] = None
                if "DriverID" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["DriverID"] = None
                if "Fuel" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["Fuel"] = None
                if "EmployeeID" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["EmployeeID"] = None
                if "AID" not in credit_card.card_data_raw:  # This should always be in the card - should have error.
                    credit_card.card_data_raw["AID"] = None
                if "CVM" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["CVM"] = None
                status = self.post(action, credit_card.card_data_raw)
                status = status["payload"]["message"].lower()
            except Exception as e:
                log.warning(e)
        return status

    def _validate_to_proceed(self):
        """
        Maximum 3 attempts to check the pinpad status before swipe and returns the payload message as status
        Args: None
        Returns: status (string)
        """
        status = "check"
        max_attempts = 5
        current_step = 0
        while current_step < max_attempts and status not in "success":
            current_step = current_step + 1
            status = self.check_before_swipe().lower()
            if status not in "success":
                time.sleep(5)
        return status

    def check_before_swipe(self):
        """
        Get the status of the pinpad either to proceed the swipe/insert/tap the card transaction or not
        Args: None
        Returns: Result of the payload message(string)
        """
        action = "/check_pinpad_status"
        card_data = "{check: 'status'}"
        result = self.post(action, card_data)
        log.warning(f"check_pinpad_status [{result}]")
        return result["payload"]

    def get_pinpad_current_status(self):
        """
        Get the current status of pinpad
        Args: None
        Returns: Result of the payload message(string)
        """
        action = "/current_pinpad_state"
        card_data = "{check: 'status'}"
        result = self.post(action, card_data)
        log.info(f"get_pinpad_status [{result}]")
        return result["payload"]

    @staticmethod
    def wait_for_text(text, timeout=30):
        log.warning("Function not implemented on pinpad sim.  Only applicable to pinpad robot.")
        return True

    def swipe_card(
        self, credit_card: CreditCard, debit_fee=False, cashback_amount=None, zip_code=None, cvn=None, custom=None
    ):
        """
        Sends a POST request to the PIN Pad Simulator that will simulate swiping a card with the
        card name you passed in.
        Args:
            credit_card: (CreditCard) CreditCard object
            debit_fee : (bool) If Debit Fee is prompted and set to True, we click OK; otherwise, we click No.
            cashback_amount: (str) The cashback amount you wish to enter
            zip_code : (str) The ZIP code value you wish to enter
            cvn      : (str) The CVN value you wish to enter
            custom : (str) The Custom prompt value you wish to enter
        Returns:
            dict: Dictionary containing a success message and a payload of the data you sent.
        Examples:
            > swipe_card(
                credit_card=VISA_MAGSTRIPE,
                debit_fee=True,
                cashback_amount='10.00'
            )
        """
        status = self._validate_to_proceed()
        log.warning(f"self._validate_to_proceed() :: [{status}]")
        if status == "success":
            action = "/swipe"
            try:
                # Arguments given by scripter that will be sent in POST request.
                if debit_fee is not None:
                    credit_card.card_data_raw["DebitFee"] = debit_fee
                if cashback_amount is not None:
                    credit_card.card_data_raw["CashBackAmount"] = cashback_amount
                if zip_code is not None:
                    credit_card.card_data_raw["ZipCode"] = zip_code
                if custom is not None:
                    credit_card.card_data_raw["Custom"] = custom
                if cvn is not None:
                    credit_card.card_data_raw["CVN"] = cvn

                # Keys in JSON file that will be sent in the POST request.
                if "VehicleID" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["VehicleID"] = None
                if "Odometer" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["Odometer"] = None
                if "DriverID" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["DriverID"] = None
                if "Fuel" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["Fuel"] = None
                if "EmployeeID" not in credit_card.card_data_raw:
                    credit_card.card_data_raw["EmployeeID"] = None
                status = self.post(action, credit_card.card_data_raw)
                status = status["payload"]["message"].lower()
            except Exception as e:
                log.warning(e)
        return status

    # TODO: Refactor with the new structure (CreditCard object has card_data_raw)
    # def manual_entry(self, credit_card: CreditCard, zip_code=None, custom=None):
    #     """
    #     Sends a POST request to the PIN Pad Simulator that will simulate manual entering the
    #     card name you passed in.
    #     Args:
    #         credit_card: (CreditCard) CreditCard object
    #         zip_code : (str) The ZIP code value you wish to enter
    #         custom : (str) The Custom prompt value you wish to enter
    #     Returns:
    #         dict: Dictionary containing a success message and a payload of the data you sent.
    #     Examples:
    #         > manual_entry(
    #             brand='Generic',
    #             card_name='GiftCard'
    #         )
    #         > manual_entry(
    #             brand='Core',
    #             card_name='Discover'
    #         )
    #     """
    #     action = '/manual_entry'
    #     log.debug(f"Checking {constants.CARD_DATA_MANUAL} for {credit_card.card_name}")
    #     card_data = {}
    #     with open(constants.CARD_DATA_MANUAL, 'r') as fp:
    #         card_data_file = json.load(fp)
    #         try:
    #             card_data = card_data_file[passport.get_brand()][credit_card.card_name]
    #         except Exception:
    #             log.warning(f"Unable to find {credit_card.card_name} within {constants.CARD_DATA_MANUAL}.")
    #     if not card_data:
    #         log.debug(f"Checking {constants.CARD_DATA} for {credit_card.card_name}")
    #         card_data = self._get_card_data(credit_card.card_brand, credit_card.card_name)
    #
    #     try:
    #         # Arguments given by scripter that will be sent in POST request.
    #         card_data['ZipCode'] = zip_code
    #         card_data['Custom'] = custom
    #
    #         # Keys in JSON file that will be sent in the POST request.
    #         if 'VehicleID' not in card_data:
    #             card_data['VehicleID'] = None
    #         if 'Odometer' not in card_data:
    #             card_data['Odometer'] = None
    #         if 'DriverID' not in card_data:
    #             card_data['DriverID'] = None
    #         if 'Fuel' not in card_data:
    #             card_data['Fuel'] = None
    #         if 'EmployeeID' not in card_data:
    #             card_data['EmployeeID'] = None
    #         status = self.post(action, card_data)
    #         status = status['payload']['message'].lower()
    #     except Exception as e:
    #         log.warning(e)
    #     return status

    def swipe_loyalty(self, credit_card: CreditCard):
        """
        Sends a POST request to the PIN Pad Simulator that will simulate swiping a loyalty card with the
        card name you passed in.
        Args:
            credit_card: (CreditCard) CreditCard object
        Examples:
            > swipe_loyalty(
                credit_card=VISA_LOYALTY
            )
        """
        action = "/swipe_loyalty"
        return self.post(action, credit_card.card_data_raw)

    def running_mode(self, mode=PinpadSimMode.AUTO):
        """
        Sends a POST request to set the running mode of the PIN Pad Simulator.
        Args:
            mode: (PinpadSimMode) The mode you wish to set the PIN Pad Simulator to.
        Examples:
            > running_mode(
                mode=PinpadSimMode.AUTO
            )
        """
        action = "/postResponse"
        data = {"message": f"{mode.value},RUNNING_MODE"}
        return self.post(action, data)

    def add_donation(self, selection=1):
        """
        Send a GET request to the PINPad simulator that will add the donation option to the transaction.
        It works for other selections.
        Args:
            selection   : (str) Which of the four options to choose donation amount (1 - 4).
        Examples:
            >> add_donation("1")
        """
        action = f"/selection/{selection}"
        result = self.get(action)
        return result["payload"]["message"].lower()

    def press_cancel(self):
        """
        Send a GET request to the PINPad simulator that will press the cancel button.
        Args:
        Examples:
            >> press_cancel()
                "Success"
        """
        action = "/presscancel"
        result = self.get(action)
        return result["payload"]["message"].lower()

    def reboot(self):
        log.debug("Rebooting pinpad sim")
        action = "/reboot"
        result = self.get(action)
        log.debug(f"Reboot: [{result}]")
        return result["payload"]

    def set_trace_level(self, level):
        log.debug(f"Setting trace level to {level}")
        action = f"/debug?level={level}"
        result = self.get(action)
        log.debug(f"Set trace level: [{result}]")
        return result["payload"]

    def reset(self):
        log.debug("Resetting pinpad simulator and clearing queued up contents")
        action = "/reset"
        result = self.get(action)
        log.warning(f"Reset: [{result}]")
        time.sleep(1)
        return result

    def get_health_check(self):
        """
        Get the connection and transaction status of the pinpad
        Args: None
        Returns: Result of the payload message(string)
        """
        action = "/gethealthcheck"
        result = self.get(action)
        log.debug(f"get_health_check [{result}]")
        return result["payload"]

    def get_logs(self):
        log.debug("Getting Pinpad Logs")
        action = "/getLogs"
        result = self.get(action)
        return result["payload"]
