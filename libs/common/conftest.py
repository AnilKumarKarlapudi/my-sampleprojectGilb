import pytest

from datetime import datetime

from google.protobuf.timestamp_pb2 import Timestamp
from libs.common.fixtures.models import (
    ExampleDomain,
    ExampleMessage,
    ExampleEnum,
    ExampleMoney,
    ExampleComponent,
    ExampleCompose,
    ExampleComponentMessage,
    ExampleComposeMessage,
)
from libs.common.fields import EnumeratedField, MoneyField, TimestampField


@pytest.fixture
def basic_interface_enum():
    return ExampleEnum


@pytest.fixture
def base_datetime():
    return datetime(2023, 1, 1, 12, 0, 0)


@pytest.fixture
def base_datetime_epoch(base_datetime):
    return int(base_datetime.timestamp())


@pytest.fixture
def grpc_timestamp(base_datetime_epoch):
    timestamp = Timestamp()
    timestamp.seconds = base_datetime_epoch
    timestamp.nanos = 0
    return timestamp


@pytest.fixture
def example_money():
    return ExampleMoney(currency_code="USD", units=2, nanos=0)


@pytest.fixture
def example_message_model(grpc_timestamp, basic_interface_enum, example_money):
    return ExampleMessage(
        target_id=82,
        target_field1=1,
        target_field2=2,
        enum_target=basic_interface_enum.ONE.backend,
        ts_target=grpc_timestamp,
        amount_target=example_money,
    )


@pytest.fixture
def example_domain_component():
    return ExampleComponent(id=81, a=1, b=2)


@pytest.fixture
def example_domain_composed(example_domain_component):
    return ExampleCompose(id=82, a=3, component=example_domain_component)


@pytest.fixture
def example_message_component():
    return ExampleComponentMessage(target_id=81, target_field1=1, target_field2=2)


@pytest.fixture
def example_message_composed(example_message_component):
    return ExampleComposeMessage(target_id=82, target_field1=3, target_field2=example_message_component)


@pytest.fixture
def example_domain_model(base_datetime, basic_interface_enum):
    return ExampleDomain(
        id=82, field1=1, field2=2, example_enum=basic_interface_enum.ONE, example_timestamp=base_datetime, amount=2.0
    )


@pytest.fixture
def example_enum_field():
    return EnumeratedField(target_field="test_field", enumerated=ExampleEnum)


@pytest.fixture
def example_money_field(example_money):
    return MoneyField(target_field="test_field", money_class=example_money.__class__)


@pytest.fixture
def example_timestamp_field():
    return TimestampField(target_field="test_field")
