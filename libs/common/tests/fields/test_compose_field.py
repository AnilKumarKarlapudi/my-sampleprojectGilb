from libs.common.fixtures.models import (
    ExampleComponentMessage,
    ExampleComposeMessage,
    ExampleComponent,
    ExampleCompose,
)
import pytest


@pytest.mark.internal
def test_component_field_encoding_decoding(example_domain_component):
    encoded_value = example_domain_component.encode()

    assert isinstance(encoded_value, ExampleComponentMessage)

    decoded_value = example_domain_component.decode(encoded_value)

    assert isinstance(decoded_value, ExampleComponent)


@pytest.mark.internal
def test_compose_field_encoding_decoding(example_domain_composed):
    # Encoding test
    encoded_value = example_domain_composed.encode()

    assert isinstance(encoded_value, ExampleComposeMessage)
    assert isinstance(encoded_value.target_field2, ExampleComponentMessage)

    decoded_value = example_domain_composed.decode(encoded_value)

    assert isinstance(decoded_value, ExampleCompose)
    assert isinstance(decoded_value.component, ExampleComponent)
