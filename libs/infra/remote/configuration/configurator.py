import datetime
import json
from typing import IO

from libs.infra.remote import resolvers
from libs.infra.remote.configuration.properties import ProviderProperties
from libs.infra.remote.configuration.properties import ServiceProperties
from libs.infra.remote.models import Instance
from libs.infra.remote.models import Service
from libs.infra.remote.persistence import get_connection


class Configurator(object):
    def __init__(self, fp_configs: IO):
        self._db = get_connection()

        self._configs = json.load(fp_configs)

        # Load provider
        self._provider = ProviderProperties.load(self._configs.get('provider'))

        # Load services
        self._services = ServiceProperties.load(self._configs['services'])

    def configure(self):
        self.start()

        for service_properties in self._services:
            service = Service.create(
                name=service_properties.name,
                healthchecker=service_properties.healthchecker,
                description=service_properties.description,
                enabled=service_properties.enabled,
                started_at=datetime.datetime.now(),
                last_update_at=None
            )
            for instance_properties in service_properties.instances:
                try:
                    instance = Instance()

                    instance.ip = resolvers.ip(instance_properties.ip, self._provider)

                    instance.port = resolvers.port(instance_properties.port, self._provider)

                    instance.hostname = resolvers.hostname(instance_properties, instance.ip)

                    instance.homepage = instance_properties.homepage

                    # Usually hosts are non-https, so the secure flag will always be False
                    instance.secure = instance_properties.secure

                    instance.service = service

                    instance.enabled = resolvers.check_instance(instance) if instance_properties.enabled else False

                    instance.identifier = instance.get_identifier()

                    instance.save(force_insert=True)

                except Exception as ex:
                    if not self._provider.ignore_errors:
                        raise ex

    def start(self):
        self._db.create_tables([Service, Instance], fail_silently=True)

    def cleanup(self):
        if len(self._db.get_tables()) != 0:
            Instance.delete().execute()
            Service.delete().execute()
