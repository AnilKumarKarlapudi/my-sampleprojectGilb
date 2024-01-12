from collections import namedtuple

from libs.infra.io.system.user import SystemUser

# SQLRecord structure
SQLRecord = namedtuple("SQLRecord", ["columns", "record"])

# Model Primary Key structure
ModelPK = namedtuple("ModelPK", ["field"])

# Field structure
Field = namedtuple("Field", ["name"])


# @wither(['database'])
class DatasourceProperties:
    """
    Datasource properties
    """

    server: str  # required
    database: str  # required
    user: SystemUser  # required

    def with_database(self, database: str) -> "DatasourceProperties":
        """
        Overrides database attr for properties.

        :param database: str - new database
        :returns: DatasourceProperties - object with new database overridden
        """
        self.database = database
        return self
