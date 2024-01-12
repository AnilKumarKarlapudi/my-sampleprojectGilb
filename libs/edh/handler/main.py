from libs.edh.common.constants import EDHDatasourceProperties
from libs.edh.common.constants import EDH_DATASOURCE_SERVER
from libs.edh.common.enums import EDHBrands
from libs.edh.common.enums import EDHDatabase
from libs.edh.common.enums import EDHPspID
from libs.edh.common.exceptions import EDHTaskError
from libs.edh.network.message.handler.concord import ConcordNetworkHandler
from libs.edh.network.message.handler.generic import GenericNetworkHandler
from libs.edh.network.message.handler.rbs import RBSNetworkHandler
from libs.infra.db.command import SQLCommand
from libs.infra.io.command import CommandWithCredentials
from libs.infra.io.system import platform
from libs.infra.io.system.constants import RegisterKeys
from libs.infra.io.system.user import SystemUser


class EDHMainHandler(object):
    EPS_DASHBOARD_EXECUTABLE = "C:\\Passport\\System\\Bin\\EPSDashboard.exe"

    @staticmethod
    def wrap_sqlcmd_shell(cmd: str) -> str:
        """
        Wraps SQL CMD shell command
        """
        return f"sqlcmd.exe -S passporteps -l 50 -E -Q \"xp_cmdshell\" \'{cmd}\'"

    def __init__(self):
        # EDH Datasource properties
        self._ds_props = EDHDatasourceProperties.with_database(EDHDatabase.NETWORK)

        # Default user
        self._users = {
            'default': SystemUser(),
            'edh': SystemUser(username='EDH', password='EDH')
        }

        # System brand
        self._brand = EDHBrands.of(platform.get_brand())

        # System Network
        self._network = GenericNetworkHandler(self._brand)

    def is_online(self) -> bool:
        """
        Check if EDH is online
        """
        return CommandWithCredentials("ping passporteps -w 500 -n 1", self._users['default']).run().ok

    def setup(self):
        """
        Setup fake car drawer, printer and enables the car wash.
        """
        self._enable_car_wash()

        cmd = (
            f"reg add HKEY_LOCAL_MACHINE\\{RegisterKeys.CRIND}\\Download "
            "/v SecurePromptAlternateContent /t REG_SZ "
            "/d True "
            "/f"
        )
        command = CommandWithCredentials(self.wrap_sqlcmd_shell(cmd), self._users['edh'])
        result = command.run()

        if not result.ok:
            raise EDHTaskError('setup', result.error)

    def restart(self):
        """
        Restart the EDH
        """
        cmd = f"{self.EPS_DASHBOARD_EXECUTABLE} HIDE_GUI RESTART_EPS"
        command = CommandWithCredentials(cmd, self._users['default'])
        result = command.run()

        if not result.ok:
            raise EDHTaskError('restart', result.error)

    def enable_security(self, security_type: str = "local"):
        """
        Hardens EDH for performing credit and debit sales.
        """
        if security_type.lower() == 'local':
            query = "UPDATE SMIStatus SET OptionValue = '1' WHERE OptionID = '0'"
        else:
            query = "INSERT INTO EncryptionConfig (ConfigID, value) VALUES (6, 1)"

        command = SQLCommand(query, self._ds_props)
        if not command.execute():
            raise EDHTaskError('enable_security', f'unable to execute query: {query}')

    def kill(self, process_name: str = None):
        """
        Kill a process in the EDH, if not process is provided it will kill the primary network process.
        """
        if not process_name:
            if EDHPspID.is_concord(self._brand.psp_id):
                process_name = "concordnetwork.exe"

            elif EDHBrands.WORLDPAY.name == self._brand.name:
                process_name = "RBSNetwork.exe"

            else:
                # Brand is not supported to kill self process
                raise EDHTaskError('kill', f'unsupported brand: {self._brand.psp_id} - {self._brand.name}')

        # EDH user with domain = 'passporteps'
        user = self._users['edh'].model_copy()
        user.domain = EDH_DATASOURCE_SERVER

        command = CommandWithCredentials(self.wrap_sqlcmd_shell(f"taskkill /im {process_name} /F"), user)
        result = command.run()

        if not result.ok:
            raise EDHTaskError('kill', result.error)

    def collect_logs(self):
        """
        Collects EDH logs and transfers them to the MWS
        """
        cmd = f"{self.EPS_DASHBOARD_EXECUTABLE} HIDE_GUI COLLECTLOGS"
        command = CommandWithCredentials(cmd, self._users['default'])
        result = command.run()
        if not result.ok:
            raise EDHTaskError('collect_logs', result.error)

    def _enable_car_wash(self):
        """
        Enable car wash controller simulator
        """
        cmd = (
            f"reg add HKEY_LOCAL_MACHINE\\{RegisterKeys.CAR_WASH}\\RykoServiceObject "
            "/v Simulator /t REG_DWORD "
            "/d 1 /f"
        )
        command = CommandWithCredentials(self.wrap_sqlcmd_shell(cmd), self._users['edh'])
        result = command.run()

        if not result.ok:
            raise EDHTaskError('enable_car_wash', result.error)

    def init_network(self):
        """
        Update EDH database to configure network parameters that allow connectivity with the host.
        """
        if EDHPspID.is_concord(self._brand.psp_id):
            self._network = ConcordNetworkHandler()

        elif EDHPspID.WORLDPAY == self._brand.psp_id:
            self._network = RBSNetworkHandler()

        if self._network.init():
            # Restart/Kill process only if the network has initialized for the first time
            # NOTE: I think this should be a restart...
            self.kill()
