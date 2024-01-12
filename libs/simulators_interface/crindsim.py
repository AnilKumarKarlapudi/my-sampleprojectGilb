from dataclasses import dataclass
from enum import Enum, auto
import logging
import re
import time
from typing import Optional

"""
from app.util.runas import run_sqlcmd
from app.framework import EDH
from app.util import server, constants, runas
from app.framework.tc_helpers import test_func
"""

from hornets.models.credit_card.models import CreditCard
from libs.simulators_interface.basesim import Simulator
from libs.simulators_interface.enums import SimulatorResource, CrindSimMode

# Global Variables:
log = logging.getLogger("crindsim")


class CrindPromptsMethods(Enum):
    SOFTKEY = auto()
    KEYPAD = auto()
    CARWASH = auto()
    MERCH_ITEMS = auto()


@dataclass
class CrindPrompt(object):
    legends: list[str]
    values: list[str]
    method: CrindPromptsMethods


class CrindPrompts(object):

    def __init__(self, debit="no", pin="1234", carwash="no", selection="1", receipt="yes", vehicle_number="1234",
                 id_number="1234", customer_id="1234", customer_code="1234", odometer="1234", driver_id="1234",
                 zip_code="12345", vendor="Vendor", merch_items="", loyalty_prompts=None):
        """
        Initialize prompts required for crind operation

        Args:
            debit: (str) Answer to debit prompt.
            pin: (str) PIN to be entered
            carwash: (str) Answer to carwash prompt
            selection: (str) Answer to carwash package selection prompt
              NOTE: If carwash = "no" leaving this as "1" is ok
            receipt: (str) Answer to receipt prompt
            vehicle_number: (str) Fleet prompt for vehicle number
            id_number: (str) Fleet prompt for ID Number
            customer_id: (str) Fleet prompt for customer ID
            customer_code: (str) Fleet prompt for customer code
            driver_id: (str) Fleet prompt for driver id/ driver number
            odometer: (str) Fleet prompt for odometer
            zip_code: (str) Prompt for zipcode
            vendor: (str) Merch Vendor
            merch_items: (str) Merch item to select
            loyalty_prompts: (dict) Handle custom loyalty prompts e.g. Would You Like to Save today? Yes/No
        """
        self.loyalty_prompts = loyalty_prompts
        self.prompts = [
            CrindPrompt(legends=["vehicle number"], values=[vehicle_number], method=CrindPromptsMethods.KEYPAD),
            CrindPrompt(legends=["id number"], values=[id_number], method=CrindPromptsMethods.KEYPAD),
            CrindPrompt(legends=["customer id"], values=[customer_id], method=CrindPromptsMethods.KEYPAD),
            CrindPrompt(legends=["customer code"], values=[customer_code], method=CrindPromptsMethods.KEYPAD),
            CrindPrompt(legends=["driver"], values=[driver_id], method=CrindPromptsMethods.KEYPAD),
            CrindPrompt(legends=["zip"], values=[zip_code], method=CrindPromptsMethods.KEYPAD),
            CrindPrompt(legends=["odometer reading"], values=[odometer], method=CrindPromptsMethods.KEYPAD),
            CrindPrompt(legends=["debit"], values=[debit], method=CrindPromptsMethods.SOFTKEY),
            CrindPrompt(legends=["pin"], values=[pin], method=CrindPromptsMethods.KEYPAD),
            CrindPrompt(
                legends=["carwash", vendor.lower()],
                values=[carwash, vendor, merch_items, selection],
                method=CrindPromptsMethods.CARWASH
            ),
            CrindPrompt(legends=["non-fuel total"], values=["Done"], method=CrindPromptsMethods.SOFTKEY),
            # carwash alone prompt is different from carwash & vendor prompt
            CrindPrompt(legends=["carwash"], values=[carwash], method=CrindPromptsMethods.SOFTKEY),
            CrindPrompt(legends=["make selection"], values=[selection], method=CrindPromptsMethods.SOFTKEY),
            CrindPrompt(legends=[vendor.lower()], values=[merch_items], method=CrindPromptsMethods.MERCH_ITEMS),
            CrindPrompt(legends=["receipt?"], values=[receipt], method=CrindPromptsMethods.SOFTKEY),
        ]

    def get_prompt_for_display(self, display) -> Optional[CrindPrompt]:
        # Find prompt method
        for prompt in self.prompts:
            # Check if display has all requested substrings
            if all(prompt_part in display for prompt_part in prompt.legends):
                return prompt

        return None


class CrindSim(Simulator):

    def __init__(self, dispenser_id: str, ip: Optional[str] = None):
        """
        Initializes the CrindSim class.
        """
        super().__init__(SimulatorResource.CRIND, ip)
        self.dispenser_id = dispenser_id

    def set_trace_level(self, level):
        log.info(f"Setting trace level to {level}")
        result = self.get(f"/debug/{level}")
        if result['success']:
            return True
        log.warning(f"Received the following Error: {result['payload']}")
        return False

    def close(self):
        """
        Closes the dispenser. This is a TCP/IP disconnect.

        Returns:
            True/False: (bool) True if the dispenser successfully closed. False otherwise.

        Example:
            >> crindsim.close()
                True
            >> crindsim.close(4)
                True
            >> crindsim.close("bananas")
                False
        """
        result = self.get(f"/closedispenser/{self.dispenser_id}")
        if result['success']:
            return True
        log.warning(f"Received the following Error: {result['payload']}")
        return False

    def set_price_format(self, decimals=3):
        """
        Set the price format of the requested dispenser to 2 or 3 decimals.

        Args:
            decimals:   (int)   The number of decimal places you want your price format to have
                                Ex. 3 is $x.xxx while 2 is $xx.xx format
        Returns:
            (bool) True if sim successfully configures the price format. False if not.

        Examples:
            >> crindsim.set_price_format(decimals = 2)
            True - Sets price format to $xx.xx
            >> crindsim.set_price_format(decimals = 3)
            True - Sets price format to $x.xxx
            >> crindsim.set_price_format(decimals = 4)
            False - Only supports 2 or 3 decimals
        """
        if not (decimals == 2 or decimals == 3):
            log.warning(f"Only 2 and 3 decimal price formats are supported.  You requested {decimals} decimals.")
            return False
        else:
            # Endpoint for 2 decimals is 3 while 3 decimals is 4 so increment by 1
            decimals = decimals + 1

        req = f"/dispenser/{self.dispenser_id}/ppuformat/{decimals}"
        result = self.post(req, "")
        if not result['success']:
            log.warning(f"{result['payload']}")
            return False

        return True

    def set_receipt_response(self, auto_response=True, print_receipt=True):
        """
        Automatically respond to a dispensers receipt prompt with Yes/No or use auto_response False to
        retain traditional functionality.

        Args:
            auto_response:  (bool)  True if you would like to automatically respond to receipt prompts on
                                    the dispenser with the provided response arg.
            print_receipt:  (bool)   The response if you want a print receipt.
        Returns:
            (bool) True if sim successfully configures the price format. False if not.

        Examples:
            >> crindsim.set_receipt_response(auto_response=False, dispenser=1)
            True - Disables auto receipt response and restores legacy functionality on dispenser 1.
            >> crindsim.set_receipt_response(auto_response=True, print_receipt=True, dispenser=1)
            True - Enables auto response.  All receipt prompts respond with "Yes" on dispenser 1
            >> crindsim.set_receipt_response(auto_response=True, print_receipt=False, dispenser=1)
            True - Enables auto response.  All receipt prompts respond with "No" on dispenser 1
        """

        response = "Yes" if print_receipt else "No"
        if auto_response:
            req = f"/setprintreceipt/{response}/{self.dispenser_id}"
        else:
            req = f"/unsetprintreceipt/{self.dispenser_id}"
        result = self.get(req)

        if not result['success']:
            log.warning(f"{result['payload']}")
            return False

        return True

    def get_price_format(self):
        """
        Get the price format of the requested dispenser

        Returns:
            (int)   The number of decimals in the current price format. 2 for $xx.xx, 3 for $x.xxx.  0 for failure

        Examples:
            >> crindsim.get_price_format()
            2 - price format is $xx.xx
            >> crindsim.set_price_format()
            3 - price format is $x.xxx
            >> crindsim.set_price_format()
            0 - failed to get request through
        """
        req = f"/dispenser/{self.dispenser_id}/ppuformat"
        result = self.get(req)
        if not result['success']:
            log.warning(f"{result['payload']}")
            return 0
        else:
            decimals_str = result['payload']['message']
            if decimals_str == "ThreeDecimal":
                return 3
            elif decimals_str == "TwoDecimal":
                return 2
            else:
                log.warning(
                    f"Price format returned from crindsim was {decimals_str}, "
                    f"while we expected ThreeDecimal or TwoDecimal."
                )
                return 0

    def close_nozzle(self):
        """
        Closes the nozzle to the selected dispenser.

        Returns:
            True/False: (bool) True if the dispenser's nozzle was successfully closed. False otherwise.

        Examples:
            >> close_nozzle()
                True
            >> close_nozzle(3)
                True
            >> close_nozzle("some text")
                False
        """
        log.info(f"Close nozzle in dispenser #{self.dispenser_id}")
        result = self.get(f"/closenozzle/{self.dispenser_id}")
        if result['success']:
            return True
        log.warning(f"Received the following Error: {result['payload']}")
        return False

    def get_display_text(self):
        """
        Gets the text that is on the dispenser.

        Returns:
            lines: (list) A list of texts split down by the line. The list will be empty if there was any error.

        Examples:
            >> get_display_text()
                ["Pay inside", "or insert card"]
            >> get_display_text(3)
                ["Downloading..."]
            >> get_display_text("bad argument")
                []
        """
        lines = ""
        result = self.get(f"/getdisplay/{self.dispenser_id}")
        if result['success']:
            display_text = result['payload']['message']
        else:
            log.warning(result['payload'])
            return lines
        lines = display_text.replace("\n", " ")
        # log.info(f"The dispenser screen shows {lines}")
        return lines

    def get_pump_status(self):
        """
        Gets the current status of a pump (idle, calling, dispensing, etc.)

        Returns: (str) The status of the pump. Empty string if the pump is not open or an error occurs.

        Examples:
            >> get_pump_status()
            "Idle"
            >> get_pump_status(2)
            "Dispensing"
            >> get_pump_status(25)
            ""
        """
        result = self.get(f"/pumpstatus/{self.dispenser_id}")
        if result['success']:
            return result['payload']['message']
        log.warning(result['payload'])
        return ""

    def get_grade_price(self, grade=1, price_type="credit"):
        """
        Gets the prices of the selected grade at the selected dispenser.
        Note that for blended pumps, pure grades appear as the last grades, i.e. for BLN_3+1 the 1 will be grade 6.

        Args:
            grade: (int) The grade in which the price will be received from
            price_type: (str) The price type for the grade. Only credit and cash are supported

        Returns
            (str) The price of the selected grade. An empty string if there was an error.

        Examples:
            >> get_grade_price()
                "1.000"
            >> get_grade_price(1, dispenser = 2)
                "0.999"
            >> get_grade_price(1, "invalid price type", 3)
                ""
        """
        result = self.get(f"/getgradeprice/{grade}/{price_type}/{self.dispenser_id}")
        if result['success']:
            return result['payload']['message']
        log.warning(result['payload'])
        return ""

    def get_mode(self) -> Optional[CrindSimMode]:
        """
        Gets the mode of the selected dispenser (auto or manual)

        Returns:
            (str) The mode that the selected dispenser is on (auto or manual). An Empty string if there was an error.

        Examples:
            >> get_mode(2)
                "auto"
            >> get_mode()
                "manual"
            >> get_mode("guitar") #There's no dispenser called guitar
                None
        """
        result = self.get(f"/getmode/{self.dispenser_id}")
        if result['success']:
            return CrindSimMode(result['payload']['message'].lower())
        log.warning(result['payload'])

        return None

    def get_receipt(self):
        """
        Gets the most recent receipt printed on the CRIND.

        Returns:
            (str) The string that represents the receipt. Empty string if there was no receipt or if there was an error

        Examples:
            >> get_receipt()
                "\r\nAutomation Island\r\n299\r\n1234 Some Street\r\nFort Lauderdale, FL\r\n33308\r\n
                09/18/2019\r\n01:15:41 PM\r\n \r\nPREPAID RECEIPT\r\n \r\nPUMP# 1\r\nDiesel 1     "\
                "20.020G\r\nPRICE/GAL     $0.999\r\n \r\nFUEL TOTAL  $  20.00\r\n \r\n   FINAL PURCHASE\r\n
                AMOUNT RECEIPT WITH\r\n  FULL TRANSACTION\r\n  DETAIL AVAILABLE\r\n       "\
                    "INSIDE\r\n \r\n
            >> get_receipt(1)
                "\r\nAutomation Island\r\n299\r\n1234 Some Street\r\nFort Lauderdale, FL\r\n33308\r\n09/18/2019\r\n
                01:15:41 PM\r\n \r\nPREPAID RECEIPT\r\n \r\nPUMP# 1\r\nDiesel 1     "\
                "20.020G\r\nPRICE/GAL     $0.999\r\n \r\nFUEL TOTAL  $  20.00\r\n \r\n   FINAL PURCHASE\r\n
                AMOUNT RECEIPT WITH\r\n  FULL TRANSACTION\r\n  DETAIL AVAILABLE\r\n       "\
                    "INSIDE\r\n \r\n"
            >> get_receipt("Not a dispenser")
                ""
        """
        result = self.get(f"/getreceipt/{self.dispenser_id}")
        if result['success']:
            receipt = result['payload']['message']
            log.info(f"The receipt of dispenser #{self.dispenser_id} is {receipt}")
            return receipt
        log.warning(result['payload'])
        return ""

    def get_softkey_text(self):
        """
        Gets the text of each softkey that is available.

        Returns:
            (list) A list of the softkeys that are currently active and the text that they contain.
                   An Empty list if there are no softkeys active or if there was an error.

        Examples:
            >> get_softkey_text()
                [] #This sometimes isn't bad if there are no softkeys with text
            >> get_softkey_text(2)
                ["yes", "no"]
            >> get_softkey_text("Not a dispenser")
                []
        """
        result = self.get(f"/getsoftkeytexts/{self.dispenser_id}")
        if result['success']:
            return result['payload']["message"].split(",")
        # Returning an empty list in case there are no speedkey texts or if there was a failure.
        log.warning(result['payload']["message"])
        return []

    def lift_handle(self):
        """
        Lifts the handle to the selected dispenser.

        Returns:
            True/False: (bool) True if the handle was successfully lifted. False otherwise.

        Examples:
            >> lift_handle()
                True
            >> lift_handle(3)
                True
            >> lift_handle("Not a dispenser")
                False
        """
        log.info(f"Lift the handle on dispenser #{self.dispenser_id}")
        result = self.get(f"/lifthandle/{self.dispenser_id}")
        if result['success']:
            return True
        log.warning(result['payload'])
        return False

    def lower_handle(self):
        """
        Lowers the handle to the selected dispenser.

        Returns:
            True/False: (bool) True if the handle was successfully lowered. False otherwise.

        Examples:
            >> lower_handle()
                True
            >> lower_handle(2)
                True
            >> lower_handle("Not a dispenser")
                False
        """
        log.info(f"Lower the handle on dispenser #{self.dispenser_id}")
        result = self.get(f"/lowerhandle/{self.dispenser_id}")
        if result['success']:
            return True
        log.warning(result['payload'])
        return False

    def open(self):
        """
        Opens the dispenser through a TCP/IP connection.

        Returns:
            True/False: (bool) True if the dispenser was successfully opened. False otherwise.

        Examples:
            >> open()
                True
            >> open(4)
                True
            >> open("Not a dispenser")
                False
        """
        result = self.get(f"/opendispenser/{self.dispenser_id}")
        if result['success']:
            return True
        log.warning(result['payload'])
        return False

    def open_nozzle(self):
        """
        Opens the nozzle of the selected dispenser.

        Returns:
            True/False: (bool) True if the nozzle was successfully opened. False otherwise.

        Examples:
            >> open_nozzle()
                True
            >> open_nozzle(7)
                True
            >> open_nozzle("Not a dispenser")
                False
        """
        log.info(f"Open nozzle on dispenser #{self.dispenser_id}")
        result = self.get(f"/opennozzle/{self.dispenser_id}")
        if result['success']:
            return True
        log.warning(result['payload'])
        return False

    def press_keypad(self, key, validate=False):
        """
        Presses a key on the keypad of the selected dispenser.

        Args:
            key: (str) The key that will be pressed.
            validate: (bool) Verify the requested key press has registered in the keypad display.

        Returns:
            True/False: (bool) True if the keypad key was successfully pressed. False otherwise.

        Examples:
            >> press_keypad("4")
                True
            >> press_keypad("Help", 2)
                True
            >> press_keypad("Not a key")
                False
            >> press_keypad("Cancel", "not a dispenser")
                False
            >> press_keypad("4", validate = True)
                True (4 was successfully entered and read)
            >> press_keypad("4", validate = True)
                False (4 was not visible in the keypad read after entering)
        """
        if validate:
            if not key.isdecimal():
                log.warning("Cannot validate special keys.")
                validate = False
        log.debug(f"Click on keypad {key} on dispenser #{self.dispenser_id}")
        start_read = self.read_keypad_entry()
        result = self.get(f"/presskeypadkey/{key}/{self.dispenser_id}")
        if not result['success']:
            log.warning(result['payload'])
            return False
        if validate:
            end_read = self.read_keypad_entry()
            if start_read == "":
                return end_read == key
            length_diff = len(end_read) - len(start_read)
            if not length_diff == 1:
                return False
            return end_read[len(end_read) - 1] == key
        else:
            return True

    def read_keypad_entry(self):
        """
        Gets the text of keypad.

        Returns:
            (string) A string of the text that has been input from the crindsim.
                   An empty string if there is no input.

        Examples:
            >> read_keypad_entry()
                "12"
            >> read_keypad_entry(2)
                "1234"
            >> read_keypad_entry("Not a dispenser")
                ""
        """

        result = self.get(f"/getkeypadtext/{self.dispenser_id}")
        if result['success']:
            text_input = result['payload']["message"]
            log.debug(f"The text input is: {text_input}")
            return text_input
        # Returning an empty string in case there are no text.
        log.warning(result['payload']["message"])
        return ""

    def press_softkey(self, key):
        """
        Presses a softkey on the dispenser if it exists.

        Args:
            key: (str) The text for the softkey being pressed.

        Returns:
            True/False: (bool) True if the softkey was pressed successfully. False otherwise.

        Examples:
            >> press_softkey("yes")
                True
            >> press_softkey("no", 3)
                True
            >> press_softkey("Not yes")
                False
            >> press_softkey("yes", "Not a dispenser")
                False
        """
        log.debug(f"Click softkey key {key} on dispenser #{self.dispenser_id}")
        result = self.get(f"/presssoftkey/{key}/{self.dispenser_id}")
        if result['success']:
            return True
        log.warning(result['payload'])
        return False

    def select_grade(self, grade=1):
        """
        Selects the grade that will be dispensed.
        Note that for blended pumps, pure grades appear as the last grades, i.e. for BLN_3+1 the 1 will be grade 6.
        Selecting a not configured grade may lead to errors.

        Args:
            grade: (int) The grade number that will be dispensed. (Starts with 1)

        Returns:
            True/False: (bool) True if the grade was successfully selected. False otherwise.

        Examples:
            >> select_grade()
                True
            >> select_grade(2)
                True
            >> select_grade(3, 2)
                True
            >> select_grade(dispenser = 4)
                True
            >> select_grade("not a grade")
                False
            >> select_grade(2, "Not a dispenser")
                False
        """
        log.info(f"Select grade {grade} on dispenser #{self.dispenser_id}")
        response = self.get(f"/selectgrade/{grade}/{self.dispenser_id}")
        if response['success']:
            if response['payload']['message'] == 'false':
                log.warning(f"Could not select grade: {grade}")
            log.debug(f"Successfully selected the grade: {grade}")
            return True
        else:
            log.warning(f"Could not select grade: {grade}")
            return False

    def set_flow_rate(self, rate):
        """
        Sets the flow rate to the selected dispenser. The higher the flow rate, the faster the CRIND will dispense.

        Args:
            rate: (int) The rate in which the fuel will be dispensed. Maximum rate: 10. Minimum rate: 1.

        Returns:
            True/False: (bool) True if the rate was successfully set. False otherwise.

        Examples:
            >> set_flow_rate(5)
                True
            >> set_flow_rate(8, 2)
                True
            >> set_flow_rate("not a flow rate")
                False
            >> set_flow_rate(2, "not a dispenser")
                False
        """
        log.info(f"Set Flow rate {rate} on dispenser #{self.dispenser_id}")

        if type(rate) is str and not rate.isdigit():
            log.warning(f"The rate was {rate} instead of a digit.")
            return False
        results = self.get(f"/setflowrate/{int(rate)}/{self.dispenser_id}")
        if results['success'] and "false" not in results['payload']['message']:
            return True
        log.warning("Could not successfully set the flow rate.")
        return False

    def set_mode(self, mode: CrindSimMode):
        """
        Sets the mode to the dispenser. If auto, the fuel will be dispensed automatically when authorized.

        Args:
            mode: (CrindSimMode) The mode that the dispenser will be set to. Only AUTO and MANUAL are supported.

        Returns:
            True/False: (bool)
                True if the mode was successfully set.
                False if an invalid mode was selected or if there was any other error.

        Examples:
            >> set_mode(CrindSimMode.AUTO)
                True
            >> set_mode(CrindSimMode.MANUAL, 3)
                True
        """

        log.info(f"Set mode {mode.name} for dispenser #{self.dispenser_id}")
        result = self.get(f"/setmode/{mode}/{self.dispenser_id}")

        if not result['success']:
            log.warning(result['payload'])
            return False

        return True

    def set_sales_target(self, sales_type="auth", target="20.00"):
        """
        Sets the sales target of the dispenser.

        Args:
            sales_type: (str) The target type. Can be auth (authorized amount), money (set money amount),
                volume (set volume amount), or random (random money amount)
            target: (str) A string representative of how much the user wants dispensed (money or volume).
                Only works with money or volume types.

        Returns:
            True/False: (bool) True if the sales target was successfully set.
                False if an invalid type was entered or if there was any other error.

        Examples:
            >> set_sales_target()
                True
            >> set_sales_target("money")
                True
            >> set_sales_target("money", "15.00")
                True
            >> set_sales_target("volume", "25.00", 3)
                True
            >> set_sales_target(dispenser = 2)
                True
            >> set_sales_target("cash")
                False
            >> set_sales_target("money", "stuff")
                False
            >> set_sales_target("money", "10.00", "not a dispenser")
                False
        """
        log.info(f"Set dispenser {self.dispenser_id} with sales_type: {sales_type} and target: {target}")
        if sales_type.lower() not in ["auth", "money", "volume", "random"]:
            log.warning(f"{sales_type.lower()} is an invalid sales type. Please choose auth, money, volume, or random")
            return False

        results = self.get(f"/setsalestarget/{sales_type.lower()}/{target}/{self.dispenser_id}")

        if results['success'] and "false" not in results['payload']:
            return True
        if not results['success']:
            log.warning(results['payload'])

        return False

    def swipe_card(self, credit_card: CreditCard):
        """
        Swipes a selected card at the CRIND.

        Args:
            credit_card: (CreditCard) CreditCard object

        Returns:
            True/False: (bool) True if the card was successfully swiped at the CRIND. False if there was any error.

        Examples:
            >> swipe_card(VISA_MAGSTRIPE)
                True
            >> swipe_card(credit_card=VISA_MAGSTRIPE)
                True
            >> swipe_card(VISA_MAGSTRIPE, dispenser=2)
                True
            >> swipe_card(VISA_MAGSTRIPE, dispenser = "not a dispenser")
                False
        """
        log.info(f"Swipe card {credit_card.card_name} for dispenser #{self.dispenser_id}")
        result = self.post(f"/swipecard/{self.dispenser_id}", credit_card.card_data_raw)
        if result['success']:
            return True
        log.warning(f"Receieved the following Error: {result['payload']}")
        return False

    def insert_card(self, credit_card: CreditCard):
        """
        Swipes a selected card at the CRIND.

        Args:
            credit_card: (CreditCard) CreditCard object

        Returns:
            True/False: (bool) True if the card was successfully swiped at the CRIND. False if there was any error.

        Examples:
            >> insert_card(VISA_MAGSTRIPE)
                True
            >> insert_card(credit_card=VISA_MAGSTRIPE)
                True
            >> insert_card(VISA_MAGSTRIPE, dispenser=2)
                True
            >> insert_card(VISA_MAGSTRIPE, dispenser = "not a dispenser")
                False
        """

        # Crind simulator must receive TlvData and RecordTable for EMV cards
        if "TlvData" not in credit_card.card_data_raw or "RecordTable" not in credit_card.card_data_raw:
            log.warning(
                "Card data for EMV card to insert must include TlvData and RecordTable data. Use a different card.")
            return False
        result = self.post(f"/insertCard/{self.dispenser_id}", credit_card.card_data_raw)
        if result['success']:
            return True
        log.warning(f"Receieved the following Error: {result['payload']}")
        return False

    def remove_card(self):
        """
        Remove the currently inserted card at the CRIND. Does nothing if no card is inserted.
        Args:
            dispenser: (int) The number of the dispenser to remove the card from.
        Returns: (bool) True/False for success or failure
        Examples:
            >> remove_card()
            True
            >> remove_card(7)
            True
        """
        result = self.post(f"/removeCard/{self.dispenser_id}", None)
        if result['success']:
            return True
        log.warning(f"Received the following Error: {result['payload']}")
        return False

    def tap_card(self, credit_card: CreditCard):
        """
        Tap a contactless EMV card at the CRIND.
        Args:
            credit_card: (CreditCard) CreditCard object
        Examples:
            >> tap_card()
            True
            >> tap_card(VISA_MAGSTRIPE, dispenser=2)
            True
        """
        if "TlvData" not in credit_card.card_data_raw or "RecordTable" not in credit_card.card_data_raw:
            log.warning(
                "Card data for EMV card to tap must include TlvData and RecordTable data. Use a different card.")
            return False

        result = self.post(f"/tapcard/{self.dispenser_id}", credit_card.card_data_raw)
        if result['success']:
            return True
        log.warning(f"Received the following Error: {result['payload']}")
        return False

    def receipt_prompt_handler(self, receipt_response="Yes", receipt_timeout=30, thanks_timeout=30):
        """
        Wait for the receipt prompt on the crind display text.
        Respond with the answer provided by the receipt_response arg.
        Wait for the "thank you" screen to display on the crind.
        Args:
            receipt_response: (str) Yes/No Response answer for whether you want your receipt printed or not.
            receipt_timeout: (int) Time to wait for the crind's screen to display the prompt for printing the receipt.
            thanks_timeout: (int) Time to wait for the crind's screen to display the "thank you" screen after
            completing the transaction.
        Examples:
            >> receipt_handler("Yes", 20, 30)
            True
            >> receipt_handler("No", 20, 30)
            True
        """
        if not self.wait_for_screen("Do you want a receipt?", timeout=receipt_timeout):
            log.error(f"Failed to see the 'Do you want a receipt' screen within {receipt_timeout} seconds.")
            return False
        if not self.press_softkey(receipt_response):
            log.error(f"Failed to response to the receipt prompt with {receipt_response}")
            return False
        if not self.wait_for_screen("Thank you Please come again", timeout=thanks_timeout):
            log.error(f"Failed to see the thank you screen within {thanks_timeout} seconds.")
            return False
        return True

    def wait_for_screen(self, screen_text, timeout=30):
        start_time = time.time()
        previous_display = None
        # Loop will check the current display. If it is the screen we want, it exits.
        while time.time() - start_time < timeout:
            display = self.get_display_text().lower()
            if screen_text.lower() in display:
                log.debug(f"Found: {screen_text}")
                return True
            if display == previous_display:
                continue
            # Log the new screen if it has changed
            else:
                log.debug(f"Current screen: {display}")
                previous_display = display
        else:
            log.warning(f"Failed to find the screen: {screen_text}")
            return False

    def wait_for_softkey(self, key_text, timeout=10):
        # Clean the key to remove spaces and make it lowercase
        if key_text:
            key_text = key_text.lower()
            key_text = key_text.replace(" ", "")
        else:
            log.warning("Enter a valid key_text argument")
            return False

        start_time = time.time()
        previous_text = None
        # Loop will check the current softkey text displayed. If it is the softkey we want, it exits.
        while time.time() - start_time < timeout:
            softkey_text = self.get_softkey_text()
            for key in softkey_text:
                if key:
                    # Clean the current key to remove spaces and make it lowercase
                    key = key.lower()
                    key = key.replace(" ", "")
                    if key_text in key:
                        log.debug(f"Found: {key_text}")
                        return True
            if softkey_text == previous_text:
                continue
            # Log the new screen if it has changed
            else:
                log.debug(f"Current softkey text: {softkey_text}")
                previous_text = softkey_text
        else:
            log.warning(f"Failed to find the softkey text: {key_text}")
            return False

    def insert_bill(self, value):
        """
        Simulate insertion of a bill to a cash acceptor.
        Args:
            value: (int) The value of the bill to insert. 100 for $1, 500 for $5, etc.
        Returns: (bool)
            True if the request succeeded
            False if not. Note that this does not indicate whether the bill was accepted.
        Examples:
            >> insert_bill(1000)
            True
            >> insert_bill(2000, 3)
            True
        """
        result = self.get(f"/cash/insert/bill/{value}/{self.dispenser_id}")
        time.sleep(3)
        if 'Insert bills, begin fueling' not in self.get_display_text():
            log.warning('Crind cash acceptor is not working properly! Please check the configuration.')
            return False
        elif result['success']:
            return True
        else:
            log.warning(result['payload'])
            return False

    # endregion

    # region Unfinished
    # TODO: Need to see if these are needed.

    def get_money(self):
        raise NotImplementedError

    def get_volume(self):
        raise NotImplementedError

    def get_flow_rate(self):
        raise NotImplementedError

    # endregion

    # region statics

    def outside_sale(
            self,
            credit_card: CreditCard,
            prompts=CrindPrompts(),
            target_type="auth",
            target_amount="10.00",
            grade=1,
            loyalty_card=None,
            timeout=60,
            cash_acceptor=False,
            bill_amount=None
    ):
        """
        Run an outside sale and answers all prompts.
        NOTE: Support for Crind Merch not currently implemented
        NOTE: Add support for amount to dispense (Currently dispenses max)

        Args:
            credit_card: (CreditCard) CreditCard object
            prompts: (CrindPrompts) Prompts object with required values
            target_type: (str) Type to set sales target to (Auth, Money, Volume)
            target_amount: (str) Amount to set sales target to
            grade: (int) Grade to dispense
            loyalty_card: (str) If a card is passed in, it will be used for a loyalty transaction
            timeout: (int) The time given for the transaction to complete.
            cash_acceptor: (bool) enable/disable crind cash acceptor transaction
            bill_amount: (list) The amount of the bills for cash acceptor transaction
        Returns:
            True/False: (bool) True if CRIND sale was successful. False if there was any error.

        Examples:
            >> crind_sale(VISA_MAGSTRIPE)
                True
            >> crind_sale(card_name = "Discover", prompts=CrindPrompts(carwash = "yes", selection = "2"))
                True
            >> crind_sale(card_name="Discover", prompts=CrindPrompts(vendor="Vendor", merch_items="Item 2|$5.00"))
                True
            >> crind_sale("Not a Card")
                False
            >> crind_sale(VISA_MAGSTRIPE, dispenser="not a dispenser")
                False
            >> crind_sale(
                  loyalty_card="Loyalty",
                  prompts=CrindPrompts(
                    loyalty_prompt={'kickback':{'prompt':'Would you like to save today?','answer':'Yes'}}
                  )
               )
                True
            >> crind_sale(cash_acceptor=True, bill_amount=[1000,2000])
                True
        """

        # Set a default value
        if not bill_amount:
            bill_amount = ['1000']

        # Waiting for the dispenser to go Idle, it could take a full minute to do so
        if not self.wait_for_screen("insert", timeout=60):
            log.warning(f"Unable to run the transaction as the Dispenser #{self.dispenser_id} is not IDLE")
            return False

        # Loop that gets current crind display and answers any prompts
        start_time = time.time()
        previous_display = []
        while time.time() - start_time < timeout:
            display = self.get_display_text().lower()
            if display == previous_display:
                # Wait for a new display message
                continue

            log.debug(f"Display: {display}")

            # Get available prompt entering method and values for displayed message
            prompt = prompts.get_prompt_for_display(display)

            # TODO: It should handle loyalty card
            # if loyalty_prompt:
            #     for loyalty in loyalty_prompt:
            #         if loyalty_prompt[loyalty]['prompt'].lower() in display:
            #             self.press_softkey(loyalty_prompt[loyalty]['answer'], dispenser)
            #             log.debug(
            #                 "pressed " + loyalty_prompt[loyalty]['answer'] + " for prompt: " +
            #                 loyalty_prompt[loyalty]['prompt'])
            if "insert" in display:
                # TODO: It should handle cash acceptor
                # if cash_acceptor:
                #     if not self.note_acceptor_status().lower() == 'idle':
                #         log.error("Cash Acceptor is not Idle.")
                #         return False
                #     for bill in bill_amount:
                #         if not self.insert_bill(bill):
                #             log.error("Unable to insert bill.")
                #             return False
                #         time.sleep(1)
                #     log.debug(f"{bill_amount}$ Bill inserted.")
                # elif credit_card.card_data_raw["Type"] == "EMV":
                if credit_card.card_data_raw["Type"] == "EMV":
                    self.insert_card(credit_card)
                    log.debug("inserted " + credit_card.card_name)
                elif credit_card.card_data_raw["Type"] == "Magstripe":
                    # TODO: It should handle loyalty card
                    # if loyalty_card:
                    #     self.swipe_card(card_name=loyalty_card)
                    #     time.sleep(3)
                    #     if not self.wait_for_screen("Pay here Insert card"):
                    #         log.error("Did not see 'pay here insert card' after swiping loyalty")
                    #         return False
                    self.swipe_card(credit_card)
                    log.debug("swiped " + credit_card.card_name)
            elif "please see cashier" in display:
                log.warning("Customer instructed to see cashier")
                return False
            elif "lift handle" in display and self.get_mode() == CrindSimMode.MANUAL:
                self.fuel_manually(grade, target_type, target_amount)
            elif "insert bills, begin fueling" in display and self.get_mode() == CrindSimMode.MANUAL:
                self.fuel_manually(grade, target_type, target_amount)
            elif "remove card" in display:
                self.remove_card()
            elif prompt:
                if prompt.method == CrindPromptsMethods.KEYPAD:
                    value = prompt.values[0]
                    for digit in value:
                        self.press_keypad(digit)
                    self.press_keypad("Enter")
                    log.debug(f"entered {value} for {prompt.legends[0]}")
                elif prompt.method == CrindPromptsMethods.SOFTKEY:
                    value = prompt.values[0]
                    self.press_softkey(value)
                    log.debug(f"pressed {value} for {prompt.legends[0]}")
                elif prompt.method == CrindPromptsMethods.CARWASH:
                    carwash = prompt.values[0]
                    vendor = prompt.values[1]
                    merch_items = prompt.values[2]
                    selection = prompt.values[3]
                    if carwash == "no":
                        if not merch_items:
                            self.wait_for_softkey('don')
                            self.press_softkey("Done")
                        else:
                            self.wait_for_softkey(vendor)
                            self.press_softkey(vendor)
                            self.handle_merchandise_prompts(merch_items)
                            self.wait_for_screen('Make selection Carwash Vendor')
                            self.wait_for_softkey('don')
                            self.press_softkey("Done")
                    elif carwash == "yes":
                        self.press_softkey("Carwash")
                        self.wait_for_softkey(selection, timeout=5)
                        self.press_softkey(selection)
                elif prompt.method == CrindPromptsMethods.MERCH_ITEMS:
                    merch_items = prompt.values[0]
                    if merch_items:
                        self.press_softkey("yes")
                        log.debug("pressed yes for Merchandise Vendor")
                        self.handle_merchandise_prompts(merch_items)
                    else:
                        self.press_softkey("no")
                        log.debug("pressed no for Merchandise Vendor")
            elif "thank you" in display:
                log.debug("Sale complete")
                return True

            previous_display = display

        log.warning("Transaction did not complete before timeout")
        return False

    def handle_merchandise_prompts(self, merch_item):
        self.wait_for_softkey(merch_item, timeout=5)
        self.press_softkey(merch_item)
        log.debug("pressed " + merch_item + " for Merchandise item")
        self.wait_for_screen('Make selection')
        self.wait_for_softkey('don')
        self.press_softkey("Done")

    # TODO: this function should be here?
    #  Maybe it belongs to another module with the responsibility of doing high level operations
    def fuel_manually(self, grade=1, target_type="auth", amount="10.00", dispense_time=5):
        """
        Used to dispense fuel for a crindsim that is set to manual mode
        NOTE: Support for Zip, Crind Merch not currently implemented
        NOTE: Add support for amount to dispense (Currently dispenses max)

        Args:
            target_type: (str) Type to set sales target to (Auth, Money, Volume)
            amount: (str) Amount to set sales target to
            grade: (int) Grade to dispense
            dispense_time: (int) Amount of time you would like to allow the crindsim to dispense fuel
        Returns:
            True/False: (bool) True if fuel was dispensed. False if there was any error.

        Examples:
            >> fuel_manually()
                True
            >> fuel_manually(grade = 2)
                True
            >> fuel_manually(target_type="money", target_amount="20.00")
                True
        """
        if target_type == "auth":
            self.set_sales_target("auth")
        else:
            self.set_sales_target(target_type, amount)
        self.select_grade(grade)
        self.lift_handle()
        self.open_nozzle()
        time.sleep(dispense_time)
        self.lower_handle()
        return True

    def get_logs(self):
        log.debug("Getting Crindsim Logs")
        action = '/getLogs'
        result = self.get(action)
        return result['payload']

    # endregion

    def check_receipt_for(self, values):
        if type(values) is not list:
            values = [values]

        lines_not_found = []
        string_rcpt = self.get_receipt()
        actual_rcpt = re.split('\r\n', string_rcpt)

        if not actual_rcpt:
            log.warning("The receipt we returned was blank. Attempting to parse it again")
            string_rcpt = self.get_receipt()
            actual_rcpt = re.split('\r\n', string_rcpt)
            if not actual_rcpt:
                log.error("The receipt we returned was blank again.")
                return False
        ret = True
        for value in values:
            value = value.replace(' ', '')
            # List comprehension to search every line of the receipt while ignoring whitespace
            if not any([value in line.replace(' ', '') for line in actual_rcpt]):
                lines_not_found.append(value)
                log.debug("Did not find %s in the receipt." % value)
                ret = False
        return ret

    # TODO: this function should be here?
    #  Maybe it belongs to another module with the responsibility of doing high level operations
    # def fuel_prepay(self, dispense_time=5, timeout=20):
    #     """
    #     Used to dispense fuel for a prepay fuel sale
    #
    #     Args:
    #         dispenser:      (int) The number of the dispenser that the card will be swiping at.
    #         dispense_time:  (int) Amount of time you would like to allow the crindsim to dispense fuel
    #
    #     Returns:
    #         True/False: (bool) True if fuel was dispensed. False if there was any error.
    #     """
    #     log.info("Handling fueling of prepay transaction")
    #     # Loop that gets current crind display and answers any prompts
    #     start_time = time.time()
    #     previous_display = []
    #     while time.time() - start_time < timeout:
    #         display = self.get_display_text().lower()
    #         if not display == previous_display:
    #             log.debug(display)
    #         if "lift handle" in display:
    #             log.info("Attempting to dispense fuel.")
    #             self.lift_handle()
    #             self.open_nozzle()
    #             time.sleep(dispense_time)
    #             self.lower_handle()
    #             self.close_nozzle()
    #         elif "receipt?" in display:
    #             log.debug("pressing no for receipt")
    #             self.press_softkey("no", self.dispenser_id)
    #         elif "thank you" in display:
    #             log.info("Sale complete")
    #             previous_display = display
    #             while time.time() - start_time < 10:
    #                 end_display = self.get_display_text().lower()
    #                 if not end_display == previous_display:
    #                     log.debug(end_display)
    #                 if "insert card" in display:
    #                     log.debug("Transaction has completed")
    #                     return True
    #             else:
    #                 log.warning("Dispenser did not return to idle within the timeout")
    #                 return False
    #         previous_display = display
    #     log.warning("Transaction did not complete before timeout")
    #     return False

    # TODO: setting up EDH belongs to this module?
    # @staticmethod
    # def setup_edh(num_dispensers, ip="10.80.31.210"):
    #     """
    #     Sets up the needed registry keys for the EDH to accept the CRIND Sim
    #     Args:
    #         num_dispensers: (int) The number of dispensers to setup
    #         ip: (str) The IP address where the CRIND Sim is running. Default value: 10.80.31.210
    #     Returns:
    #         None
    #     Example:
    #         >> setup_edh(4)
    #     """
    #     log.info(f"Using the ip: {ip} to set the CRINDs")
    #     crindsim_root = r'HKLM\%s\Debug\TWOIPIPTest' % (constants.CRIND_SUBKEY)
    #     status = True
    #     tls_type = r'reg add HKLM\%s /v TWOIPIPConnection /t REG_SZ /d TLSNoAuth /f' \
    #                % (constants.SECURE_SUBKEY)
    #     if "The operation completed successfully." in str(run_sqlcmd(tls_type)):
    #         log.info("tls_type added successfully")
    #     else:
    #         log.info("tls_type not added successfully")
    #         status = False
    #
    #     key_4 = r'reg add %s\4 /f' % (crindsim_root)
    #     if "The operation completed successfully." in str(run_sqlcmd(key_4)):
    #         log.info("key_4 added successfully")
    #     else:
    #         log.info("key_4 not added successfully")
    #         status = False
    #
    #     key_5 = r'reg add %s\5 /f' % (crindsim_root)
    #     if "The operation completed successfully." in str(run_sqlcmd(key_5)):
    #         log.info("key_5 added successfully")
    #     else:
    #         log.info("key_5 not added successfully")
    #         status = False
    #
    #     for i in range(int(num_dispensers)):
    #         string_4 = r'reg add %s\4 /v %s /t REG_SZ /d default /f' \
    #                    % (crindsim_root, str(i + 1))
    #         if "The operation completed successfully." in str(run_sqlcmd(string_4)):
    #             log.info("string_4 added successfully")
    #         else:
    #             log.info("string_4 not added successfully")
    #             status = False
    #     IP = r'reg add %s\4 /v defaultip /t REG_SZ /d %s /f' \
    #          % (crindsim_root, ip)
    #     if "The operation completed successfully." in str(run_sqlcmd(IP)):
    #         log.info("IP added successfully")
    #     else:
    #         log.info("IP not added successfully")
    #         status = False
    #     Port = r'reg add %s\4 /v defaultport /t REG_DWORD /d 0x000012c0 /f' \
    #            % (crindsim_root)
    #     if "The operation completed successfully." in str(run_sqlcmd(Port)):
    #         log.info("Port added successfully")
    #     else:
    #         log.info("Port not added successfully")
    #         status = False
    #     edh = EDH.EDH()
    #     log.info("EDH  initialization successful")
    #     if edh.restart():
    #         log.info("restart successful")
    #     else:
    #         log.info("EDH restart not successful")
    #         status = False
    #     checkService = "sc \\\\passporteps query edh"
    #     timeout = time.time() + 30
    #     while time.time() < timeout:
    #         if "running" in str(run_sqlcmd(checkService)).lower():
    #             log.debug("Confirmed EDH is online")
    #             status = True
    #             break
    #         else:
    #             log.debug("EDH is not online yet")
    #             status = False
    #         time.sleep(1)
    #     return status

    # TODO: Should this function reset EDH? CrindSim should manage EDH? Maybe it should be a caller responsibility
    # def set_pump_type(self, pump_type, blend_ratios=None, restart_edh=True):
    #     """
    #     Set the pump type and blend ratios (if applicable) for the selected dispenser.
    #     Restarts the EDH, so it will pick up the new configuration.
    #
    #     Args:
    #         pump_type: (str) The pump type to set - MULTI_3, BLN_4, etc.
    #         blend_ratios: (list) The low product percentage for each blended grade, if there are any.
    #         restart_edh: (bool) Whether to restart the EDH after setting the pump type. This is required for the pump
    #             to come up,so only set it False if you're setting multiple pumps at once and don't want to restart
    #             repeatedly.
    #     Returns:
    #         (bool) True if sim successfully configures the pump. False if not.
    #
    #     Examples:
    #         >> crindsim.set_pump_type("MULTI_3")
    #         True
    #         >> crindsim.set_pump_type("BLN_3+1", [100, 50, 0])
    #         True
    #         >> crindsim.set_pump_type("BLN_4", [100, 50, 0])
    #         False
    #     """
    #     if not blend_ratios:
    #         blend_ratios = []
    #     pump_type = pump_type.replace('+', '_').upper()
    #     if blend_ratios:
    #         ratios_str = ",".join([str(r) for r in blend_ratios])
    #         req = f"/setpumptype/{pump_type}/{ratios_str}/{self.dispenser_id}"
    #     else:
    #         req = f"/setpumptype/{pump_type}/{self.dispenser_id}"
    #     result = self.get(req)
    #     if not result['success']:
    #         log.warning(f"{result['payload']}")
    #         return False
    #     elif restart_edh:
    #         EDH.EDH().restart()  # EDH may not pick up on the config change without a restart
    #
    #     return True

    # TODO: this function should be here?
    #  Maybe it belongs to another module with the responsibility of doing high level operations
    # def commercial(
    #         self,
    #         card_name="NGFC",
    #         brand="Exxon",
    #         selection="tractor",
    #         need_def="no",
    #         tractor_grade=1,
    #         tractor_target_type="auth",
    #         tractor_target_amount="10.00",
    #         reefer_grade=1,
    #         reefer_target_type="auth",
    #         reefer_target_amount="10.00",
    #         def_grade=3,
    #         def_target_type="auth",
    #         def_target_amount="10.00",
    #         receipt="yes",
    #         additional_product="no",
    #         timeout=60
    # ):
    #     """
    #     Run a commercial fuel sale at the crind and answers all prompts.
    #
    #     Args:
    #         card_name: (str) The name of the card being used.
    #           NOTE: Please refer to app/data/CardData.json for card names and bins.
    #         brand: (str) The brand of the store. NOTE: Different stores have different bin ranges.
    #         selection: (str) Type of fuel to purchase (Tractor, Reefer, Both)
    #         need_def: (str) Answer to the Need DEF? prompt
    #         tractor_grade: (int) Grade to dispense for Tractor
    #         tractor_target_type: (str) Type to send to set_sale_target for Tractor (Auth, Money, Volume)
    #         tractor_target_amount: (str) Amount to set sales target to for Tractor
    #         reefer_grade: (int) Grade to dispense for Tractor
    #         reefer_target_type: (str) Type to send to set_sale_target for Reefer (Auth, Money, Volume)
    #         reefer_target_amount: (str) Amount to set sales target to for Reefer
    #         def_grade: (int) Grade to dispense for Tractor
    #         def_target_type: (str) Type to send to set_sale_target for DEF (Auth, Money, Volume)
    #         def_target_amount: (str) Amount to set sales target to for DEF
    #         receipt: (str) Answer to receipt prompt
    #         additional_product: (str) Answer to additional product prompt
    #         timeout: (int) The time given for the transaction to complete.
    #     Returns:
    #         True/False: (bool)
    #           True if CRIND sale was successful.
    #           False if there was any error or if the customer was told to go inside.
    #
    #     Examples:
    #         >> commercial_sale()
    #             True
    #         >> commercial_sale("Mastercard")
    #             True
    #         >> commercial_sale(selection = "Reefer", need_def = "yes")
    #             True
    #         >> commercial_sale("Not a Card")
    #             False
    #         >> commercial_sale("VisaFleet", "Not a brand")
    #             False
    #         >> commercial_sale("MCFleet", dispenser = "not a dispenser")
    #             False
    #     """
    #
    #     # set crindsim mode to manual as auto mode will not allow grades to be changed for commercial fueling
    #     self.set_mode(CrindSimMode.MANUAL)
    #     # Waiting for the dispenser to go Idle
    #     if not self.wait_for_screen("insert card"):
    #         log.warning(f"Unable to run the transaction as the Dispenser #{self.dispenser_id}is not IDLE")
    #         return False
    #
    #     # Loop that gets current crind display and answers any prompts
    #     start_time = time.time()
    #     previous_display = []
    #     while time.time() - start_time < timeout:
    #         display = self.get_display_text().lower()
    #         if not display == previous_display:
    #             log.debug(display)
    #         if "insert card" in display:
    #             self.swipe_card(card_name, brand)
    #             log.debug("swiped " + card_name)
    #         elif "please see cashier" in display:
    #             log.warning("Customer instructed to see cashier")
    #             return False
    #         elif "make selection" in display:
    #             self.press_softkey(selection)
    #             log.debug(selection + " selected")
    #         elif "need def?" in display:
    #             self.press_softkey(need_def)
    #             log.debug(need_def + " entered for Need DEF?")
    #         elif "additional products" in display:
    #             self.press_softkey(additional_product)
    #             log.debug(additional_product + " selected for Additional Products?")
    #         elif "ready to fuel tractor" in display:
    #             self.fuel_manually(tractor_grade, tractor_target_type, tractor_target_amount)
    #         elif "ready to fuel def" in display:
    #             self.fuel_manually(def_grade, def_target_type, def_target_amount)
    #         elif "ready to fuel reefer" in display:
    #             self.fuel_manually(reefer_grade, reefer_target_type, reefer_target_amount)
    #         elif "receipt?" in display:
    #             self.press_softkey(receipt)
    #             log.debug("pressed " + receipt + " for receipt")
    #         elif "thank you" in display:
    #             log.debug("sale complete")
    #             return True
    #         previous_display = display
    #
    #         time.sleep(1)
    #     log.warning("Transaction did not complete before timeout")
    #     return False

    # TODO: think if this function belongs to this class
    # def note_acceptor_status(self):
    #     """
    #     Get the status of a dispenser's note acceptor.
    #     Possible values include Idle, BillInEscrow, BillStackedIntoCassette, BillReturned, BillRejected,
    #     ActivityDetected, CommunicationsLost.
    #     Args:
    #         dispenser: (int) The dispenser to get the note acceptor status for.
    #     Returns: (str) The status of the note acceptor.
    #     Examples:
    #         >> note_acceptor_status()
    #         'Idle'
    #         >> note_acceptor_status(2)
    #         'BillStackedIntoCassette'
    #     """
    #     if not int(runas.run_sqlquery("select BillAcceptorEnabled from CrindUnit where crindid = 1")['rows'][0][0]):
    #         log.warning("Crind cash acceptor is not connected with crind.")
    #         return "offline"
    #
    #     if not int(
    #             runas.run_sqlquery("select BillAcceptorInstalled from G_Fuel_Dispenser where DispenserID = 1")
    #               ['rows'][0][0]):
    #         log.warning("Crind cash acceptor is not enabled on MWS Forecourt Installation.")
    #         return "offline"
    #
    #     result = self.get(f"/cash/status/{self.dispenser_id}")
    #
    #     if result['success'] and "false" not in result['payload']:
    #         return result['payload']['message']
    #     if not result['success']:
    #         log.warning(result['payload'])
