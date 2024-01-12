import pytest
from libs.common.fixtures.models import ExampleEnum


@pytest.mark.internal
def test_interface_enum_backend(basic_interface_enum):
    assert basic_interface_enum.UNKNOWN.backend == 0
    assert basic_interface_enum.TWO.backend == 2


@pytest.mark.internal
def test_interface_enum_frontend(basic_interface_enum):
    assert basic_interface_enum.ONE.frontend == "ONE"
    assert basic_interface_enum.TWO.frontend == "TWO"


@pytest.mark.internal
@pytest.mark.parametrize(
    "value, expected",
    [
        (ExampleEnum.ONE.backend, ExampleEnum.ONE),
        (ExampleEnum.TWO.backend, ExampleEnum.TWO),
        (9999, ExampleEnum.UNKNOWN),
        (99999999, ExampleEnum.UNKNOWN),
        (9898989899, ExampleEnum.UNKNOWN),
    ],
)
def test_from_value(basic_interface_enum, value, expected):
    assert basic_interface_enum.from_value(value) == expected
