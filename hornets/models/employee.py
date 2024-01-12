from datetime import datetime
from libs.common.template_model import TemplateModel
from libs.common.fields import Field, TimestampField, ComposeField
from libs.grpc.resources.compiled_protos import Employee_pb2 as employee_pb2
from hornets.models.telephone import Telephone


class Employee(TemplateModel):
    id: str
    first_name: str
    last_name: str
    date_of_birth: datetime
    telephone: Telephone
    active: bool
    clock_in_out_required: bool
    security_group: int
    override_blind_balancing: bool
    blind_balancing_enabled: bool

    class META(TemplateModel.META):
        resource = "grpc"
        pk_field = "EmployeeId"
        target_message = employee_pb2.Employee

        mapping = {
            "id": Field(target_field="EmployeeId", domain_type=str, target_type=str),
            "first_name": Field(target_field="FirstName", domain_type=str, target_type=str),
            "last_name": Field(target_field="LastName", domain_type=str, target_type=str),
            "date_of_birth": TimestampField("DateOfBirth"),
            "telephone": ComposeField(target_field="Telephone", model=Telephone),
            "active": Field(target_field="Active", domain_type=bool, target_type=bool),
            "clock_in_out_required": Field(target_field="ClockInOutRequired", domain_type=bool, target_type=bool),
            "security_group": Field(target_field="SecurityGroupId", domain_type=int, target_type=int),
            "override_blind_balancing": Field(
                target_field="OverrideBlindBalancing", domain_type=bool, target_type=bool
            ),
            "blind_balancing_enabled": Field(target_field="BlindBalancingEnabled", domain_type=bool, target_type=bool),
        }

    def __str__(self):
        return f"{vars(self)}"

    def __eq__(self, other):
        """
        Two employees are the same if they have the same id.
        It doesn't compare the rest of the data fields
        """
        if not isinstance(other, self.__class__):
            raise TypeError(f"Cannot compare {self.__class__} with {other.__class__}")

        return self.id == other.id
