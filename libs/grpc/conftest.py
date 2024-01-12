import pytest
from libs.grpc.connector.security.main import GRPCSecurity


@pytest.fixture
def grpc_security_default():
    return GRPCSecurity()
