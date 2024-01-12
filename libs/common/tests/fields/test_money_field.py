import pytest
from libs.common.utils import compare_instances


@pytest.mark.internal
def test_money_field_content_encoding_format(example_money, example_money_field):
    field = example_money_field

    # Encoding test
    encoded_value = field.encode(2)
    assert compare_instances(example_money, encoded_value)

    # Decoding
    decoded_value = field.decode(encoded_value)
    assert decoded_value == 2


@pytest.mark.internal
@pytest.mark.parametrize(
    "value, expected_units, expected_nanos",
    [
        (2, 2, 0),
        (1.75, 1, 750000000),
        (1.7564, 1, 756400000),
        (-1, -1, 0),
        (-1.75, -1, -750000000),
        (-1.7564, -1, -756400000),
        (100, 100, 0),
        (1000, 1000, 0),
        (193.471, 193, 471000000),
    ],
)
def test_money_field_encoding(value, expected_units, expected_nanos, example_money, example_money_field):
    field = example_money_field

    # Encoding test
    encoded_value = field.encode(value)

    # Assert expected units and nanos
    assert encoded_value.units == expected_units
    assert encoded_value.nanos == expected_nanos

    # Decoding
    decoded_value = field.decode(encoded_value)
    assert decoded_value == value


@pytest.mark.internal
def test_money_field_encoding_char(example_money_field):
    field = example_money_field

    with pytest.raises(TypeError):
        field.encode("a")


@pytest.mark.internal
def test_money_field_encoding_with_zero(example_money, example_money_field):
    field = example_money_field

    # Encoding test
    encoded_value = field.encode(0)
    assert encoded_value.units == 0
    assert encoded_value.nanos == 0

    # Decoding
    decoded_value = field.decode(encoded_value)
    assert decoded_value == 0


@pytest.mark.internal
def test_money_field_encoding_with_negative_zero(example_money, example_money_field):
    field = example_money_field

    # Encoding test
    encoded_value = field.encode(-0)
    assert encoded_value.units == 0
    assert encoded_value.nanos == 0

    # Decoding
    decoded_value = field.decode(encoded_value)
    assert decoded_value == 0
