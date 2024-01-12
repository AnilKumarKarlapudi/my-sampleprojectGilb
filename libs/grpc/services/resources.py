from abc import ABC

from libs.grpc.services.models import GrpcToolChannel, GrpcApiChannel
from libs.grpc.resources.compiled_protos import Pricebook_pb2_grpc, Register_pb2_grpc, Employee_pb2_grpc
from libs.grpc.resources.compiled_protos import ExtractionTool_pb2_grpc


class PricebookResource(GrpcApiChannel, ABC):
    def __init__(self, channel):
        super().__init__(Pricebook_pb2_grpc.PricebookServiceStub(channel))


class RegisterResource(GrpcApiChannel, ABC):
    def __init__(self, channel):
        super().__init__(Register_pb2_grpc.RegisterServiceStub(channel))


class EmployeeResource(GrpcApiChannel, ABC):
    def __init__(self, channel):
        super().__init__(Employee_pb2_grpc.EmployeeServiceStub(channel))


class ExtractionToolResource(GrpcToolChannel, ABC):
    def __init__(self, channel):
        super().__init__(ExtractionTool_pb2_grpc.ExtractionToolServiceStub(channel))
