from hornets.utilities.log_config import logger
from abc import ABC, abstractmethod
from pathlib import Path
import grpc
import socket

from libs.grpc.connector.security.main import GRPCSecurity


class GRPCConnector(ABC):
    @abstractmethod
    def create_channel(self, port: int) -> grpc.Channel:
        raise NotImplementedError()


class MwsGRPC(GRPCConnector):
    """
    gRPC connector implementation for MWS.
    """

    def __init__(
        self,
        client_cert_path: Path = "",
        client_key_path: Path = "",
        root_cert_path: Path = "",
        machine_name: Path = "",
    ):
        if not machine_name:
            machine_name = socket.gethostname()

        self.machine_name = machine_name

        self.auth = GRPCSecurity(
            client_cert_path=client_cert_path, client_key_path=client_key_path, root_cert_path=root_cert_path
        )

        self.credentials = grpc.ssl_channel_credentials(
            root_certificates=self.auth.root_cert,
            private_key=self.auth.client_key,
            certificate_chain=self.auth.client_cert,
        )

    def create_channel(self, port: int) -> grpc.Channel:
        """
        Creates a secure gRPC channel to the specified port using the pre-configured credentials.

        Parameters:
            port (int): The port number to connect to on the gRPC server.

        Returns:
            grpc.Channel: A secure gRPC channel to the specified server and port.

        Raises:
            ValueError: If the port is not specified or is invalid.
        """
        if not port:
            raise ValueError("The channel port should be specified.")

        try:
            channel = grpc.secure_channel(f"{self.machine_name}:{port}", self.credentials)
        except grpc.RpcError as e:
            logger.error(f"Error creating GRPC channel: {e}")
            raise Exception(f"Connection refused. {self.machine_name}:{port}")
        except Exception as e:
            raise Exception(f"Error creating GRPC channel. {self.machine_name}:{port} --> {e}")

        logger.info(f"GRPC Channel created --> {self.machine_name}:{port}")

        return channel
