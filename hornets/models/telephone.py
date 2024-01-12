from libs.common.fields import Field
from libs.common.template_model import TemplateModel
from libs.grpc.resources.compiled_protos import Common_pb2 as common_pb2


class Telephone(TemplateModel):
    area_code: str
    number: str

    class META(TemplateModel.META):
        resource = "grpc"
        target_message = common_pb2.Telephone

        mapping = {
            "area_code": Field(target_field="AreaCode", domain_type=str, target_type=str),
            "number": Field(target_field="PhoneNumber", domain_type=str, target_type=str),
        }
