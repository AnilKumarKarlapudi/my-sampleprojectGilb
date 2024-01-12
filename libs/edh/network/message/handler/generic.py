from typing import Callable

from libs.edh.common.enums import EDHBrand
from libs.edh.common.enums import EDHPspID
from libs.edh.network.message.handler.base import NetworkHandler


class GenericNetworkHandler(NetworkHandler):
    """
    Generic Network Handler implementation
    """
    def __init__(self, brand: EDHBrand):
        super().__init__()
        self._brand = brand

    def _init(self):
        """
        Dummy implementation of initialization
        """
        pass

    def filterer(self) -> Callable[[str], bool]:
        """
        Filterer implementation by its brand
        """
        if EDHPspID.CHICAGO == self._brand.psp_id:
            return self._chicago()

        elif EDHPspID.HPS_DALLAS == self._brand.psp_id:
            return self._hps_dallas()

        elif EDHPspID.CHEVRON == self._brand.psp_id:
            return self._chevron()

        elif self._brand.psp_id in [EDHPspID.NBS, EDHPspID.RBS]:
            return self._nbs_rbs()

        elif EDHPspID.MOBILE == self._brand.psp_id:
            return self._mobile()

        else:
            # Dummy
            return lambda message: True

    @classmethod
    def _chicago(cls) -> Callable[[str], bool]:
        def checker(message: str) -> bool:
            return "Re" in message

        return checker

    @classmethod
    def _hps_dallas(cls) -> Callable[[str], bool]:
        def checker(message: str) -> bool:
            return "24" in message

        return checker

    @classmethod
    def _chevron(cls) -> Callable[[str], bool]:
        def checker(message: str) -> bool:
            tags = ["2100", "2210", "2304", "2430", "2604", "2804",
                    "2110", "2220", "2314", "2504", "2614", "2814",
                    "2200", "2230", "2420", "2514", "2644"]
            return any([tag in message for tag in tags])

        return checker

    @classmethod
    def _nbs_rbs(cls) -> Callable[[str], bool]:
        def checker(message: str) -> bool:
            return any([tag in message for tag in ["Request", "Response"]])

        return checker

    @classmethod
    def _mobile(cls) -> Callable[[str], bool]:
        def checker(message: str) -> bool:
            return "HeartBeat" not in message and any([tag in message for tag in ["REQUEST", "RESPONSE"]])

        return checker
