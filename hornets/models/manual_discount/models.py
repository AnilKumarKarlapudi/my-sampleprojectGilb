from hornets.models.manual_discount.enums import ManualDiscountMethod, ManualDiscountReason
from libs.common.template_model import TemplateModel
from libs.grpc.resources.compiled_protos import money_pb2
import libs.grpc.resources.compiled_protos.Pricebook_pb2 as pricebook_pb2
from libs.common.fields import Field, EnumeratedField, TimestampField, MoneyField

from datetime import datetime, timedelta
from typing import Optional


class ManualDiscount(TemplateModel):
    id: Optional[int] = -1
    name: str
    method: ManualDiscountMethod
    reason: ManualDiscountReason
    amount: float

    begin_date: Optional[datetime] = datetime.now() - timedelta(days=1)
    end_date: Optional[datetime] = datetime.now() + timedelta(days=1000)

    class META(TemplateModel.META):
        resource = "grpc"
        pk_field = "DiscountId"
        target_message = pricebook_pb2.Discount

        mapping = {
            "id": Field(target_field="DiscountId", domain_type=int, target_type=int),
            "name": Field(target_field="Description", domain_type=str, target_type=str),
            "method": EnumeratedField(target_field="DiscountMethod", enumerated=ManualDiscountMethod),
            "reason": EnumeratedField(target_field="PromotionReasonId", enumerated=ManualDiscountReason),
            "amount": MoneyField(target_field="Value", money_class=money_pb2.Money),
            "begin_date": TimestampField("BeginDate"),
            "end_date": TimestampField("EndDate"),
        }

    @property
    def discount_amount(self) -> str:
        return self.amount

    @property
    def apply_discount_to(self) -> str:
        return self.method.frontend[1]

    @property
    def discount_type(self) -> str:
        return self.method.frontend[2]
