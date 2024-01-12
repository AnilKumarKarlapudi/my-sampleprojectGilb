from hornets.base_enum import BaseEnum


class TenderGroupEnum(BaseEnum):
    CASH = "Cash"
    CHECK = "Check"
    COUPON = "Coupon"
    DRIVE_OFFS = "Drive Offs"
    EBT_CASH_NOT_INTEGRATED = "EBT Cash (Not Integrated)"
    EBT_FOOD_NOT_INTEGRATED = "EBT Food (Not Integrated)"
    FOOD_STAMPS = "Food Stamps"
    IMPRINTER_INTEGRATED = "Imprinter (Integrated)"
    IMPRINTER_NOT_INTEGRATED = "Imprinter (Not Integrated)"
    INTEGRATED_COMMERCIAL_CHECK = "Integrated Commercial Check"
    INTEGRATED_CREDIT = "Integrated Credit"
    INTEGRATED_EBT_CASH = "Integrated EBT Cash"
    INTEGRATED_EBT_FOOD = "Integrated EBT Food"
    LOCAL_ACCOUNTS = "Local Accounts"
    NOT_INTEGRATED_CREDIT = "Not Integrated Credit"
    NOT_INTEGRATED_DEBIT = "Not Integrated Debit"


class NacsTenderCodeEnum(BaseEnum):
    CASH = "cash"
    CHECK = "check"
    MONEY_ORDER = "moneyOrder"
    FOOD_STAMPS = "foodStamps"
    EBT_CASH = "ebt"
    GIFT_CERTIFICATES = "giftCertificates"
    CREDIT_CARDS = "creditCards"
    FLEET_CARDS = "fleetCards"
    DEBIT_CARDS = "debitCards"
    RADIO_FREQUENCY = "radioFrequency"
    PREPAID_CARDS = "prepaidCards"
    SMART_CARDS = "smartCards"
    HOUSE_CHARGES = "houseCharges"
    DRIVE_OFF = "driveOff"
    LOTTERY_WINNING_TICKET = "lotteryWinningTicket"
    LOTTO_WINNING_TICKET = "lottoWinningTicket"
    COUPONS = "coupons"
    WIC_PAYMENT = "wicPayment"
    PUMP_FOR_TEST = "pumpForTest"
    USER_DEFINED_TENDERS_TYPES = "userDefinedTendersTypes"
    GENERIC = "generic"
    OUTSIDE_CREDIT = "outsideCredit"
    OUTSIDE_DEBIT = "outsideDebit"
    CASH_ACCEPTOR_CHANGE = "cashAcceptorChange"
    AUXILIARY_CREDIT = "auxiliaryCredit"
    OUTSIDE_AUXILIARY_CREDIT = "outsideAuxiliaryCredit"
    AUXILIARY_DEBIT = "auxiliaryDebit"
    OUTSIDE_AUXILIARY_DEBIT = "outsideAuxiliaryDebit"
    LOYALTY_OFFER = "loyaltyOffer"
    MOBILE_CREDIT = "mobileCredit"
    OUTSIDE_MOBILE_CREDIT = "outsideMobileCredit"


class PrimaryTenderForChangeEnum(BaseEnum):
    OTHER = "Other"
    NO_TENDER = "No Tender"


class SecondaryTenderForChangeEnum(BaseEnum):
    OTHER = "Other"
    NO_TENDER = "No Tender"
