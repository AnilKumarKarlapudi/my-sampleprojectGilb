from hornets.base_enum import BaseEnum


class ItemDepartmentEnum(BaseEnum):
    DEPT_1 = "Dept 1"
    DEPT_2 = "Dept 2"
    DEPT_3 = "Dept 3"
    DEPT_4 = "Dept 4"
    DEPT_5 = "Dept 5"
    DEPT_6 = "Dept 6"
    DEPT_7 = "Dept 7"
    DEPT_8 = "Dept 8"
    DEPT_9 = "Dept 9"
    DEPT_10 = "Dept 10"
    DEPT_11 = "Dept 11"
    DEPT_12 = "Dept 12"
    DEPT_13 = "Dept 13"
    DEPT_14 = "Dept 14"
    DEPT_15 = "Dept 15"
    DEPT_16 = "Dept 16"
    FUEL_1 = "Fuel 1"
    FUEL_2 = "Fuel 2"
    OUTSIDE_LOTTERY = "Outside Lottery"
    RESET_PASSWORD = "Reset Password"
    CHANGE_DUE = "Change/Refund Due"
    FEES = "Fees"
    CASH_CARD = "Cash Card"
    STORE_COUPON = "Store Coupon"
    CAR_WASH = "Car Wash"


class ItemTypeEnum(BaseEnum):
    REGULAR_ITEM = "Regular Item"
    CARWASH = "Car Wash"
    INCOMM_FAST_PIN_DDP = "InComm Fast PIN DDP"
    INCOMM_FAST_PIN = "InComm Fast PIN"
    INCOMM_RTR = "InComm Fast RTR"
    INCOMM_GIFT_CARD = "InComm Gift Card"


class ItemRestrictionGroupEnum(BaseEnum):
    NO_RESTRICTION = "<No Restrictions>"
    MUST_BE_18_PDI = "Must be 18 (PDI)"
    MUST_BE_21_PDI = "Must be 21 (PDI)"
    MUST_BE_19_PDI = "Must be 19 (PDI)"
    MUST_BE_18 = "Must be 18"
    MUST_BE_21 = "Must be 21"
    MUST_BE_19 = "Must be 19"
