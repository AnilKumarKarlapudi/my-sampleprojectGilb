from typing import Callable, Optional, Union, Dict, Any

from libs.edh.common.enums import EDHDatabase
from libs.infra.db.models import SQLModel
from libs.infra.db.schemas import ModelPK, Field

# EDH Message Body type
MessageBody = Union[str, Dict[str, Any]]

# EDH Message Body Extractor function contract
MessageBodyExtractor = Callable[[str], Optional[MessageBody]]

# EDH Message Body Checker function contract
MessageChecker = Callable[['NetworkMessage'], bool]


class NetworkMessage(SQLModel):
    """
    EDHNetworkMessage model
    """

    class META(SQLModel.META):
        """
        Model metadata placeholder
        """
        db = EDHDatabase.NETWORK
        table_name = 'networkmessages'
        pk = ModelPK('network_message_id')
        columns = {
            'NetworkMessageId': Field('network_message_id'),
            'NetworkMessageDateTime': Field('network_message_date_time'),
            'NetworkPSPId': Field('network_psp_id'),
            'NetworkMessage': Field('network_message')
        }

    # SQL: NetworkMessageId
    network_message_id: int

    # SQL: NetworkMessageDateTime
    network_message_date_time: str

    # SQL: NetworkPSPId
    network_psp_id: int

    # SQL: NetworkMessage
    network_message: str

    def get_message_body(self, extractor: Optional[MessageBodyExtractor] = None) -> Optional[MessageBody]:
        """
        Get message body using a custom extractor (if set) otherwise, return the raw network_message field.

        :param extractor: Optional[MessageBodyExtractor] - if set, use this as the body extractor
        :return: Option[MessageBody] - str or dict
        """
        if extractor:
            return extractor(self.network_message)
        return self.network_message

    def can_translate(self) -> bool:
        """
        Check if the network message can be translated.
        """
        return "=> [" in self.network_message
