from enum import Enum


class PassportServices(Enum):
    """
    Passport services with corresponding port numbers.
    TLS ports!
    """

    ASU = 5802
    FTS = 5810
    POS = 7490
    SCHEDULER = 7491
    FUEL_CONFIGURATION = 7492
    CONFIGURATION = 7493
    REPORTING = 7494
    MWS_WEB_APP = 7495
    LOCAL_ACCOUNTS = 7496
    REMOTE_SUPPORT = 7497
    REMOTE_MANAGER = 7498
    CONTAINER = 7499
    LEGACY_HTML_POS = 7500
    POS_WEB_APP = 7501
