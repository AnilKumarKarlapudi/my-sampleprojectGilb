from libs.edh.common.enums import EDHDatabase
from libs.infra.db.models import Field
from libs.infra.db.models import ModelPK
from libs.infra.db.models import SQLModel


class EncryptionConfig(SQLModel):
    """
    Encryption Config model
    """

    class META(SQLModel.META):
        """
        Model metadata placeholder
        """
        db = EDHDatabase.NETWORK
        table_name = 'EncryptionConfig'
        pk = ModelPK('ConfigID')
        columns = {
            'ConfigID': Field('config_id'),
            'Value': Field('value')
        }

    # SQL: ConfigID
    config_id: int

    # SQL: Value
    value: str
