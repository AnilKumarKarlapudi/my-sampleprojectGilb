import logging
from typing import Optional, Tuple

import requests

from libs.edh.network.message.models import MessageBody
from libs.infra.remote.server import RemoteServer


class NetworkMessageParseService(RemoteServer):
    """
    External network message parser service
    """

    # FIXME: this needs to be retrieve from somewhere, I suggest using a discovery service
    API_URL = "http://10.4.38.122:3000"

    def __init__(self):
        super().__init__('network-message-parser')
        self.log = logging.getLogger(NetworkMessageParseService.__name__)

    def parse_network_message_body(self,
                                   raw_message_body: str,
                                   timeout: int = 60) -> Tuple[bool, Optional[MessageBody]]:
        """
        Parse a network message body in a certain time.

        :param raw_message_body: str - raw message body
        :param timeout: int - timeout
        :return: Tuple[bool, Optional[EDHMessageBody]] - first element is the ok flag, second is the parsed message or
        an error message
        """
        try:
            url = "/".join([self.address, "parser/"])
            response = requests.post(url, data=raw_message_body.strip(), timeout=timeout)
            self.log.debug(f"HTTP {response.request.method} {response.request.url} {response.status_code}\n"
                           f"{response.request.headers}\n\n"
                           f"{response.request.body}")
            if response.ok:
                return True, response.json()
            else:
                self.log.error(f"An error has occurred requesting service: {response.text}")
                return False, "unknown error"

        except requests.exceptions.RequestException:
            return False, "unable to execute request"

        except ValueError:
            return False, "unable to parse JSON response"
