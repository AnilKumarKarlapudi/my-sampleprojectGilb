from libs.infra.db.schemas import DatasourceProperties
from libs.infra.io.system.user import SystemUser

# Constants
# Datasource
EDH_DATASOURCE_SERVER = "passporteps"
EDH_DATASOURCE_USER = "EDH"
EDH_DATASOURCE_PASSWORD = "EDH"
EDH_DATASOURCE_DOMAIN = "passport"

# EDH Datasource Properties
EDHDatasourceProperties = DatasourceProperties()
EDHDatasourceProperties.server = EDH_DATASOURCE_SERVER
EDHDatasourceProperties.user = SystemUser(
    username=EDH_DATASOURCE_USER,
    password=EDH_DATASOURCE_PASSWORD,
    domain=EDH_DATASOURCE_DOMAIN
)

# This is for network handlers...
# In the old framework this is handled with the file NetworkStandard.json, in which every value is the same...
EDH_NETWORK_UNKNOWN_ADDRESS = "1.2.3.4"
EDH_NETWORK_UNKNOWN_PORT = 8085
