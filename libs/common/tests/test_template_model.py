from libs.common.fixtures.models import ExampleDomain, ExampleMessage
from libs.common.utils import compare_instances
import pytest


@pytest.mark.internal
def test_successful_decoding(example_domain_model, example_message_model):
    decoded = ExampleDomain.decode(example_message_model)
    assert isinstance(decoded, ExampleDomain)
    assert compare_instances(decoded, example_domain_model)


@pytest.mark.internal
def test_successful_encoding(example_domain_model, example_message_model):
    encoded = example_domain_model.encode()
    assert isinstance(encoded, ExampleMessage)
    assert encoded.ts_target.seconds == example_domain_model.example_timestamp.timestamp()
    assert compare_instances(encoded, example_message_model)


@pytest.mark.internal
def test_encode_and_decode(example_domain_model, example_message_model):
    decoded = ExampleDomain.decode(example_message_model)
    assert compare_instances(decoded, example_domain_model)
    reencoded = decoded.encode()
    assert compare_instances(reencoded, example_message_model)


@pytest.mark.internal
def test_decoding_same_type_raises_error(example_domain_model):
    with pytest.raises(TypeError):
        ExampleDomain.decode(example_domain_model)
