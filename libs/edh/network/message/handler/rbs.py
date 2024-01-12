from typing import Callable

from libs.edh.network.message.handler.base import NetworkHandler
from libs.edh.common.enums import EDHBrands
from libs.edh.common.constants import EDH_NETWORK_UNKNOWN_ADDRESS
from libs.edh.common.constants import EDH_NETWORK_UNKNOWN_PORT
from libs.infra.db.utils import prepare_statement
from libs.infra.db.command import SQLCommand
from libs.edh.common.constants import EDHDatasourceProperties
from libs.edh.common.enums import EDHDatabase


class RBSNetworkHandler(NetworkHandler):
    """
    RBS Network Handler implementation
    """
    # NOTE: This is kind of a magic number, but in the old framework it was also hardcoded...
    TERMINAL_ID = "542929803125772000088971"

    def __init__(self):
        super().__init__()

        # Why is this WORLDPLAY and not RBS or NBS?
        self._brand = EDHBrands.WORLDPAY
        self._ds_props = EDHDatasourceProperties.with_database(EDHDatabase.NETWORK)

    def _init(self):
        """
        RBS Network initialization
        """
        # RBS ConnectionInfo update
        query = ("UPDATE RBS_ConnectionInfo "
                 "SET "
                 "PrimaryIPAddress = {primary_ip}, "
                 "PrimaryIPPort = {primary_port}, "
                 "SecondaryIPAddress = {secondary_ip}, "
                 "SecondaryIPPort = {secondary_port}, "
                 "URLAndIPPort = {url_port}, "
                 "EnableSSL = {enable_ssl}")

        # NOTE: URLAndIPPort is not defined anywhere... how?
        statement = prepare_statement(query,
                                      primary_ip=EDH_NETWORK_UNKNOWN_ADDRESS,
                                      primary_port=EDH_NETWORK_UNKNOWN_PORT,
                                      secondary_ip=EDH_NETWORK_UNKNOWN_ADDRESS,
                                      secondary_port=EDH_NETWORK_UNKNOWN_PORT,
                                      url_port="",
                                      enable_ssl='2')

        command = SQLCommand(statement, self._ds_props)
        if not command.execute():
            raise Exception("Cannot update RBS_ConnectionInfo")

        # RBS GlobalInfo update
        statement = prepare_statement("UPDATE RBS_GlobalInfo SET TID = {tid}", tid=self.TERMINAL_ID)
        command = SQLCommand(statement, self._ds_props)

        if not command.execute():
            raise Exception("Cannot update RBS_GlobalInfo")

    def filterer(self) -> Callable[[str], bool]:
        """
        Dummy filter for RBS: see GenericNetworkHandler for specific implementation
        """
        return lambda message: True
