from libs.grpc.paths import GRPC_CERTS_DIR
from pathlib import Path
from typing import Optional
import re


class GRPCSecurity:
    CLIENT_CERT_FILE_DEFAULT = GRPC_CERTS_DIR / "client.pem"
    CLIENT_KEY_FILE_DEFAULT = GRPC_CERTS_DIR / "client.key"
    ROOT_CERT_FILE_DEFAULT = GRPC_CERTS_DIR / "server.pem"
    VALIDATION_REGEX = r"-----BEGIN .*?-----.*?-----END .*?-----"

    def __init__(
        self,
        client_cert_path: Path = "",
        client_key_path: Path = "",
        root_cert_path: Path = "",
    ):
        self.certs_root = GRPC_CERTS_DIR

        # Create credentials using the certificate and key
        self.client_cert = self._load_and_validate_certificate(client_cert_path, self.CLIENT_CERT_FILE_DEFAULT)
        self.client_key = self._load_and_validate_certificate(client_key_path, self.CLIENT_KEY_FILE_DEFAULT)
        self.root_cert = self._load_and_validate_certificate(root_cert_path, self.ROOT_CERT_FILE_DEFAULT)

    def _validate_certificate(self, certificate_data: bytes) -> bool:
        """
        Validates the provided certificate.

        Validates if the format of the key files are valid.

        Parameters:
            certificate_data (bytes): The binary data of the certificate to be validated.

        Returns:
            bool: True if the certificate is valid, False otherwise.
        """
        block_pattern = re.compile(self.VALIDATION_REGEX, re.DOTALL)
        return bool(block_pattern.search(str(certificate_data)))

    def _load_and_validate_certificate(self, file: Optional[str] = None, default: Optional[str] = None) -> bytes:
        """
        Loads a certificate from a specified file and validates it.

        Attempts to load a certificate from the given file path. If the file path is not provided,
        it uses a default path. After loading, it validates the certificate data.

        Parameters:
            file (str): The path to the certificate file. If None, the default path is used.
            default (str): The default path to use if the 'file' parameter is None.

        Returns:
            bytes: The binary data of the loaded and validated certificate.

        Raises:
            InvalidCertificateError: If the certificate fails the pre-validation check.
        """
        file_path = file or default

        with open(file_path, "rb") as f:
            certificate_data = f.read()

        if self._validate_certificate(certificate_data):
            return certificate_data
        else:
            raise InvalidCertificateError(f"Certificate: {file_path} was rejected. Pre-validation failed.")


class InvalidCertificateError(Exception):
    pass
