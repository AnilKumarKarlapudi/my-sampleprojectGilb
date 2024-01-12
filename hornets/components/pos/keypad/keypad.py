from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.utilities.log_config import logger
from hornets.base_enum import BaseEnum
from hornets.components.pos.pos_section import PosSection


class Keypad(PosSection):

    def __init__(self, driver: WebDriver, keypad, enter_button: BaseEnum):
        super().__init__(driver)
        self.keypad = keypad
        self.enter_button = enter_button
        self._char_mapping = CHAR_MAPPING

    def enter_value(self, value: str):
        """
        Enter a value in the keypad
        Args:
            value (str): Value to enter
        """
        for char in value:
            char_name = self._get_char_name(char)
            self.click(self.keypad[char_name])
        self.click(self.enter_button)

    def _get_char_name(self, char: str):
        """
        Given a character returns their respective name in NumberKeypadLocators or KeyboardKeypadLocators enums
        Args:
            char (str): Character to translate
        Returns:
            str: String that represents the name of that character within the enums.
        """
        try:
            return self._char_mapping[char]
        except KeyError:
            logger.error(f"No enum name found with value '{char}'")


CHAR_MAPPING = {
    "1": "ONE",
    "2": "TWO",
    "3": "THREE",
    "4": "FOUR",
    "5": "FIVE",
    "6": "SIX",
    "7": "SEVEN",
    "8": "EIGHT",
    "9": "NINE",
    "0": "ZERO",
    "00": "DOUBLE_ZERO",
    "@": "AT",
    "+": "PLUS",
    "-": "MINUS",
    "#": "HASH",
    "$": "DOLLAR",
    "%": "PERCENT",
    "^": "CARET",
    "&": "AMPERSAND",
    "*": "ASTERISK",
    "(": "OPEN_PAREN",
    ")": "CLOSE_PAREN",
    "q": "Q",
    "w": "W",
    "e": "E",
    "r": "R",
    "t": "T",
    "y": "Y",
    "u": "U",
    "i": "I",
    "o": "O",
    "p": "P",
    "a": "A",
    "s": "S",
    "d": "D",
    "f": "F",
    "g": "G",
    "h": "H",
    "j": "J",
    "k": "K",
    "l": "L",
    "\\": "BACKSLASH",
    "z": "Z",
    "x": "X",
    "c": "C",
    "v": "V",
    "b": "B",
    "n": "N",
    "m": "M",
    "/": "SLASH",
    ":": "COLON",
    ".": "PERIOD",
    ",": "COMMA",
    " ": "SPACE",
}
