from hornets.base_enum import BaseEnum


class PosMainLocators(BaseEnum):
    PINPAD_DISPLAY = "//div[@class='pinpad']"


class SpeedKeysDisplayLocators(BaseEnum):
    KEY_BY_TEXT = "//div[@id='speedkeys_container']//div[text()='{}']/.."


class SelectionListLocators(BaseEnum):
    KEY_BY_TEXT = "//div[@id='selection_list_container']//div[text()='{}']/.."


class PromptBoxLocators(BaseEnum):
    HEADER = "//span[@id='prompt_box_heading']"
    BODY = "//div[@id='prompt_box_text']"
    BUTTON = "//*[@id='prompt_box_buttons']/span/button"
    KEY_BY_TEXT = ("//button[starts-with(@class, 'functionkey_button') and translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz') = '%s']")
    KEY_1 = "(//div[@id='prompt_box_buttons']//button[starts-with(@class, 'functionkey_button')])[1]"
    KEY_2 = "(//div[@id='prompt_box_buttons']//button[starts-with(@class, 'functionkey_button')])[2]"
    KEY_3 = "(//div[@id='prompt_box_buttons']//button[starts-with(@class, 'functionkey_button')])[3]"
    CLOSE = "//span[@class='close_button glyphicons glyphicons-remove']"
    YES = "//*[@id='prompt_box_buttons']/span[1]/button"
    NO = "//*[@id='prompt_box_buttons']/span[2]/button"
    OK = "//*[@id='prompt_box_buttons']/span/button"


class FunctionKeysLocators(BaseEnum):
    PAY = "//*[@data-autoid='FKey_15']"
    VOID_TRANSACTION = "//*[@data-autoid='FKey_1']"
    DISCOUNT = "//*[@data-autoid='FKey_45']"
    EXACT_AMOUNT = "//div[starts-with(@class, 'preset_amount exact')]/button"
    CREDIT_CARD = "//div[@id='tenderkeys_container']//span[text()='Card']/.."
    CLOSE_TILL = "//*[@data-autoid='FKey_32']"
    SIGN_ON = "//*[@data-autoid='FKey_136']"
    SIGN_OFF = "//*[@data-autoid='FKey_24']"


class WatermarkDispayLocators(BaseEnum):
    TRANSACTION_COMPLETED = "//*[@id='transaction_complete_watermark']/p"
    TRANSACTION_VOIDED = "//*[@id='transaction_void_watermark']/p"


class TransactionDisplayLocators(BaseEnum):
    ITEMS = "//div[@id='receipt_items']//div[@id='receipt_line']"
    DISCOUNT = "//div[@class='receipt_item_disc']"
    BASKET_COUNT = "//div[@id='basket_count']"
    TOTAL_AMOUNT = "//div[@id='total_amount']"


class NumberKeypadLocators(BaseEnum):
    DISPLAY = "//p[starts-with(@class, 'display_text')]"
    ONE = "//button[starts-with(@class, 'keypad_button') and @tag='1']"
    TWO = "//button[starts-with(@class, 'keypad_button') and @tag='2']"
    THREE = "//button[starts-with(@class, 'keypad_button') and @tag='3']"
    FOUR = "//button[starts-with(@class, 'keypad_button') and @tag='4']"
    FIVE = "//button[starts-with(@class, 'keypad_button') and @tag='5']"
    SIX = "//button[starts-with(@class, 'keypad_button') and @tag='6']"
    SEVEN = "//button[starts-with(@class, 'keypad_button') and @tag='7']"
    EIGHT = "//button[starts-with(@class, 'keypad_button') and @tag='8']"
    NINE = "//button[starts-with(@class, 'keypad_button') and @tag='9']"
    ZERO = "//button[starts-with(@class, 'keypad_button') and @tag='0']"
    DOUBLE_ZERO = "//button[starts-with(@class, 'keypad_button') and @tag='00']"
    AT = "//button[starts-with(@class, 'keypad_button') and @tag='at']"
    FOR = "//button[starts-with(@class, 'keypad_button') and @tag='for']"
    PLUS = "//button[starts-with(@class, 'keypad_button') and @tag='plus']"
    MINUS = "//button[starts-with(@class, 'keypad_button') and @tag='minus']"
    ITEM = "//button[starts-with(@class, 'keypad_button') and @tag='item']"
    TRANSACTION = "//button[starts-with(@class, 'keypad_button') and @tag='trans']"
    REST_IN_FUEL = "//button[starts-with(@class, 'keypad_button') and @tag='restInFuel']"
    CANCEL = "//button[starts-with(@class, 'keypad_button') and @tag='cancel']"
    CLEAR = "//button[starts-with(@class, 'keypad_button') and @tag='clear']"
    ENTER = "//button[starts-with(@class, 'keypad_button') and @tag='enter']"
    FINALIZE = "//button[starts-with(@class, 'keypad_button') and @tag='enter']"
    PLU = "//button[starts-with(@class, 'keypad_button') and @tag='enter']"
    MANUAL = "//button[starts-with(@class, 'keypad_button') and @tag='manual']"


class KeyboardKeypadLocators(BaseEnum):
    HEADING = "//div[@id='alphaprompt_box_heading']"
    PROMPT = "//div[@id='alphaprompt_box_text']"
    ENTRY = "//span[@id='alphaprompt_input']"
    EXCLAMATION = "//button[@tag='!']"
    AT = "//button[@tag='@']"
    HASH = "//button[@tag='#']"
    DOLLAR = "//button[@tag='$']"
    PERCENT = "//button[@tag='%']"
    CARET = "//button[@tag='^']"
    AMPERSAND = "//button[@tag='&']"
    ASTERISK = "//button[@tag='*']"
    OPEN_PAREN = "//button[@tag='(']"
    CLOSE_PAREN = "//button[@tag=')']"
    Q = "//button[@id='keyboard_Q']"
    W = "//button[@id='keyboard_W']"
    E = "//button[@id='keyboard_E']"
    R = "//button[@id='keyboard_R']",
    T = "//button[@id='keyboard_T']"
    Y = "//button[@id='keyboard_Y']"
    U = "//button[@id='keyboard_U']"
    I = "//button[@id='keyboard_I']"
    O = "//button[@id='keyboard_O']"
    P = "//button[@id='keyboard_P']"
    A = "//button[@id='keyboard_A']"
    S = "//button[@id='keyboard_S']"
    D = "//button[@id='keyboard_D']"
    F = "//button[@id='keyboard_F']"
    G = "//button[@id='keyboard_G']"
    H = "//button[@id='keyboard_H']"
    J = "//button[@id='keyboard_J']"
    K = "//button[@id='keyboard_K']"
    L = "//button[@id='keyboard_L']"
    BACKSLASH = "//button[@tag='\\']"
    Z = "//button[@id='keyboard_Z']"
    X = "//button[@id='keyboard_X']"
    C = "//button[@id='keyboard_C']"
    V = "//button[@id='keyboard_V']"
    B = "//button[@id='keyboard_B']"
    N = "//button[@id='keyboard_N']"
    M = "//button[@id='keyboard_M']"
    SLASH = "//button[@tag='/']"
    COLON = "//button[@tag=':']"
    PERIOD = "//button[@tag='.']"
    COMMA = "//button[@tag=',']"
    SPACE = "//button[@tag=' ']"
    SPACE_ALT = "//button[@tag=' ']"
    SHIFT = "//button[@tag='shift']"
    ONE = "//div[@id='numpad']//button[@tag='1']"
    TWO = "//div[@id='numpad']//button[@tag='2']"
    THREE = "//div[@id='numpad']//button[@tag='3']"
    FOUR = "//div[@id='numpad']//button[@tag='4']"
    FIVE = "//div[@id='numpad']//button[@tag='5']"
    SIX = "//div[@id='numpad']//button[@tag='6']"
    SEVEN = "//div[@id='numpad']//button[@tag='7']"
    EIGHT = "//div[@id='numpad']//button[@tag='8']"
    NINE = "//div[@id='numpad']//button[@tag='9']"
    ZERO = "//div[@id='numpad']//button[@tag='0']"
    BACK = "//button[@tag='back']"
    CLEAR = "//button[@id='keyboard_clear']"
    CANCEL = "//button[@id='keyboard_cancel']"
    OK = "//button[@id='keyboard_ok']"


class StatusInformationLocators(BaseEnum):
    DEVICE_STATUS = "//table[@class='peripheral_status_information_screen_table' and caption='Device Status']"
    STATUS_INFORMATION = "//table[@class='status_information_screen_table' and caption='Status Information']"
    BACK = "//button[@data-autoid='FKey_Cancel']"


class HeaderLocators(BaseEnum):
    RELOAD = "//button[@id='reload_button']"
    INFORMATION_BUTTON = "//button[@id='information_button']"


class ForecourtLocators(BaseEnum):
    FORECOURT_DISPLAY = "//*[@class='dispenser_buffers_parent']"
    DISPENSER = "(//div[starts-with(@class, 'dispenser_buffers_parent')])[{}]"
    ALL_STOP = "//div[@id='dispenser_stop']"
    CLEAR_ALL_STOP = "//div[@id='dispenser_stop']//button[text()='Clear All Stop']"
    YES = "//button[@class='functionkey_button' and text()='Yes']"
    NO = "//button[@class='functionkey_button' and text()='No']"


class DispenserLocators(BaseEnum):
    DISPENSER_STATUS = "//div[starts-with(@class, 'dispenserdetailstatusbox')]/div"
    BACK = "//*[starts-with(@class, 'functionkey_container')][.//span[text()='Back']]"
