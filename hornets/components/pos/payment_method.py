from abc import ABC, abstractmethod

from hornets.components.pos.enums import PaymentMethodEnum
from hornets.models.credit_card.models import CreditCard


class PaymentMethod(ABC):
    def __init__(self, payment_method: PaymentMethodEnum):
        self.payment_method_name = payment_method

    def __str__(self):
        return f"{self.payment_method_name}"

    @abstractmethod
    def pay_with(self, pos):
        raise NotImplementedError


class CashPaymentMethod(PaymentMethod):
    def __init__(self):
        super().__init__(PaymentMethodEnum.CASH)

    def pay_with(self, pos):
        pos._process_payment_with_cash()


class CreditCardPaymentMethod(PaymentMethod):
    def __init__(self, credit_card: CreditCard):
        super().__init__(PaymentMethodEnum.CREDIT_CARD)
        self.credit_card = credit_card

    def pay_with(self, pos):
        pos._process_payment_with_credit_card(self.credit_card)


class DebitCardPaymentMethod(PaymentMethod):
    def __init__(self):
        super().__init__(PaymentMethodEnum.DEBIT_CARD)

    def pay_with(self, pos):
        pos._process_payment_with_debit_card()


class ChequePaymentMethod(PaymentMethod):
    def __init__(self):
        super().__init__(PaymentMethodEnum.CHEQUE)

    def pay_with(self, pos):
        pos._process_payment_with_cheque()
