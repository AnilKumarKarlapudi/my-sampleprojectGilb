from libs.common.template_model import TemplateModel
from typing import Optional
import libs.grpc.resources.compiled_protos.Register_pb2 as register_pb2
from libs.common.fields import Field


class SpeedKey(TemplateModel):
    DEFAULT_POSITION = 1

    plu: str  # PLU assigned
    caption: str
    position: Optional[int] = DEFAULT_POSITION

    class META(TemplateModel.META):
        resource = "grpc"
        pk_field = "Position"
        target_message = register_pb2.SpeedKey

        mapping = {
            "position": Field(target_field="Position", domain_type=int, target_type=int),
            "caption": Field(target_field="Caption", domain_type=str, target_type=str),
            "plu": Field(target_field="ItemIdAssigned", domain_type=str, target_type=str),
        }

    def __str__(self):
        return f"{vars(self)}"

    def __eq__(self, other):
        """
        I need to avoid having two items at the same position.
        This will help the .exists method to protect passport
        """
        if isinstance(other, self.__class__):
            return self.position == other.position
