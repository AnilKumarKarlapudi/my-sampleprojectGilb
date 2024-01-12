from libs.grpc.services.resources import GrpcToolChannel
from abc import ABC


class BaseTool(ABC):
    def __init__(self, backend_api: GrpcToolChannel):
        self.backend_api = backend_api
