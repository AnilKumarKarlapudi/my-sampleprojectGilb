import pytest


@pytest.mark.internal
def test_valid_pem_content(grpc_security_default):
    pem_content = """
    -----BEGIN PRIVATE KEY-----
    Valid private key content
    -----END PRIVATE KEY-----
    """
    result = grpc_security_default._validate_certificate(pem_content)
    assert result is True


@pytest.mark.internal
def test_valid_key_content(grpc_security_default):
    key_content = """
    -----BEGIN PUBLIC KEY-----
    Valid public key content
    -----END PUBLIC KEY-----
    """
    result = grpc_security_default._validate_certificate(key_content)
    assert result is True


@pytest.mark.internal
def test_invalid_content(grpc_security_default):
    invalid_content = "This is not a valid .pem or .key content."

    result = grpc_security_default._validate_certificate(invalid_content)
    assert result is False


@pytest.mark.internal
def test_empty_content(grpc_security_default):
    empty_content = ""

    result = grpc_security_default._validate_certificate(empty_content)
    assert result is False
