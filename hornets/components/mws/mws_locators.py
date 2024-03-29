from hornets.base_enum import BaseEnum


class DiscountsMwsPageLocators(BaseEnum):
    HEADER = "//h1[@class='page-header-fixed-title' and contains(text(), 'Discounts')]"
    SEARCH_DISCOUNTS = "//input[@autoid[contains(.,'search') and contains(.,'textbox')]]"
    DISCOUNT_NAME_SEARCH_RESULT = "//span[@title='{}']"
    ADD = "//button[@autoid='addbutton']"
    DISCOUNT_NAME = "//input[@autoid[contains(.,'discountName')]]"
    DISCOUNT_AMOUNT = "//div[@autoid[contains(.,'VariableDiscountSelectBar')]]"
    APPLY_DISCOUNT_TO = "//div[@autoid[contains(.,'TransactionDiscountSelectBar')]]"
    DISCOUNT_TYPE = "//div[@autoid[contains(.,'DiscountMethod')]]"
    AMOUNT = "//input[@autoid[contains(.,'DiscountValue')]]"
    SAVE = "//span[@class[contains(.,'application-button')] and contains(text(), 'Save')]"
    DELETE = "//tr[*//span[text()='{}']]//button[@autoid[contains(.,'delete')]]"
    POPUP_YES_DELETE = "//span[text()='Yes, delete']"


class LoginMwsPageLocators(BaseEnum):
    USERNAME = "//input[@name='Username']"
    LOGIN_ERROR_MESSAGE = ("//div[contains(@class, 'rz-growl-item-container') and contains(@class, "
                           "'rz-state-highlight') and contains(@class, 'rz-growl-message-error')]")
    PASSWORD = "//input[@name='Password']"
    SIGN_ON = "//button[@type='submit']"


class PdlDownloadMwsPageLocators(BaseEnum):
    HEADER = "//*[@id='rz-dialog-0-label' and contains(text(), 'PDL Download')]"
    YES = "//span[@class='rz-button-text' and text()='Yes']"
    NO = "//span[@class='rz-button-text' and text()='No']"
    SUCCEEDED_MESSAGE = "//div[@class='rz-dialog-content']//p[contains(text(), 'Download succeeded. Card Table Load successful')]"
    OK = "//span[@class='rz-button-text' and text()='Ok']"


class PosMwsPageLocators(BaseEnum):
    POS_HEADER = "//p[starts-with(@class, 'header_info_text')]"


class LoyaltyMwsPageLocators(BaseEnum):
    HEADER = "//h1[@class='page-header-fixed-title' and contains(text(), 'Loyalty Configuration')]"


class SiteConfigurationLocators(BaseEnum):
    HEADER = "//h1[@class='page-header-fixed-title' and contains(text(), 'Global Network Parameters')]"
    SAVE_BUTTON = "//span[@class='application-button-text']"
    SAVE_SUCCESS_MESSAGE = "//div[contains(@class,'rz-notification-message')]//p[text()='Saved']"

    # Global Information
    GLOBAL_INFORMATION_TAB = "//div[normalize-space()='Global Information']"
    MERCHANT_NUMBER_INPUT = "//div[normalize-space()='Merchant Number']/following-sibling::div/input[contains(@class,'rz-textbox')]"
    STATION_NAME_INPUT = "//label[text()='Station Name']/parent::div/following-sibling::div/input"
    STATION_ADDRESS_INPUT = "//label[text()='Station Address']/parent::div/following-sibling::div/input"
    STATION_CITY_INPUT = "//label[text()='Station City']/parent::div/following-sibling::div/input"
    STATION_STATE_INPUT = "//label[text()='Station State']/parent::div/following-sibling::div/input"
    STATION_ZIP_CODE_INPUT = "//label[text()='Station Zip Code']/parent::div/following-sibling::div/input"
    HOST_CONNECTION_TYPE_DROP_DOWN = "//label[text()='Host Connection Type']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"
    SVC_ACTIVATION_RECHARGE_GRANULARITY_INPUT = "//label[text()='SVC Activation Recharge Granularity']/parent::div/following-sibling::div//input"
    SVC_ACTIVATION_RECHARGE_MINIMUM_INPUT = "//label[text()='SVC Activation Recharge Minimum']/parent::div/following-sibling::div//input"
    SVC_ACTIVATION_RECHARGE_MAXIMUM_INPUT = "//label[text()='SVC Activation Recharge Maximum']/parent::div/following-sibling::div//input"
    DEBIT_CASH_BACK_GRANULARITY_INPUT = "//label[text()='Debit Cash Back Granularity']/parent::div/following-sibling::div//input"
    DEBIT_CASH_BACK_MINIMUM_INPUT = "//label[text()='Debit Cash Back Minimum']/parent::div/following-sibling::div//input"
    DEBIT_CASH_BACK_MAXIMUM_INPUT = "//label[text()='Debit Cash Back Maximum']/parent::div/following-sibling::div//input"
    EBT_CASH_BACK_GRANULARITY = "//label[text()='EBT Cash Back Granularity']/parent::div/following-sibling::div//input"
    EBT_CASH_BACK_MINIMUM_INPUT = "//label[text()='EBT Cash Back Minimum']/parent::div/following-sibling::div//input"
    EBT_CASH_BACK_MAXIMUM_INPUT = "//label[text()='EBT Cash Back Maximum']/parent::div/following-sibling::div//input"
    DEBIT_CASH_BACK_FEE_INPUT = "//label[text()='Debit Cash Back Fee']/parent::div/following-sibling::div//input"
    DEBIT_SALE_FEE_INPUT = "//label[text()='Debit Sale Fee']/parent::div/following-sibling::div//input"
    DAYS_TO_KEEP_NETWORK_DATA_INPUT = "//label[text()='Days To Keep Network Data']/parent::div/following-sibling::div//input"
    AVS_ENABLED_BY_HOST_DROP_DOWN = "//label[text()='AVS Enabled By Host']/parent::div/following-sibling::div/input"
    PRINT_STORE_COPY_OF_THE_RECEIPT_INSIDE_DROP_DOWN = "//label[text()='Print store copy of the receipt inside']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"
    PRINT_CUSTOMER_COPY_OF_THE_RECEIPT_INSIDE_DROP_DOWN = "//label[text()='Print customer copy of the receipt inside']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"
    POINT_TO_POINT_ENCRYPTION_P2PE_DROP_DOWN = "//label[text()='Point to point encryption (P2PE)']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"
    TAVE_DOMAIN_INPUT = "//label[text()='TAVE Domain']/parent::div/following-sibling::div//input"
    TAVE_PROCESSOR_CODE_INPUT = "//label[text()='TAVE Processor Code']/parent::div/following-sibling::div//input"
    TAVE_TOKEN_ID_INPUT = "//label[text()='TAVE Token Type ID']/parent::div/following-sibling::div//input"

    # Network Connection Options
    NETWORK_CONECTION_OPTIONS_TAB = "//div[normalize-space()='Network Connection Options']"
    COM_PORT = "//label[text()='Com Port']/parent::div/following-sibling::div//input"
    BAUD_RATE_DROP_DOWN = "//label[text()='Baud Rate']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"
    ACCESS_CODE = "//label[text()='Access Code']/parent::div/following-sibling::div/input"
    DOWNLOAD_PHONE_NUMBER = "//label[text()='Download Phone Number']/parent::div/following-sibling::div/input"
    PRIMARY_PHONE_NUMBER = "//label[text()='Primary Phone Number']/parent::div/following-sibling::div/input"
    SECONDARY_PHONE_NUMBER = "//label[text()='Secondary Phone Number']/parent::div/following-sibling::div/input"
    INIT_STRING = "//label[text()='Init String']/parent::div/following-sibling::div/input"
    DIAL_HEADER = "//label[text()='Dial Header']/parent::div/following-sibling::div/input"
    DIAL_TRAILER = "//label[text()='Dial Trailer']/parent::div/following-sibling::div/input"
    DTMF_SPEED_DROP_DOWN = "//label[text()='DTMF Speed']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"
    CONNECTION_TIMER = "//label[text()='Connection Timer']/parent::div/following-sibling::div//input"
    HOST_IP_ADDRESS = "//label[text()='Host IP Address']/parent::div/following-sibling::div/input"
    IP_PORT = "//label[text()='IP Port']/parent::div/following-sibling::div//input"
    KEEP_ALIVE_TIME_FRAME_MINUTES = "//label[text()='Keep Alive time frame (minutes)']/parent::div/following-sibling::div//input"
    DATAWIRE_REGISTRATION_URL = "//label[text()='Datawire Registration URL']/parent::div/following-sibling::div/input"

    # Store & Forward Parameters
    STORE_FORWARD_PARAMETERS_TAB = "//div[normalize-space()='Store & Forward Parameters']"
    STORE_FORWARD_WARNING_COUNT_PERCENT = "//label[text()='Store & Forward Warning Count Percent']/parent::div/following-sibling::div//input"
    STORE_FORWARD_WARNING_TOTAL_PERCENT = "//label[text()='Store & Forward Warning Total Percent']/parent::div/following-sibling::div//input"
    MAXIMUM_STORE_FORWARD_COUNT = "//label[text()='Maximum Store & Forward Count']/parent::div/following-sibling::div//input"
    MAXIMUM_STORE_FORWARD_TOTAL = "//label[text()='Maximum Store & Forward Total']/parent::div/following-sibling::div//input"
    SHOW_STORE_FORWARD_INDICATOR = "//div[@autoid='switch']"
    CLOSE_PASSWORD = "//label[text()='Close Password']/parent::div/following-sibling::div//input"

    # Global EMV Parameters
    GLOBAL_EMV_PARAMETERS_TAB = "//div[normalize-space()='Global EMV Parameters']"
    PREFER_US_COMMON_DEBIT = "//label[text()='Prefer US Common Debit']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"
    EMV_FALLBACK_ALLOWED_INSIDE = "//label[text()='EMV Fallback Allowed Inside']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"
    EMV_FALLBACK_ALLOWED_OUTSIDE = "//label[text()='EMV Fallback Allowed Outside']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"

    # Card Based EMV Parameters
    CARD_BASED_EMV_PARAMETERS_TAB = "//div[normalize-space()='Card Based EMV Parameters']"
    CARD_TYPE = "//ul[@class='rz-listbox-list']"
    ALLOW_PIN_BYPASS_INSIDE = "//label[text()='Allow PIN Bypass Inside']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"
    ALLOW_PIN_BYPASS_OUTSIDE = "//label[text()='Allow PIN Bypass Outside']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"
    ALLOW_FALLBACK_INSIDE = "//label[text()='Allow Fallback Inside']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"
    ALLOW_FALLBACK_OUTSIDE = "//label[text()='Allow Fallback Outside']/parent::div/following-sibling::div/div[@class[contains(., 'rz-dropdown ')]]"


class ItemsMwsPageLocators(BaseEnum):
    # Search Item Screen
    HEADER = "//h1[@class='page-header-fixed-title' and contains(text(), 'Items')]"
    ADD = "//button[@autoid='addbutton']"
    EDIT = "//button[@autoid='item{}editbutton']"
    SAVE = "//a[@autoid='savebutton']"
    ITEM_ADDED_TOAST = "//div[@class='rz-growl-item']//p[text()='Items Added']"
    BACK = "//a[@autoid='backbutton']"
    SEARCH_BUTTON = "//button[@autoid='searchbutton']"
    SEARCH_INPUT = "//input[@autoid='searchtextbox']"
    PLU_RADIO_BUTTON = "//label[text()='PLU/UPC']//preceding-sibling::div"
    DESCRIPTION_RADIO_BUTTON = "//label[text()='Description']//preceding-sibling::div"
    SCANCODE_RADIO_BUTTON = "//label[text()='Scan Code']//preceding-sibling::div"
    RECEIPTDESCRIPTION_RADIO_BUTTON = "//label[text()='Receipt Description']//preceding-sibling::div"
    DEPARTMENT_DROPDOWN = "//label[text()='Department']//parent::div//following-sibling::div//div[@class[contains(.,'dropdown-trigger')]]"
    TYPE_DROPDOWN = "//label[text()='Item Type']//parent::div//following-sibling::div//div[@class[contains(.,'dropdown-trigger')]]"
    DROPDOWN_OPTION = "//li[@aria-label='{}']"
    RESULTS_TABLE = "//table/tbody/tr"
    RESULTS_ROWS = "//tr[contains(@class, 'rz-data-row')]"
    # Add Item Section Titles
    SECTION_TITLE = "//div[@autoid='title' and contains(text(), '{}')]"
    # Add Item Screen - General
    PLU_INPUT = "//input[@autoid='plumask']"
    DESCRIPTION_INPUT = "//input[@autoid='descriptiontextbox']"
    DEPARTMENT_INPUT = "//label[@autoid='departmentlabel']//parent::div//following-sibling::div//div[@class[contains(.,'dropdown-trigger')]]"
    ITEM_TYPE_INPUT = "//label[@autoid='itemtypelabel']//parent::div//following-sibling::div//div[@class[contains(.,'dropdown-trigger')]]"
    RECEIPT_DESCRIPTION_INPUT = "//input[@autoid='receiptdesctextbox']"
    PRICE_REQUIRED_SWITCH = "//div[@autoid='pricerequiredswitch']"
    NORMAL_PRICE_RADIO = "//input[@autoid='normalradio']"
    NORMAL_PRICE_INPUT = "//label[@autoid='normallabel']//following-sibling::span//input"
    BASE_PLUS_ONE_RADIO = "//input[@autoid='baseplusoneradio']"
    BASE_PLUS_ONE_DEALQUANTITY_INPUT = "//span[@autoid='baseplusonequantitynumeric']//input"
    BASE_PLUS_ONE_UNITPRICE_INPUT = "//span[@autoid='baseplusoneunitpricenumeric']//input"
    GROUP_THRESHOLD_RADIO = "//input[@autoid='groupthresholdradio']"
    GROUP_THRESHOLD_UNITPRICE_INPUT = "//span[@autoid='groupthresholdunitpricenumeric']//input"
    GROUP_THRESHOLD_DEALQUANTITY_INPUT = "//span[@autoid='groupthresholdquantitynumeric']//input"
    GROUP_THRESHOLD_DEALPRICE_INPUT = "//span[@autoid='groupthresholddealpricenumeric']//input"
    BULK_RADIO = "//input[@autoid='bulkradio']"
    BULK_DEALQUANTITY_INPUT = "//span[@autoid='bulkquantitynumeric']//input"
    BULK_DEALPRICE_INPUT = "//span[@autoid='bulkpricenumeric']//input"
    UNIT_ADJUSTED_RADIO = "//input[@autoid='unitadjustedradio']"
    UNIT_ADJUSTED_UNITPRICE_INPUT = "//span[@autoid='unitadjustedunitpricenumeric']//input"
    UNIT_ADJUSTED_DEALQUANTITY_INPUT = "//span[@autoid='unitadjustedquantitynumeric']//input"
    UNIT_ADJUSTED_DEALPRICE_INPUT = "//span[@autoid='unitadjusteddealpricenumeric']//input"
    # Add Item Screen - Options
    ACTIVE_FOR_SALE = "//div[@autoid='activeforsaleswitch']"
    FOOD_STAMPABLE = "//div[@autoid='foodstampableswitch']"
    DISCOUNTABLE = "//div[@autoid='discountableswitch']"
    FEE = "//div[@autoid='feeswitch']"
    ALLOW_REFUNDS = "//div[@autoid='allowrefundsswitch']"
    QUANTITY_ALLOWED = "//div[@autoid='quantityallowedswitch']"
    QUANTITY_REQUIRED = "//div[@autoid='quantityrequiredswitch']"
    FRACTIONAL_QUANTITY_ALLOWED = "//div[@autoid='allowfractionalquantityswitch']"
    RETURN_PRICE = "//label[@autoid='returnpricelabel']//parent::div//following-sibling::div//input"
    UNIT_OF_MEASURE = "//div[@autoid='unitofmeasuredropdown']"
    TAX_GROUP = "//div[@autoid='taxgroupdropdown']"
    RESTRICTION_GROUP = "//div[@autoid='restrictiongroupdropdown']"
    PRICING_GROUP = "//div[@autoid='pricinggroupdropdown']"
    NETWORK_PRODUCT_CODE = "//input[@autoid='networkproductcodemask']"
    INCOMM_PRICE_MIN = "//span[@autoid='incommminpricenumeric']//input"
    INCOMM_PRICE_MAX = "//span[@autoid='incommmaxpricenumeric']//input"
    # Add Item Screen - Tender Restrictions
    CASH_SWITCH = "//div[@autoid='cashcheckbox']"
    CHECK_SWITCH = "//div[@autoid='checkcheckbox']"
    MONEY_ORDER_SWITCH = "//div[@autoid='moneyOrdercheckbox']"
    FOODSTAMPS_SWITCH = "//div[@autoid='foodStampscheckbox']"
    EBT_SWITCH = "//div[@autoid='ebtcheckbox']"
    GIFT_CERTIFICATES_SWITCH = "//div[@autoid='giftCertificatescheckbox']"
    CREDIT_CARDS_SWITCH = "//div[@autoid='creditCardscheckbox']"
    FLEET_CARDS_SWITCH = "//div[@autoid='fleetCardscheckbox']"
    DEBIT_CARDS_SWITCH = "//div[@autoid='debitCardscheckbox']"
    RADIO_FREQUENCY_SWITCH = "//div[@autoid='radioFrequencycheckbox']"
    PREPAID_CARDS_SWITCH = "//div[@autoid='prepaidCardscheckbox']"
    SMART_CARDS_SWITCH = "//div[@autoid='smartCardscheckbox']"
    HOUSE_CHARGES_SWITCH = "//div[@autoid='houseChargescheckbox']"
    DRIVE_OFF_SWITCH = "//div[@autoid='driveOffcheckbox']"
    LOTTERY_WINNING_TICKET_SWITCH = "//div[@autoid='lotteryWinningTicketcheckbox']"
    LOTTO_WINNING_TICKET_SWITCH = "//div[@autoid='lottoWinningTicketcheckbox']"
    WIC_PAYMENT_SWITCH = "//div[@autoid='wicPaymentcheckbox']"
    PUMP_FOR_TEST_SWITCH = "//div[@autoid='pumpForTestcheckbox']"
    USER_DEFINED_SWITCH = "//div[@autoid='userDefinedTenderTypescheckbox']"
    GENERIC_SWITCH = "//div[@autoid='genericcheckbox']"
    OUTSIDE_CREDIT_SWITCH = "//div[@autoid='outsideCreditcheckbox']"
    OUTSIDE_DEBIT_SWITCH = "//div[@autoid='outsideDebitcheckbox']"
    CASH_ACCEPT_OR_CHANGE_SWITCH = "//div[@autoid='cashAcceptorChangecheckbox']"
    AUXILIARY_CREDIT_SWITCH = "//div[@autoid='auxilliaryCreditcheckbox']"
    OUTSIDE_AUXILIARY_CREDIT_SWITCH = "//div[@autoid='outsideAuxilliaryCreditcheckbox']"
    AUXILIARY_DEBIT_SWITCH = "//div[@autoid='auxilliaryDebitcheckbox']"
    OUTSIDE_AUXILIARY_DEBIT_SWITCH = "//div[@autoid='outsideAuxilliaryDebitcheckbox']"
    MOBILE_CREDIT_SWITCH = "//div[@autoid='mobileCreditcheckbox']"
    OUTSIDE_MOBILE_SWITCH = "//div[@autoid='outsideMobileCreditcheckbox']"


class MainMwsPageLocators(BaseEnum):
    LOGO = "//img[@class='header-img-logo']"
    POS_BUTTON = "//i[@autoid='POSButton']"
    SEARCH_BUTTON = "//*[@class='menu-search-icon-style']"
    MENU_SEARCH = "//input[@id='MenuSearch']"
    SEARCH_RESULT = "//span[text()='{}']"
    SAVE_BUTTON = "//span[@class[contains(.,'application-button')] and contains(text(), 'Save')]"
    SAVE_TOAST = "//div[@class='rz-growl-item']//p[text()='Saved']"
    DROPDOWN = "//div[@class='rz-dropdown-items-wrapper']"
    DROPDOWN_VALUE = "//div[(@class[contains(.,'multiselect')] or @class[contains(.,'dropdown')]) and @style[contains(.,'display: block')]]//span[text()='{}']"
    PROMPT_YES = "//span[@class='rz-button-text' and text()='Yes']"
    SUCCESS_BANNER = "//div[@class='rz-growl-message']/span[@class='rz-growl-title' and text()='{}']/following-sibling::p[text()='Saved' or text()='Updated' or text()='Added']"
    BANNER_CLOSE = "(//div[@class='rz-growl-item']//div)[1]"
    DIALOGUE_BOX = "//*[@class='rz-dialog-content']//p"
    YES = "//span[@class='rz-button-text' and text()='Yes']"
    NO = "//span[@class='rz-button-text' and text()='No']"
    SECTION_EXPAND_PLUS_BUTTONS = "//span[contains(@class, 'rzi-plus')]"


class StoreCloseMwsPageLocators(BaseEnum):
    HEADER = "//*[@id='rz-dialog-0-label' and contains(text(), 'Store Close')]"
    YES = "//span[@class='rz-button-text' and text()='Yes']"
    NO = "//span[@class='rz-button-text' and text()='No']"


class ForecourtInstallationMwsPageLocators(BaseEnum):
    HEADER = "//h1[@class='page-header-fixed-title' and contains(text(), 'Forecourt Installation')]"
    DISPENSERS_SUBSECTION = "//*[@autoid='dispensersCollapsiblepanel']"
    PRODUCTS_SUBSECTION = "//*[@autoid='productCollapsiblepanel']"
    DISPENSERS = "//div[@autoid='dispensersCollapsiblepanel']//tbody//tr"
    PRODUCTS = "//div[@autoid='productCollapsiblepanel']//tbody//tr"
    ADD_PRODUCT = "//button[@autoid='ProductAddButton']"
    DELETE_PRODUCT = "//button[@autoid='ProductDeleteButton']"
    EDIT_DISPENSER = "(//button[@autoid='DispenserChangeButton'])[{}]"
    EDIT_PRODUCT = "(//button[@autoid='ProductEditButton'])[{}]"
    DISPENSER_MANUFACTURER = "//input[@autoid='Manufacturer']"
    DISPENSER_SERIAL_NUMBER = "//input[@autoid='SerialNumber']"
    DISPENSER_SAVE_BUTTON = "//button[@autoid='DispenserEditOkButton']"
    TDES_SWITCH = "//div[@autoid='TDESswitch']"
    DISPENSER_TYPE = "//div[@autoid='DispenserType']"
    PUMP_PROTOCOL = "//div[@autoid='PumpProtocol']"
    PAYMENT_TERMINAL_TYPE = "//div[@autoid='PaymentTerminalType']"
    USE_IP_ADDRESS_FOR_PUMP = "//div[@autoid='UseIpAddressPumpSwitchswitch']"
    PUMP_IP_ADDRESS = "//*[@id='IpAddressPump']"
    BILL_ACCEPTOR = "//div[@autoid='BillAcceptorswitch']"
    BAR_CODE = "//div[@autoid='BarCodeswitch']"
    AUTO_ON = "//div[@autoid='AutoOnswitch']"
    DOOR_ALARM = "//div[@autoid='DoorAlarmswitch']"
    COMMERCIAL_DIESEL = "//div[@autoid='CommercialDieselswitch']"
    REFER = "//div[@autoid='ReeferEnabledswitch']"
    PRODUCT_NAME = "//input[@autoid='ProductNameTextBox']"
    PRODUCT_SAVE_BUTTON = "//button[@autoid='ProductEditOkButton']"
    GRADE_EDIT_BUTTON = "//button[@autoid='GradeEditButton']"
    GRADE_SAVE_BUTTON = "//button[@autoid='GradeEditOkButton']"
    GRADE_NAME = "//div[@autoid='GradeNameDropDown']"
    GRADE_REEFER = "//div[@autoid='ReeferDropDown']"
    BLENDED_GRADE = "//div[@autoid='BlendedGradeSwitchswitch']"
    LOW_PRODUCT = "//div[@autoid='LowProductDropDown']"
    LOW_PRODUCT_PERCENT = "//span[@autoid='LowProductPercent']"
    HIGH_PRODUCT = "//div[@autoid='HighProductDropDown']"
    HIGH_PRODUCT_PERCENT = "//span[@autoid='HighProductPercent']"


class RegistersMwsPageLocators(BaseEnum):
    HEADER = "//h1[@class='page-header-fixed-title' and contains(text(), 'Registers')]"
    ADD = "//button[@autoid='AddButton']"
    REGISTERS = "//table[@class[contains(.,'rz-grid-table')]]/tbody/tr"
    EDIT = "//tr[*//text()='{}']//button[@autoid='EditButton']"
    DELETE = "//tr[*//text()='{}']//button[@autoid='DeleteButton']"
    REGISTER_NUMBER = "//span[@autoid='RegisterNumberNumeric']//child::input"
    MACHINE_NAME = "//div[@autoid='MachineNameDropdown']"
    REGISTER_GROUP = "//div[@autoid='RegisterGroupIdDropDown']"
    PERSONALITY = "//div[@autoid='RegisterTypeDropdown']"
    ASSET_ID = "//input[@autoid='AssetIdTextBox']"
    MODEL_NUMBER = "//input[@autoid='ModelNumberTextBox']"
    SERIAL_NUMBER = "//input[@autoid='SerialNumberTextBox']"
    LINE_DISPLAY = "//div[@autoid='LineDisplayTypeDropDown']"
    PINPAD_TYPE = "//div[@autoid='PinpadTypeDropDown']"
    IP_ADDRESS = "//input[@autoid='PinpadIpAddressTextBox']"
    SCANNER_IP = "//input[@autoid='ScannerIpTextBox']"
    PRINTER_TYPE = "//div[@autoid='PrinterTypeDropDown']"
    PRINTER_IP = "//input[@autoid='PrinterIpAddressTextBox']"
    ELECTRONIC_SIGNATURE = "//div[@autoid='switch'][@id='ElectronicSignature']"
    FORWARD_OUTSIDE_TRANSACTION = "//div[@autoid='switch'][@id='ForwardOutsideTransaction']"
    REBOOT_PINPAD = "//div[@autoid='RebootPinpadDatePicker']//input"
    SCANNER_TYPE = "//div[@autoid='ScannerConnectionTypeDropDown']"
    SCANNER_COM_PORT = "//div[@autoid='ScannerComPortDropDown']"


class NetworkSiteConfiguration(BaseEnum):
    HEADER = "//h1[@class='page-header-fixed-title' and contains(text(), 'Global Network Parameters')]"


class TendersMwsPageLocators(BaseEnum):
    HEADER = "//h1[@class='page-header-fixed-title' and contains(text(), 'Tenders')]"
    TENDERS = "//tr[contains(@class, 'rz-data-row')]"
    ADD = "//button[@autoid='addbutton']"
    SAVE_BUTTON = "//a[@class='btn btn-success' and @autoid='savebutton' and not(@disabled)]"
    TENDER_DESCRIPTION = "//input[@autoid='TenderDescription']"
    TENDER_CODE = "(//input[@type='text'])[1]"
    TENDER_GROUP = "//div[@autoid='TenderGroupId']"
    TENDER_ENABLE_SAFE_DROPS = "//div[@id='EnableSafeDrops']"
    TENDER_PRINT_TAX_INVOICE = "//div[@id='PrintTaxInvoiceOnReceipt']"
    TENDER_RECEIPT_DESCRIPTION = "//input[@autoid='ReceiptDescription']"
    TENDER_BUTTON_DESCRIPTION = "//input[@autoid='TenderButtonDescription']"
    NACS_TENDER_CODE = "//div[@autoid='TenderCodeId']"
    EDIT_TENDER = "//button[@tender-id='{}']"
    PRIMARY_TENDER_FOR_CHANGE = "//div[@autoid='PrimaryTenderForChange']"
    SECONDARY_TENDER_FOR_CHANGE = "//div[@autoid='SecondaryTenderForChange']"
