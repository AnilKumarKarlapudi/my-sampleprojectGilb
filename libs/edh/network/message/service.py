import logging
from typing import Optional

from libs.edh.common.enums import EDHPspID
from libs.edh.network.message.parser import NetworkMessageParseService
from libs.edh.network.message.models import MessageBody
from libs.edh.network.message.models import MessageChecker
from libs.edh.network.message.models import NetworkMessage
from libs.infra.db.handler import get_datasource
from libs.infra.db.queries import F
from libs.infra.db.queries import Q
from libs.common.utils import Timeout
from libs.edh.common.constants import EDHDatasourceProperties
from libs.edh.common.enums import EDHDatabase
from libs.infra.io.system import platform
from libs.edh.common.enums import EDHBrands


class NetworkMessageService:
    """
    EDH Network Message Service object
    """

    def __init__(self):
        """
        Constructor of EDH Service
        """
        self._brand = EDHBrands.of(platform.get_brand())

        self.log = logging.getLogger(NetworkMessageService.__name__)  # TODO: use full name (with module)

        self.datasource = get_datasource(NetworkMessage, EDHDatasourceProperties.with_database(EDHDatabase.NETWORK))

        self.parser = NetworkMessageParseService()

    def get_parsed_network_message_body(
            self,
            message: NetworkMessage,
            timeout: int = 60
    ) -> Optional[MessageBody]:
        """
        Get message body parsed into a dict (usually).

        :param message: EDHNetworkMessage - message
        :param timeout: int - timeout
        :return: Optional[EDHMessageBody] - parsed message body
        """
        if not message.can_translate():
            return None

        payload = (f"{message.network_message_id} "
                   f"{message.network_message_date_time}           "
                   f"{message.network_psp_id} {message.network_message}")
        ok, message_body = self.parser.parse_network_message_body(payload, timeout)
        if not ok:
            self.log.error(f"Message could not be parsed due to: {message_body}")
        return message_body

    def get_last_network_message(
            self,
            psp_id: int = EDHPspID.CONCORD,
            start_at_message_id: Optional[int] = None
    ) -> Optional[NetworkMessage]:
        """
        Get last network message by given psp_id and (or) a start message id

        :param psp_id: EDHPspId - PSP ID
        :param start_at_message_id: Optional[int] - last known message id
        :return: Optional[EDHNetworkMessage] - last network message if found
        """

        query = Q(NetworkMessage).select().limit(1).eq('network_psp_id', psp_id)
        if start_at_message_id is not None:
            query = query.and_(F().gt('network_message_id', start_at_message_id))
        query = query.desc('network_message_id')

        messages = self.datasource.query(query)
        if len(messages) > 0:
            return messages[0]

        self.log.error("No message was retrieved!")

    def wait_for_network_message(
            self,
            message_checker: MessageChecker,
            psp_id: int = EDHPspID.CONCORD,
            batch_size: int = 10,
            last_message_id: Optional[int] = None,
            timeout: int = 60
    ) -> Optional[NetworkMessage]:
        """
        Await for a new message that matches the given psp_id and the expected message body in a given timeout.

        :param psp_id: EDHPspId - PSP ID
        :param message_checker: EDHMessageChecker - callback message checker
        :param batch_size: int - batch size for query
        :param last_message_id: Optional[int] - last known message id
        :param timeout: int - timeout
        :return: Optional[EDHNetworkMessage] - message if found
        """

        if last_message_id is None:
            last_known_message = self.get_last_network_message(psp_id)
            if last_known_message:
                last_message_id = last_known_message.network_message_id

        clock = Timeout(timeout)
        while not clock.is_timeout():
            query = Q(NetworkMessage) \
                .select() \
                .limit(batch_size) \
                .eq('network_psp_id', psp_id.value) \
                .and_(F().gt('network_message_id', last_message_id)) \
                .desc('network_message_id')

            for message in self.datasource.query(query):
                if message_checker(message):
                    return message
                else:
                    if message.network_message_id > last_message_id:
                        last_message_id = message.network_message_id

            clock.wait(1.0)

        self.log.error("No message was received!")
