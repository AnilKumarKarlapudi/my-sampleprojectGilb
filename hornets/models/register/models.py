from libs.common.fields import Field, EnumeratedField
from libs.common.template_model import TemplateModel
from libs.grpc.resources.compiled_protos import Register_pb2 as register_pb2

from hornets.models.register.enums import RegisterType


class Register(TemplateModel):
    DEFAULT_GROUP_ID = 1
    DEFAULT_MACHINE_NAME = "POSSERVER01"
    DEFAULT_REGISTER_TYPE = RegisterType.CASHIER_WORKSTATION
    DEFAULT_PRINTER_IP = "127.0.0.1"

    id: int
    group_id: int = DEFAULT_GROUP_ID
    machine_name: str = DEFAULT_MACHINE_NAME
    register_type: RegisterType = DEFAULT_REGISTER_TYPE
    model_number: str
    serial_number: str
    asset_id: str
    line_display_type: int
    printer_ip_address: str = DEFAULT_PRINTER_IP
    signature_capture_enabled: bool = False
    forward_outside_transactions: bool = False

    class META(TemplateModel.META):
        resource = "grpc"
        pk_field = "RegisterId"
        target_message = register_pb2.Register

        mapping = {
            "id": Field(
                target_field="RegisterId",
                domain_type=int,
                target_type=int
            ),
            "group_id": Field(
                target_field="RegisterGroupId",
                domain_type=int,
                target_type=int
            ),
            "machine_name": Field(
                target_field="MachineName",
                domain_type=str,
                target_type=str
            ),
            "register_type": EnumeratedField(
                target_field="Type",
                enumerated=RegisterType
            ),
            "model_number": Field(
                target_field="ModelNumber",
                domain_type=str,
                target_type=str
            ),
            "serial_number": Field(
                target_field="SerialNumber",
                domain_type=str,
                target_type=str
            ),
            "asset_id": Field(
                target_field="AssetId",
                domain_type=str,
                target_type=str
            ),
            "line_display_type": Field(
                target_field="LineDisplayType",
                domain_type=int,
                target_type=int
            ),
            "printer_ip_address": Field(
                target_field="PrinterIpAddress",
                domain_type=str,
                target_type=str
            ),
            "signature_capture_enabled": Field(
                target_field="SignatureCaptureEnabled",
                domain_type=bool,
                target_type=bool
            ),
            "forward_outside_transactions": Field(
                target_field="ForwardOutsideTransactions",
                domain_type=bool,
                target_type=bool
            ),
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
