from pydantic import BaseModel, ConfigDict
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from libs.common.enums import InterfaceEnum
from libs.common.template_model import TemplateModel
from libs.common.fields import Field, MoneyField, TimestampField, EnumeratedField, ComposeField
from typing import Optional


class ExampleEnum(InterfaceEnum):
    UNKNOWN = (0, "UNKNOWN")
    ONE = (1, "ONE")
    TWO = (2, "TWO")


class ExampleMoney(BaseModel):
    currency_code: str
    units: int
    nanos: int


class ExampleMessage(BaseModel):
    target_id: int
    target_field1: int
    target_field2: int
    amount_target: ExampleMoney
    enum_target: int
    ts_target: Timestamp

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )  # This is required to avoid problems with custom types (Timestamp)


class ExampleDomain(TemplateModel):
    id: Optional[int] = -1
    field1: int
    field2: int
    amount: float
    example_enum: InterfaceEnum
    example_timestamp: datetime

    class META(TemplateModel.META):
        from libs.common.fixtures.models import ExampleMoney

        resource = "grpc"
        pk_field = "id"
        target_message = ExampleMessage
        mapping = {
            "id": Field(target_field="target_id", domain_type=int, target_type=int),
            "field1": Field(target_field="target_field1", domain_type=int, target_type=int),
            "field2": Field(target_field="target_field2", domain_type=int, target_type=int),
            "amount": MoneyField(target_field="amount_target", money_class=ExampleMoney),
            "example_enum": EnumeratedField(target_field="enum_target", enumerated=ExampleEnum),
            "example_timestamp": TimestampField(target_field="ts_target"),
        }


class ExampleComponentMessage(TemplateModel):
    target_id: Optional[int] = -1
    target_field1: int
    target_field2: int


class ExampleComponent(TemplateModel):
    id: Optional[int] = -1
    a: int
    b: int

    class META(TemplateModel.META):
        from libs.common.fixtures.models import ExampleMoney

        resource = "grpc"
        pk_field = "id"
        target_message = ExampleComponentMessage
        mapping = {
            "id": Field(target_field="target_id", domain_type=int, target_type=int),
            "a": Field(target_field="target_field1", domain_type=int, target_type=int),
            "b": Field(target_field="target_field2", domain_type=int, target_type=int),
        }


class ExampleComposeMessage(TemplateModel):
    target_id: Optional[int] = -1
    target_field1: int
    target_field2: ExampleComponentMessage


class ExampleCompose(TemplateModel):
    id: Optional[int] = -1
    a: int
    component: ExampleComponent

    class META(TemplateModel.META):
        from libs.common.fixtures.models import ExampleMoney

        resource = "grpc"
        pk_field = "id"
        target_message = ExampleComposeMessage
        mapping = {
            "id": Field(target_field="target_id", domain_type=int, target_type=int),
            "a": Field(target_field="target_field1", domain_type=int, target_type=int),
            "component": ComposeField(target_field="target_field2", model=ExampleComponent),
        }
