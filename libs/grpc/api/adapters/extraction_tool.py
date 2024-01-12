from libs.grpc.resources.compiled_protos import ExtractionTool_pb2 as extraction_tool_pb2
from libs.grpc.resources.compiled_protos import Common_pb2
from libs.grpc.api.adapters.base import DomainAdapter
from typing import NewType, Any

ImportFile = NewType("ImportFile", Any)


class ExtractionToolAdapter(DomainAdapter):
    """
    Adapter for encoding/decoding ImportFile into ExtractionConfigurationRequest message.

    Attributes:
        DEFAULT_EMPLOYEE (str): Default employee ID.
    """

    DEFAULT_EMPLOYEE = "91"

    def encode(
        self, file: ImportFile, employee_id: str = DEFAULT_EMPLOYEE
    ) -> extraction_tool_pb2.ExtractionConfigurationRequest:
        """
        Encodes an ImportFile into an ExtractionConfigurationRequest message.

        Args:
            file (ImportFile): The ImportFile to be encoded.
            employee_id (str, optional): The employee ID. Defaults to DEFAULT_EMPLOYEE.

        Returns:
            extraction_tool_pb2.ExtractionConfigurationRequest: The encoded message.
        """
        message_file = file.encode()

        return extraction_tool_pb2.ExtractionConfigurationRequest(
            Language=Common_pb2.English,
            File=message_file,
            Sections=message_file.Sections,
            EmployeeId=employee_id,
            # Compressed = False,
        )

    def decode(self, message):
        """
        Not implemented.
        """
        raise NotImplementedError()
