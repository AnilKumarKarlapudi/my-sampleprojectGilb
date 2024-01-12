from http import HTTPStatus
import json
import logging
from typing import Optional

import requests

from libs.simulators_interface.enums import SimulatorResource

log = logging.getLogger("basesim")

# Disable logging for HTTP Requests
urllib_logger = logging.getLogger('urllib3.connectionpool')
urllib_logger.propagate = False
requests_logger = logging.getLogger("requests")
requests_logger.propagate = False


# Simulator Parent Class
class Simulator(object):
    def __init__(self, resource: SimulatorResource, ip: Optional[str] = None):
        """
        Initializes the PinPad class.
        Args:
            resource : (SimulatorResource) The resource endpoint for simulator.
            ip : (str) The simulator ip. If it's None it will get it from settings.
        """
        if not ip:
            ip = "10.5.50.5"  # TODO: Get default from environment variables
        self.url = f"http://{ip}/{resource.value}"
        self.session = requests.Session()

    def get(self, resource, timeout=30):
        full_url = self.url + resource
        try:
            # log.debug(f"Sending GET request: {full_url}")
            get_request = self.session.get(full_url, timeout=timeout)
            if get_request.status_code == HTTPStatus.OK:
                payload = {
                    "success": True,
                    "payload": json.loads(get_request.text)
                }
                return payload
            else:
                payload = {
                    "success": False,
                    "payload": f"Error. Received status code of {get_request.status_code}"
                }
                return payload
        except Exception as e:
            log.warning("Failed attempting to do a get request to: " + full_url)
            log.warning(e)
            payload = {
                "success": False,
                "payload": "Error"  # TODO : Need to be more specific.
            }
            return payload

    def post(self, resource, data, dotnet_server=True, timeout=30):
        full_url = self.url + resource
        log.debug(f"Sending POST request: {full_url} with data {data}")
        try:
            if dotnet_server:
                # TODO: Line removed because set running mode was not working
                data = json.dumps(data)  # DOTNET is expecting JSON str object
                post_request = self.session.post(
                    full_url,
                    data=json.dumps(data),  # If I leave this as just `data`, it returns 500 status code.
                    headers={'content-type': 'application/json'},  # If left out, this will throw a 415 status code.
                    timeout=timeout
                )
            else:
                post_request = self.session.post(
                    full_url,
                    data=data,
                    timeout=timeout
                )

            if post_request.status_code in [HTTPStatus.CREATED, HTTPStatus.OK]:
                payload = {
                    "success": True,
                    "payload": json.loads(post_request.text)
                }
                if logging:
                    log.debug(f"{payload} was returned from {self.url}")
                return payload
            else:
                payload = {
                    "success": False,
                    "payload": f"Error. Received status code of {post_request.status_code}"
                }
                if logging:
                    log.debug(f"{payload} was returned from {self.url}")
                return payload

        except Exception as e:
            log.warning("Failed attempting to do a get request to: " + full_url)
            log.warning(e)
            payload = {
                "success": False,
                "payload": "Error"  # TODO : Need to be more specific.
            }
            return payload

    def delete(self, resource, data, dotnet_server=True, timeout=30):
        full_url = self.url + resource
        log.debug(f"Sending DELETE request: {full_url} with data {data}")

        try:
            if dotnet_server:
                data = json.dumps(data)  # DOTNET is expecting JSON str object
                delete_request = self.session.delete(
                    full_url,
                    data=json.dumps(data),  # If I leave this as just `data`, it returns 500 status code.
                    headers={'content-type': 'application/json'},  # If left out, this will throw a 415 status code.
                    timeout=timeout
                )
            else:
                delete_request = self.session.delete(
                    full_url,
                    data=data,
                    timeout=timeout
                )

            if delete_request.status_code in [HTTPStatus.CREATED, HTTPStatus.OK]:
                payload = {
                    "success": True,
                    "payload": json.loads(delete_request.text)
                }
                if logging:
                    log.debug(f"{payload} was returned from {self.url}")
                return payload
            else:
                payload = {
                    "success": False,
                    "payload": f"Error. Received status code of {delete_request.status_code}"
                }
                if logging:
                    log.debug(f"{payload} was returned from {self.url}")
                return payload

        except Exception as e:
            log.warning("Failed attempting to do a get request to: " + full_url)
            log.warning(e)
            payload = {
                "success": False,
                "payload": "Error"  # TODO : Need to be more specific.
            }
            return payload
