import pytest


@pytest.mark.internal
def test_timestamp_field_encoding_decoding(base_datetime, grpc_timestamp, example_timestamp_field):
    field = example_timestamp_field

    # Encoding test
    encoded_value = field.encode(base_datetime)
    assert encoded_value == grpc_timestamp

    # Decoding test
    decoded_value = field.decode(grpc_timestamp)
    assert decoded_value == base_datetime


@pytest.mark.internal
def test_timestamp_field_encoding_decoding_with_none(example_timestamp_field):
    field = example_timestamp_field

    # Encoding test with None
    with pytest.raises(TypeError):
        field.encode(None)

    # Decoding test with None
    with pytest.raises(TypeError):
        field.decode(None)


@pytest.mark.internal
@pytest.mark.parametrize("invalid_value", ["char", 42, 3.14, "invalid_timestamp"])
def test_decode_invalid_timestamp(example_timestamp_field, invalid_value):
    field = example_timestamp_field

    with pytest.raises(TypeError):
        # Decoding test with an invalid timestamp
        field.decode(invalid_value)
