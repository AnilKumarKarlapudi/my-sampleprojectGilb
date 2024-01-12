import pytest
from libs.common.fields import ListField, Field, EnumeratedField
from libs.common.fixtures.models import ExampleEnum


@pytest.fixture
def example_int_field():
    return Field(domain_type=int, target_type=int)


@pytest.fixture
def example_list_field(example_int_field):
    return ListField(element_field=example_int_field)


@pytest.mark.internal
def test_list_field_empty(example_list_field):
    encoded_value = example_list_field.encode([])
    assert encoded_value == []

    decoded_value = example_list_field.decode([])
    assert decoded_value == []


@pytest.mark.internal
@pytest.mark.parametrize(
    "input_list, expected_encoded, element_field",
    [
        ([1, 2, 3], [1, 2, 3], Field(domain_type=int, target_type=int)),
        (["a", "b", "c"], ["a", "b", "c"], Field(domain_type=str, target_type=str)),
        ([1.2, 2.2, 3.5], [1.2, 2.2, 3.5], Field(domain_type=float, target_type=float)),
    ],
)
def test_list_field_valid_elements(input_list, expected_encoded, element_field):
    list_field = ListField(element_field=element_field)

    encoded_value = list_field.encode(input_list)
    assert encoded_value == expected_encoded

    decoded_value = list_field.decode(expected_encoded)
    assert decoded_value == input_list


# TODO
# Add more cases with different fields
@pytest.mark.internal
@pytest.mark.parametrize(
    "input_list, element_fields, expected_encoded",
    [
        (
            [
                ExampleEnum.ONE,  # Replace with actual enumerated values
                ExampleEnum.TWO,
            ],
            EnumeratedField(enumerated=ExampleEnum),
            [1, 2],  # Replace with actual backend values corresponding to the enumerated values
        ),
    ],
)
def test_list_field_with_nested_fields(input_list, element_fields, expected_encoded):
    list_field = ListField(element_field=element_fields)

    encoded_value = list_field.encode(input_list)
    assert encoded_value == expected_encoded

    decoded_value = list_field.decode(expected_encoded)
    assert decoded_value == input_list
