from libs.edh.common.enums import EDHDatabase
from libs.infra.db.models import Field
from libs.infra.db.models import ModelPK
from libs.infra.db.models import SQLModel


class SMIStatus(SQLModel):
    """
    SMI Status model
    """

    class META(SQLModel.META):
        """
        Model metadata placeholder
        """
        db = EDHDatabase.NETWORK
        table_name = 'SMIStatus'
        pk = ModelPK('OptionID')
        columns = {
            'OptionID': Field('option_id'),
            'Descr': Field('description'),
            'OptionValue': Field('value'),
            'Username': Field('username'),
            'Date': Field('at')
        }

    # SQL: OptionID
    option_id: int

    # SQL: Descr
    description: str

    # SQL: OptionValue
    value: str

    # SQL: Username
    username: str

    # SQL: Date
    # TODO: implement datetime value conversion
    at: str
