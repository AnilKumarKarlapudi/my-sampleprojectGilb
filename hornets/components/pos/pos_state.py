from abc import abstractmethod, ABC

from hornets.components.pos.enums import PosStateEnum
from hornets.utilities.log_config import logger


class PosState(ABC):

    def __init__(self, state: PosStateEnum):
        self._state = state
        logger.info(f"POS is in '{self}' state")

    def __str__(self):
        return f"{self._state}"

    @abstractmethod
    def return_to_idle(self, pos):
        """
        Return to idle state
        Raise:
            NotImplementedError
        """
        raise NotImplementedError


class UnknownPosState(PosState):

    def __init__(self, state: PosStateEnum = PosStateEnum.UNKNOWN):
        super().__init__(state)

    def return_to_idle(self, pos):
        pos.get_pos_state().return_to_idle(pos)


class IdlePosState(PosState):

    def __init__(self, state: PosStateEnum = PosStateEnum.IDLE):
        super().__init__(state)

    def return_to_idle(self, pos):
        """
        Return to idle state
        """
        pos._set_idle_pos_state()


class InTransactionPosState(PosState):

    def __init__(self, state: PosStateEnum = PosStateEnum.IN_TRANSACTION):
        super().__init__(state)

    def return_to_idle(self, pos):
        """
        Return to idle state
        """
        pos.void_transaction()


class LogoutPosState(PosState):

    def __init__(self, state: PosStateEnum = PosStateEnum.LOGOUT):
        super().__init__(state)

    def return_to_idle(self, pos):
        """
        Return to idle state
        """
        pos.logged_in()


class InTransactionAfterPaymentPosState(PosState):

    def __init__(self, state: PosStateEnum = PosStateEnum.IN_TRANSACTION_AFTER_PAYMENT):
        super().__init__(state)

    def return_to_idle(self, pos):
        """
        Return to idle state
        Return:
            InTransactionPosState: In transaction state
        """
        pos._cancel_transaction_after_payment()
        return InTransactionPosState().return_to_idle(pos)


class SelectingDiscountPosState(PosState):

    def __init__(self, state: PosStateEnum = PosStateEnum.SELECTING_DISCOUNT):
        super().__init__(state)

    def return_to_idle(self, pos):
        """
        Return to idle state
        Return:
            InTransactionPosState: In transaction state
        """
        pos._cancel_transaction_when_the_discount_is_selected()
        return InTransactionPosState().return_to_idle(pos)
