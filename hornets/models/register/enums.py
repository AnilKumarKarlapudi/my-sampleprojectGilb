from libs.common.enums import InterfaceEnum


class RegisterType(InterfaceEnum):
    UNKNOWN = (0, "")
    CASHIER_WORKSTATION = (1, "Cashier Workstation")
    EDGE = (2, "EDGE")
    EL_CASHIER_CONTROL_CONSOLE = (3, "Cashier Control Console")
    EXPRESS_LANE = (4, "Express Lane")
    FLEX = (5, "FLEX")
