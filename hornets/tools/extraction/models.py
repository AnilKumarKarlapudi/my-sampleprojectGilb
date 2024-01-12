from typing import List
from pathlib import WindowsPath
from libs.common.template_model import TemplateModel

from libs.common.fields import Field, ListField, EnumeratedField
from hornets.tools.extraction.enums import ExtractionToolSection
from libs.grpc.resources.compiled_protos import ExtractionTool_pb2 as extraction_tool_pb2


class ImportFile(TemplateModel):
    file_name: str
    directory: str

    sections: List[ExtractionToolSection]

    class META(TemplateModel.META):
        resource = "grpc"
        pk_field = "FileName"
        target_message = extraction_tool_pb2.ExtractionFile

        mapping = {
            "file_name": Field(target_field="FileName", domain_type=str, target_type=str),
            "directory": Field(target_field="Directory", domain_type=str, target_type=str),
            "sections": ListField(
                target_field="Sections",
                element_field=EnumeratedField(enumerated=ExtractionToolSection),
            ),
        }

    @property
    def path(self):
        return WindowsPath(self.directory) / self.file_name

    def __str__(self) -> str:
        return str(vars(self))


class ProgressUpdate(TemplateModel):
    success: bool
    percent: float
    message: str
    is_import: bool

    class META(TemplateModel.META):
        resource = "grpc"
        target_message = extraction_tool_pb2.ProgressUpdate

        mapping = {
            "success": Field(target_field="Success", domain_type=bool, target_type=bool),
            "percent": Field(target_field="PercentComplete", domain_type=float, target_type=float),
            "message": Field(target_field="Message", domain_type=str, target_type=str),
            "is_import": Field(target_field="IsImport", domain_type=bool, target_type=bool),
        }
