from hornets.tools.extraction.models import ImportFile
from hornets.tools.extraction.enums import ExtractionToolSection
from hornets.tools.mode import ToolStrategy
from hornets.utilities.log_config import logger


# Tool
def test_import_tool(extraction_tool):
    files = extraction_tool.available_files()
    assert len(files), "No import files available."

    file = ImportFile(
        file_name=files[0].file_name, directory=files[0].directory, sections=[ExtractionToolSection.SPEED_KEYS]
    )

    status = extraction_tool.import_tool(file=file, strategy=ToolStrategy.BACKEND)
    logger.info(vars(status))
    assert status.is_import
    assert status.success


def test_export_tool(extraction_tool):
    files = extraction_tool.available_files()
    assert len(files), "No import files available."

    file = ImportFile(
        file_name="pytets_grpc.json", directory=files[0].directory, sections=[ExtractionToolSection.ITEMS]
    )

    export_file_path, status = extraction_tool.export_tool(file=file, strategy=ToolStrategy.BACKEND)

    logger.info(status)

    assert export_file_path is not None
    assert status.is_import is False
    assert status.success is True


# TODO
# Increase test coverage


# API
def test_import_files(extraction_tool_configuration_api):
    files = extraction_tool_configuration_api._available_import_files(ImportFile)
    assert len(files), "No import files available."
    assert isinstance(files[0], ImportFile)


def test_extraction_tool_directories(extraction_tool_configuration_api):
    dirs = extraction_tool_configuration_api._extraction_tool_directories()
    assert isinstance(dirs, list)
    assert isinstance(dirs[0], str)


def test_import_file(extraction_tool_configuration_api):
    files = extraction_tool_configuration_api._available_import_files(ImportFile)
    assert len(files), "No import files available."
    selected_file = files[0]

    logger.debug(f"Selected file: {selected_file.path}")

    extraction_tool_configuration_api.import_tool(file=selected_file)

    status = extraction_tool_configuration_api.status()

    logger.debug(f"Status: {vars(status)}")

    assert status.is_import
    # assert status.success


def test_export_file(extraction_tool_configuration_api):
    file_path = extraction_tool_configuration_api.export_tool(sections=[ExtractionToolSection.SPEED_KEYS])

    logger.info(file_path)

    status = extraction_tool_configuration_api.status()

    logger.debug(f"Status: {vars(status)}")

    assert status.is_import is False
    assert status.success is True
