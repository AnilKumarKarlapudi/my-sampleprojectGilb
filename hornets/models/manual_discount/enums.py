from libs.common.enums import InterfaceEnum


class ManualDiscountReason(InterfaceEnum):
    UNKNOWN = (0, "")
    STORE_COUPON_OFFER = (1, "Store Coupon")
    FREE_CAR_WASH_OFFER = (2, "Free Car Wash")
    TECHNICIAN_TEST_CW = (3, "Technician Test (Car Wash)")
    EMPLOYEE_DISCOUNT = (4, "Employee Discount")
    SERVICES_DISCOUNT = (5, "Police Discount")
    SENIORS_DISCOUNT = (6, "Senior Citizen Discount")
    CLOSE_2_EXPIRY_DATE = (7, "Expiration Date")
    REDUCE_QUICK_SALE = (8, "")
    LOYALTY_DISCOUNT = (9, "Frequent Shopper")
    MANUF_COUPON_NO_TAX = (10, "")
    MANAGERS_GOODWILL = (11, "Goodwill Discount")
    MANAGER_PROMOTION = (12, "Manager Promotion")
    REG_PRICE_CHANGE = (13, "Reguilar Price Change")
    COMBINATION_OFFER = (14, "")
    FUELS_DISC_CAR_WASH = (15, "")
    MIX_AND_MATCH_OFFER = (16, "")
    TEMP_PRICE_CHANGE = (17, "")


class ManualDiscountMethod(InterfaceEnum):
    UNKNOWN = (0, ["fixed", "item", "amount_off"])
    ITEM_AMOUNT_OFF = (1, ["fixed", "item", "amount_off"])
    ITEM_PERCENTAGE_OFF = (2, ["fixed", "item", "percentage_off"])
    ITEM_NEW_PRICE = (6, ["fixed", "item", "new_price"])
    ITEM_FREE_ITEM = (7, ["fixed", "item", "free_item"])
    TRANSACTION_OFF = (9, ["fixed", "transaction", "amount_off"])
    TRANSACTION_PERCENTAGE_OFF = (10, ["fixed", "transaction", "percentage_off"])

    ITEM_NEW_PRICE_PRORATED = (11, ["fixed", "item", "new_price"])
    ITEM_STEP_PERCENTAGE_PRORATED = (12, ["variable", "item", "percentage_off"])
    ITEM_STEP_AMOUNT_PRORATED = (13, ["variable", "item", "amount_off"])
    STD_TRANSACTION_PCT = (14, ["fixed", "transaction", "percentage_off"])

    @classmethod
    def get_method_from_options(cls, discount_amount_type, apply_discount_to, discount_type):
        options = {discount_amount_type, apply_discount_to, discount_type}
        attrs = [item for item in dir(ManualDiscountMethod) if not item.startswith("__")]
        for attr in attrs:
            if options == set(getattr(cls, attr).value[1]):
                return getattr(cls, attr)
        else:
            raise Exception("No method found for the given options.")
