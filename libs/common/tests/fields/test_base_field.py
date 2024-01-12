import pytest
from libs.common.fields import Field


@pytest.mark.internal
@pytest.mark.parametrize(
    "value, domain_type, target_type, expected_encoded, expected_decoded",
    [
        (42, int, str, "42", 42),
        ("hello", str, str, "hello", "hello"),
        (3.14, float, int, 3, 3.00),
        (3.14, float, float, 3.14, 3.14),
    ],
)
def test_field_encoding_decoding(value, domain_type, target_type, expected_encoded, expected_decoded):
    field = Field(target_field="test_field", domain_type=domain_type, target_type=target_type)

    # Encoding test
    encoded_value = field.encode(value)
    assert encoded_value == expected_encoded

    # Decoding test
    decoded_value = field.decode(expected_encoded)
    assert decoded_value == expected_decoded


@pytest.mark.internal
def test_field_encoding_decoding_with_none():
    field = Field(target_field="test_field", domain_type=int, target_type=int)

    # Encoding test with None
    encoded_value = field.encode(None)
    assert encoded_value is None

    # Decoding test with None
    decoded_value = field.decode(None)
    assert decoded_value is None
