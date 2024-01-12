import datetime
import random

import requests

from libs.infra.remote import resolvers
from libs.infra.remote.models import Service, Instance


class RemoteServer(object):
    """
    Remote Server base class
    """
    def __init__(self, name: str):
        """
        Constructor

        :param name: remote server name identifier, must exist in the database configured on the startup.
        """
        try:
            self._service = Service.get_by_id(name)
            self._instances = Instance.select().join(Service).where(Service.name == name).execute()
        except Service.DoesNotExist:
            raise ValueError("Given name does not exist or it's not configured yet. ")

        # Public http session
        self.session = requests.Session()

    @property
    def address(self) -> str:
        """
        Get the server instance address.

        :raises IndexError: if no instance is enabled
        :return: remote server instance address
        """
        # Instances must be checked every 5 minutes (300 seconds)
        elapsed = datetime.datetime.now() - self._service.last_update_at
        if elapsed > datetime.timedelta(seconds=300):
            for instance in self._instances:
                instance.enabled = resolvers.check_instance(instance)
                instance.save()
            self._service.last_update_at = datetime.datetime.now()
            self._service.save()

        # Get a random instance which is enabled
        return random.choice([instance.generate() for instance in self._instances if instance.enabled])
