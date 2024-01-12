from hornets.utilities.log_config import logger


class NotApplicableDiscountException(Exception):
    pass


class DataInconsistencyException(Exception):
    pass


class ControlNotFoundError(Exception):
    logger.error("Control not found")


class ControlAmbiguousError(Exception):
    logger.error("More than one control")


class ElementNotFoundException(Exception):
    pass


class ElementNotSavedException(Exception):
    pass


class ConfigurationNotSavedException(Exception):
    pass
