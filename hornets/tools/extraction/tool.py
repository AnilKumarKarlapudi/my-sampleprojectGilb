from hornets.tools.mode import ToolStrategy
from hornets.tools.base import BaseTool
from hornets.tools.extraction.models import ImportFile, ProgressUpdate
from typing import Any, NewType
from typing import Tuple

FilePath = NewType("FilePath", Any)


class ExtractionTool(BaseTool):
    def import_tool(self, file: ImportFile, strategy: ToolStrategy = ToolStrategy.BACKEND) -> ProgressUpdate:
        """
        Imports data using the specified strategy.

        Parameters:
        - file (ImportFile): The import file containing data to be processed.
        - strategy (ToolStrategy): The strategy to be used for importing (default: ToolStrategy.BACKEND).

        Returns:
        ProgressUpdate: The progress update after the import operation.
        """
        if strategy == ToolStrategy.BACKEND:
            self.backend_api.import_tool(file)
            return self.backend_api.status()
        elif strategy == ToolStrategy.FRONTEND:
            raise NotImplementedError()
        else:
            raise NotImplementedError("Strategy not recognized.")

    def export_tool(
        self, file: ImportFile, strategy: ToolStrategy = ToolStrategy.BACKEND
    ) -> Tuple[FilePath, ProgressUpdate]:
        """
        Exports data using the specified strategy.

        Parameters:
        - file (ImportFile): The export file containing data to be processed.
        - strategy (ToolStrategy): The strategy to be used for exporting (default: ToolStrategy.BACKEND).

        Returns:
        Tuple[str, ProgressUpdate]: A tuple containing the export file path and progress update.
        """
        if strategy == ToolStrategy.BACKEND:
            export_file_path = self.backend_api.export_tool(file.sections, file.file_name, file.directory)
            return export_file_path, self.backend_api.status()
        elif strategy == ToolStrategy.FRONTEND:
            raise NotImplementedError()
        else:
            raise NotImplementedError("Strategy not recognized.")

    def available_files(self):
        return self.backend_api._available_import_files(ImportFile)
