from pathlib import WindowsPath
import libs
import os

BASE_DIR = WindowsPath(os.path.abspath(libs.__file__)).parent.parent

BASE_LIBS_DIR = BASE_DIR / "libs"
GRPC_DIR = BASE_LIBS_DIR / "grpc"
GRPC_SECURITY_DIR = GRPC_DIR / "connector" / "security"
GRPC_CERTS_DIR = GRPC_SECURITY_DIR / "certs"

COMPILED_PROTOS_DIR = GRPC_DIR / "resources" / "compiled_protos"
