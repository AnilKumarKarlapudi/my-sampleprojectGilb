from libs.infra.db.handler import DatasourceHandler
from libs.infra.db.models import SQLModel
from libs.infra.db.schemas import DatasourceProperties
from libs.infra.db.schemas import Field
from libs.infra.db.schemas import ModelPK
from libs.infra.io.system.user import SystemUser

USER = SystemUser(username="PassportTech", password="911Tech", domain="passport")


class Currency(SQLModel):
    class META(SQLModel.META):
        db = "GlobalSTORE"
        table_name = "dbo.CRRNCY"
        pk = ModelPK('curr_id')
        columns = {
            'CURR_ID': Field('curr_id'),
            'CURR_DESCR': Field('description'),
            'CURR_SYM': Field('symbol')
        }

    curr_id: int
    description: str
    symbol: str


def get_ds_properties():
    properties = DatasourceProperties()
    properties.user = USER
    properties.server = "POSSERVER01"
    properties.database = "GlobalSTORE"
    return properties


def test_handler_find_ok():
    db = DatasourceHandler()
    db.model = Currency
    db.properties = get_ds_properties()
    result = db.find(1)
    assert result.symbol == "$"
