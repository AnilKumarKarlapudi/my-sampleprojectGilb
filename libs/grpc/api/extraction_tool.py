from libs.grpc.services.resources import ExtractionToolResource
from libs.grpc.resources.compiled_protos import ExtractionTool_pb2
from hornets.tools.extraction.models import ProgressUpdate, ImportFile
from libs.grpc.api.adapters.extraction_tool import ExtractionToolAdapter
from typing import NewType, List, Any


Section = NewType("Section", Any)


class ExtractionToolAPI(ExtractionToolResource):
    ADAPTER = ExtractionToolAdapter()
    DEFAULT_FILE_NAME = "export_grpc.json"

    def import_tool(self, file: ExtractionTool_pb2.ExtractionFile) -> bool:
        """
        Imports an ExtractionTool_pb2.ExtractionFile into passport.

        Args:
            file (ExtractionTool_pb2.ExtractionFile): The file to be imported.

        Returns:
            bool: Import result.
        """
        request = self.ADAPTER.encode(file)
        self.stub.ImportConfiguration(request)
        return True

    def status(self):
        """
        Retrieves the extraction status and decodes it into a ProgressUpdate.

        Returns:
            ProgressUpdate: The decoded extraction status.
        """
        request = ExtractionTool_pb2.GetExtractionStatusRequest()
        result_message = self.stub.GetExtractionStatus(request)
        result_message = result_message.Update
        return ProgressUpdate.decode(result_message)

    def export_tool(self, sections: List[Section], file_name: str = DEFAULT_FILE_NAME, directory: str = None) -> str:
        """
        Exports the tool configuration based on specified sections and destination file.

        Args:
            sections (List[Section]): List of sections to export.
            file_name (str, optional): Name of the export file. Defaults to DEFAULT_FILE_NAME.
            directory (str, optional): Directory to save the export file. Defaults to None.

        Returns:
            str: The path to the exported file.
        """
        if not directory:
            directories = self._extraction_tool_directories()
            directory = directories[0]

        file = ImportFile(file_name=file_name, directory=directory, sections=sections)
        request = self.ADAPTER.encode(file)
        self.stub.ExportConfiguration(request)
        return file.path

    def _available_import_files(self, target_class):
        """
        Retrieves a list of available import files.

        Args:
            target_class: The target class for decoding.

        Returns:
            List[Any]: List of decoded import files.
        """
        request = ExtractionTool_pb2.GetAvailableImportFilesRequest()
        result = self.stub.GetAvailableImportFiles(request)
        import_files_messages = result.ImportFiles
        return [target_class.decode(import_file) for import_file in import_files_messages]

    def _extraction_tool_directories(self):
        """
        Retrieves a list of available extraction tool directories.

        Returns:
            List[str]: List of extraction tool directories.
        """
        request = ExtractionTool_pb2.GetExtractionToolDirectoriesRequest()
        result = self.stub.GetExtractionToolDirectories(request)
        return [str(dir) for dir in result.Directories]
