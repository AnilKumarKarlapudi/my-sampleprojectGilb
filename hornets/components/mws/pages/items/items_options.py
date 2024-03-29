from selenium.webdriver.chrome.webdriver import WebDriver

from hornets.base import BaseOptions
from hornets.components.mws.mws_locators import ItemsMwsPageLocators


class ItemOptions(BaseOptions):

    def __init__(self, driver: WebDriver):
        super().__init__(driver=driver,
                         fields=[
                             ItemsMwsPageLocators.PLU_INPUT,
                             ItemsMwsPageLocators.DESCRIPTION_INPUT,
                             ItemsMwsPageLocators.DEPARTMENT_DROPDOWN,
                             ItemsMwsPageLocators.TYPE_DROPDOWN,
                             ItemsMwsPageLocators.PRICE_REQUIRED_SWITCH,
                             ItemsMwsPageLocators.NORMAL_PRICE_RADIO,
                             ItemsMwsPageLocators.NORMAL_PRICE_INPUT,
                             ItemsMwsPageLocators.BASE_PLUS_ONE_RADIO,
                             ItemsMwsPageLocators.BASE_PLUS_ONE_UNITPRICE_INPUT,
                             ItemsMwsPageLocators.BASE_PLUS_ONE_DEALQUANTITY_INPUT,
                             ItemsMwsPageLocators.GROUP_THRESHOLD_RADIO,
                             ItemsMwsPageLocators.GROUP_THRESHOLD_UNITPRICE_INPUT,
                             ItemsMwsPageLocators.GROUP_THRESHOLD_DEALQUANTITY_INPUT,
                             ItemsMwsPageLocators.GROUP_THRESHOLD_DEALPRICE_INPUT,
                             ItemsMwsPageLocators.BULK_RADIO,
                             ItemsMwsPageLocators.BULK_DEALQUANTITY_INPUT,
                             ItemsMwsPageLocators.BULK_DEALPRICE_INPUT,
                             ItemsMwsPageLocators.UNIT_ADJUSTED_RADIO,
                             ItemsMwsPageLocators.UNIT_ADJUSTED_UNITPRICE_INPUT,
                             ItemsMwsPageLocators.UNIT_ADJUSTED_DEALQUANTITY_INPUT,
                             ItemsMwsPageLocators.UNIT_ADJUSTED_DEALPRICE_INPUT,
                             ItemsMwsPageLocators.ACTIVE_FOR_SALE,
                             ItemsMwsPageLocators.FOOD_STAMPABLE,
                             ItemsMwsPageLocators.DISCOUNTABLE,
                             ItemsMwsPageLocators.FEE,
                             ItemsMwsPageLocators.ALLOW_REFUNDS,
                             ItemsMwsPageLocators.QUANTITY_ALLOWED,
                             ItemsMwsPageLocators.QUANTITY_REQUIRED,
                             ItemsMwsPageLocators.FRACTIONAL_QUANTITY_ALLOWED,
                             ItemsMwsPageLocators.RETURN_PRICE,
                             ItemsMwsPageLocators.UNIT_OF_MEASURE,
                             ItemsMwsPageLocators.TAX_GROUP,
                             ItemsMwsPageLocators.RESTRICTION_GROUP,
                             ItemsMwsPageLocators.PRICING_GROUP,
                             ItemsMwsPageLocators.NETWORK_PRODUCT_CODE,
                             ItemsMwsPageLocators.INCOMM_PRICE_MIN,
                             ItemsMwsPageLocators.INCOMM_PRICE_MAX,
                             ItemsMwsPageLocators.CASH_SWITCH,
                             ItemsMwsPageLocators.CHECK_SWITCH,
                             ItemsMwsPageLocators.MONEY_ORDER_SWITCH,
                             ItemsMwsPageLocators.FOODSTAMPS_SWITCH,
                             ItemsMwsPageLocators.EBT_SWITCH,
                             ItemsMwsPageLocators.GIFT_CERTIFICATES_SWITCH,
                             ItemsMwsPageLocators.CREDIT_CARDS_SWITCH,
                             ItemsMwsPageLocators.FLEET_CARDS_SWITCH,
                             ItemsMwsPageLocators.DEBIT_CARDS_SWITCH,
                             ItemsMwsPageLocators.RADIO_FREQUENCY_SWITCH,
                             ItemsMwsPageLocators.PREPAID_CARDS_SWITCH,
                             ItemsMwsPageLocators.SMART_CARDS_SWITCH,
                             ItemsMwsPageLocators.HOUSE_CHARGES_SWITCH,
                             ItemsMwsPageLocators.DRIVE_OFF_SWITCH,
                             ItemsMwsPageLocators.LOTTERY_WINNING_TICKET_SWITCH,
                             ItemsMwsPageLocators.LOTTO_WINNING_TICKET_SWITCH,
                             ItemsMwsPageLocators.WIC_PAYMENT_SWITCH,
                             ItemsMwsPageLocators.PUMP_FOR_TEST_SWITCH,
                             ItemsMwsPageLocators.USER_DEFINED_SWITCH,
                             ItemsMwsPageLocators.GENERIC_SWITCH,
                             ItemsMwsPageLocators.OUTSIDE_CREDIT_SWITCH,
                             ItemsMwsPageLocators.OUTSIDE_DEBIT_SWITCH,
                             ItemsMwsPageLocators.CASH_ACCEPT_OR_CHANGE_SWITCH,
                             ItemsMwsPageLocators.AUXILIARY_CREDIT_SWITCH,
                             ItemsMwsPageLocators.OUTSIDE_AUXILIARY_CREDIT_SWITCH,
                             ItemsMwsPageLocators.AUXILIARY_DEBIT_SWITCH,
                             ItemsMwsPageLocators.OUTSIDE_AUXILIARY_DEBIT_SWITCH,
                             ItemsMwsPageLocators.MOBILE_CREDIT_SWITCH,
                             ItemsMwsPageLocators.OUTSIDE_MOBILE_SWITCH,
                         ])
