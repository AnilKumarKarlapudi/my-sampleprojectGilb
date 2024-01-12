from hornets.base_enum import BaseEnum


class PaymentMethodEnum(BaseEnum):
    CASH = "Cash"
    CREDIT_CARD = "Credit Card"
    DEBIT_CARD = "Debit Card"
    GIFT_CARD = "Gift Card"
    CHEQUE = "Cheque"


class PosStateEnum(BaseEnum):
    UNKNOWN = "Unknown"
    IDLE = "Idle"
    IN_TRANSACTION = "In Transaction"
    LOGOUT = "Logout"
    IN_TRANSACTION_AFTER_PAYMENT = "In Transaction After Payment"
    SELECTING_DISCOUNT = "Selecting Discount"


class DispenserStatusEnum(BaseEnum):
    UNKNOWN = "Unknown"
    STOPPED = "Stopped"
    INOPERATIVE = "Inoperative"
    IDLE = "Idle"


class WatermarkDisplayEnum(BaseEnum):
    TRANSACTION_COMPLETED = "transaction_completed"
    TRANSACTION_VOIDED = "transaction_voided"


class StatusInformationEnum(BaseEnum):
    DEVICE_STATUS = "device_status"
    STATUS_INFORMATION = "status_information"
    BACK = "back"
