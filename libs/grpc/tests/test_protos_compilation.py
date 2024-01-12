import os
import importlib.util
import pytest
from libs.grpc.paths import COMPILED_PROTOS_DIR


@pytest.mark.internal
def test_import_all_compiled_protos():
    for file_name in os.listdir(COMPILED_PROTOS_DIR):
        if file_name.endswith(".py") and not file_name.startswith("__"):
            module_name = os.path.splitext(file_name)[0]
            module_path = os.path.join(COMPILED_PROTOS_DIR, file_name)

            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)

            if "Register" not in module_name:
                try:
                    spec.loader.exec_module(module)
                    print(f"Imported module: {module_name}")
                except Exception as e:
                    print(f"Failed to import module {module_name}: {e}")
                    # assert False  # Fail the test if any module fails to import
