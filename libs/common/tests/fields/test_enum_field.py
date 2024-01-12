import pytest
from libs.common.fixtures.models import ExampleEnum


@pytest.mark.internal
@pytest.mark.parametrize(
    "value, expected_encoded",
    [
        (ExampleEnum.ONE, 1),
        (ExampleEnum.TWO, 2),
        (ExampleEnum.UNKNOWN, 0),
    ],
)
def test_enumerated_field_encoding_decoding(value, expected_encoded, example_enum_field):
    field = example_enum_field

    # Encoding test
    encoded_value = field.encode(value)
    assert encoded_value == value.backend

    # Decoding test
    decoded_value = field.decode(expected_encoded)
    assert decoded_value == value


@pytest.mark.internal
def test_enumerated_field_with_edge_cases(example_enum_field):
    field = example_enum_field

    # Test encoding and decoding with None
    with pytest.raises(TypeError):
        encoded_none = field.encode(None)
        assert encoded_none is None

    decoded_none = field.decode(None)
    assert decoded_none == ExampleEnum.UNKNOWN

    # Test decoding with an invalid enum value
    decoded_invalid_value = field.decode(999)
    assert decoded_invalid_value == ExampleEnum.UNKNOWN
