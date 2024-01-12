import pytest
from unittest.mock import patch, mock_open
from libs.grpc.connector.security.main import GRPCSecurity


@pytest.mark.internal
def test_default_certificates(grpc_security_default):
    assert grpc_security_default.client_cert is not None
    assert grpc_security_default.client_key is not None
    assert grpc_security_default.root_cert is not None


@pytest.mark.internal
def test_empty_certificate():
    with patch("builtins.open", mock_open(read_data=b"")):
        with pytest.raises(Exception):
            GRPCSecurity(client_cert_path="path/to/invalid_certificate.pem")


@pytest.mark.internal
def test_invalid_certificate():
    with patch("builtins.open", mock_open(read_data=b"This is not a valid certificate file")):
        with pytest.raises(Exception):
            GRPCSecurity(client_cert_path="path/to/invalid_certificate.pem")
