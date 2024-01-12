import pytest

from google.protobuf.timestamp_pb2 import Timestamp
from libs.grpc.resources.compiled_protos import Pricebook_pb2 as pricebook_pb2
from libs.grpc.resources.compiled_protos import money_pb2


@pytest.fixture
def discount_message():
    return pricebook_pb2.Discount(
        discount_id=1,
        description="Sample Discount",
        discount_method=1,
        value=money_pb2.Money(currency_code="USD", units=2, nanos=0),
        begin_date=Timestamp(seconds=1643203200),  # Timestamp for 2022-01-28 00:00:00 UTC
        end_date=Timestamp(seconds=1643548800),  # Timestamp for 2022-02-01 00:00:00 UTC
        promotion_reason_id=1,
    )


@pytest.fixture
def manual_discount_message(discount_message):
    return pricebook_pb2.ManualDiscount(
        Values=[
            discount_message,
        ]
    )
