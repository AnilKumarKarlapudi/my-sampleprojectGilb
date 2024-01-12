from typing import Callable

from libs.edh.common.constants import EDHDatasourceProperties
from libs.edh.common.constants import EDH_NETWORK_UNKNOWN_ADDRESS
from libs.edh.common.constants import EDH_NETWORK_UNKNOWN_PORT
from libs.edh.common.enums import EDHBrands
from libs.edh.common.enums import EDHDatabase
from libs.edh.network.message.handler.base import NetworkHandler
from libs.infra.db.command import SQLCommand
from libs.infra.db.utils import prepare_statement


class ConcordNetworkHandler(NetworkHandler):
    """
    CONCORD Network handler implementation
    """
    def __init__(self):
        super().__init__()
        self._brand = EDHBrands.CONCORD
        self._ds_properties = EDHDatasourceProperties.with_database(EDHDatabase.NETWORK)

    def _init(self):
        """
        Concord network initialization
        """
        statement = prepare_statement("UPDATE ConnectionInfo set IPAddress = {ip}, IPPort = {port}",
                                      ip=EDH_NETWORK_UNKNOWN_ADDRESS,
                                      port=EDH_NETWORK_UNKNOWN_PORT)

        command = SQLCommand(statement, self._ds_properties)
        if not command.execute():
            raise Exception("Unable to change ConnectionInfo for CONCORD network handler.")

    def filterer(self) -> Callable[[str], bool]:
        """
        Concord message body filterer
        """
        def __inner__(message: str) -> bool:
            return "> [" in message
        return __inner__
