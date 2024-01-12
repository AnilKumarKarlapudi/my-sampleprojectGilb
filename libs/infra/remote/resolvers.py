import logging
import socket

import requests
from pythonping import ping
from pythonping.executor import SuccessOn

from libs.infra.remote.configuration.properties import InstanceProperties
from libs.infra.remote.configuration.properties import IpProperties
from libs.infra.remote.configuration.properties import PortProperties
from libs.infra.remote.configuration.properties import ProviderProperties
from libs.infra.remote.errors import CannotBeResolvedError
from libs.infra.remote.errors import MissingResolverError
from libs.infra.remote.errors import SkipConfiguration
from libs.infra.remote.errors import UnrecognizedConfigurationError
from libs.infra.remote.models import Instance

DEFAULT_PORT = 80

# Logger
log = logging.getLogger('infra.addresses.resolvers')


def ip(ip_properties: IpProperties, provider: ProviderProperties) -> str:
    """
    Resolves an ip by using the AutomationAgentDashboard (if it's needed, otherwise, use static info).

    :param ip_properties: IP Properties configuration
    :param provider: Provider Properties configuration
    :return: instance ip from configuration
    :raises MissingResolverError: on missing provider
    :raises CannotBeResolvedError: on an error when resolving
    :raises UnrecognizedConfigurationError: on configuration type unrecognized
    :raises SkipConfiguration: on provider disabled
    """
    if ip_properties.type == 'static':
        return ip_properties.value

    elif ip_properties.type == 'resolver':
        if not provider:
            raise MissingResolverError()

        if provider.enabled:
            try:
                response = requests.get(f"{provider.url}/{ip_properties.value}")
                response.raise_for_status()
                return response.text
            except (requests.HTTPError, requests.RequestException) as ex:
                raise CannotBeResolvedError("ip") from ex
        else:
            raise SkipConfiguration()

    raise UnrecognizedConfigurationError(ip_properties.type)


def port(port_properties: PortProperties, provider: ProviderProperties) -> int:
    """
    Resolves the instance port using the AutomationAgentDashboard (if it's needed, otherwise, use static info).

    :param port_properties: Port Properties configuration
    :param provider: Provider Properties configuration
    :return: instance port resolved
    :raises ValueError: on port value not being an integer
    :raises CannotBeResolvedError: on error when resolving
    :raises UnrecognizedConfigurationError: on properties configuration unexpected
    """
    if port_properties.type == 'static':
        if isinstance(port_properties.value, str):
            return int(port_properties.value)
        return port_properties.value

    elif port_properties.type == 'resolver':
        if not provider.enabled:
            return DEFAULT_PORT
        if isinstance(port_properties.value, int):
            raise ValueError("'value' parameter must be an URI not an int")
        try:
            response = requests.get(f"{provider.url}/{port_properties.value}")
            response.raise_for_status()

            if port_properties.attr:
                return int(response.json()[port_properties.attr])
            else:
                return int(response.text.strip())

        except (requests.HTTPError, requests.RequestException, ValueError) as ex:
            raise CannotBeResolvedError('port') from ex

    raise UnrecognizedConfigurationError(port_properties.type)


def hostname(instance_properties: InstanceProperties, host_ip: str = None) -> str:
    """
    Resolve hostname from Instance Properties configuration.

    :param instance_properties: Instance Properties configuration
    :param host_ip: static host ip
    :return: hostname
    :raises ValueError: on host_ip is None if instance properties does not have hostname
    """
    if instance_properties.hostname:
        return instance_properties.hostname
    else:
        if host_ip is None:
            raise ValueError("expecting parameter 'host_ip' to be a string")
        try:
            return socket.gethostbyaddr(host_ip)[0]
        except socket.herror:
            return host_ip


def check_instance(instance: Instance) -> bool:
    """
    Check instance

    :param instance:
    :return:
    """
    healthchecker = instance.service.healthchecker

    if healthchecker == '@ping':
        check = ping(instance.ip)
        return check.success(SuccessOn.Most)

    else:
        url = instance.generate()
        url += healthchecker if healthchecker.startswith('/') else f"/{healthchecker}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.ok
        except (requests.HTTPError, requests.RequestException):
            return False
