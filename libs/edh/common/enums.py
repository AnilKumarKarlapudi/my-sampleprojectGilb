class EDHDatabase(object):
    """
    EDH Database names enum
    """
    GLOBAL_STORE = "GlobalSTORE"
    GVR_DATA = "GRVData"
    NETWORK = "network"


class EDHBrand(object):
    """
    EDH Brand object model
    """

    def __init__(self, psp_id: int, name: str):
        self.psp_id = psp_id
        self.name = name


class EDHBrands(object):
    """
    EDH Brands names and pspids
    """
    CHICAGO = EDHBrand(20, "CHICAGO")
    FAST_STOP = EDHBrand(20, "FASTSTOP")
    CONCORD = EDHBrand(23, "CONCORD")
    SUNOCO = EDHBrand(23, "SUNOCO")
    VALERO = EDHBrand(23, "VALERO")
    EXXON = EDHBrand(23, "EXXON")
    MOBIL = EDHBrand(23, "MOBIL")
    HPS_DALLAS = EDHBrand(24, "HPS-DALLAS")
    CITGO = EDHBrand(24, "CITGO")
    MARATHON = EDHBrand(24, "MARATHON")
    PHILLIPS66 = EDHBrand(24, "PHILLIPS66")
    CHEVRON = EDHBrand(26, "CHEVRON")
    TEXACO = EDHBrand(26, "TEXACO")
    SHELL = EDHBrand(27, "SHELL")
    BP = EDHBrand(29, "BP")
    IOL = EDHBrand(30, "IOL")
    CENEX = EDHBrand(32, "CENEX")
    NBS = EDHBrand(32, "NBS")
    WORLDPAY = EDHBrand(34, "WORLDPAY")

    @classmethod
    def of(cls, brand: str) -> EDHBrand:
        """
        Get brand information by given brand name.

        :raises KeyError: if given brand is not defined
        """
        for key, value in cls.__dict__.items():
            if not key.startswith('_') and key != 'of':
                if value.name == brand.upper():
                    return value
        raise KeyError(f"Brand {brand} is not defined!")

    @classmethod
    def is_concord(cls, brand: str) -> bool:
        """
        Check if given brand is CONCORD (PSP_ID = 23)
        """
        return brand.upper() in [value.name for value in [cls.CONCORD, cls.SUNOCO, cls.VALERO, cls.EXXON, cls.MOBIL]]

    @classmethod
    def is_chicago(cls, brand: str) -> bool:
        """
        Check if given brand is CHICAGO (PSP_ID = 20)
        """
        return brand.upper() in [value.name for value in [cls.CHICAGO, cls.FAST_STOP]]


class EDHPspID:
    """
    EDH Psp ID
    """
    CHICAGO = EDHBrands.CHICAGO.psp_id
    FAST_STOP = EDHBrands.FAST_STOP.psp_id
    CONCORD = EDHBrands.CONCORD.psp_id
    SUNOCO = EDHBrands.SUNOCO.psp_id
    VALERO = EDHBrands.VALERO.psp_id
    EXXON = EDHBrands.EXXON.psp_id
    MOBIL = EDHBrands.MOBIL.psp_id
    HPS_DALLAS = EDHBrands.HPS_DALLAS.psp_id
    CITGO = EDHBrands.CITGO.psp_id
    MARATHON = EDHBrands.MARATHON.psp_id
    PHILLIPS66 = EDHBrands.PHILLIPS66.psp_id
    CHEVRON = EDHBrands.CHEVRON.psp_id
    TEXACO = EDHBrands.TEXACO.psp_id
    SHELL = EDHBrands.SHELL.psp_id
    BP = EDHBrands.BP.psp_id
    IOL = EDHBrands.IOL.psp_id
    CENEX = EDHBrands.CENEX.psp_id
    NBS = EDHBrands.NBS.psp_id
    WORLDPAY = EDHBrands.WORLDPAY.psp_id
    RBS = 34
    OLD_EXXON_MOBILE = 28
    MANNATEC = 50
    LOCAL_ACCOUNTS = 51
    PINPAD = 52
    INCOMM = 53
    FIDELITY = 54
    PAY_NEAR_ME = 55
    ADS_DALLAS_AUXILIARY = 56
    LINQ3 = 57
    FDMOBILE = 60
    GS1_COUPON = 62
    PINPAD2 = 63
    MOBILE = 90
    LOYALTY = 100

    @classmethod
    def is_concord(cls, psp_id: int) -> bool:
        return psp_id == cls.CONCORD
