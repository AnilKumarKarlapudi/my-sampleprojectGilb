from typing import Any, List, Optional
from google.protobuf.json_format import MessageToDict
from grpc import RpcError

from libs.grpc.api.adapters.base import StandardAdapter
from libs.grpc.services.resources import RegisterResource
from libs.grpc.resources.compiled_protos import Register_pb2 as register_pb2, Common_pb2
from libs.grpc.hints import Register

from hornets.utilities.log_config import logger


class RegisterAPI(RegisterResource):
    ADAPTER = StandardAdapter()

    def create(self, register: Register) -> Register:
        """
        Creates a new register.

        Args:
            register (Register): The Register model.

        Returns:
            Register: Created register model gotten from system.
        """
        request = self.ADAPTER.encode(register)

        result = self.stub.AddRegister(request)
        if not result.Success:
            logger.error(f"AddRegister failed. Request: {request}")
            return None

        return self.get(register.id, register.__class__)

    def all(self, target_class: Register) -> List[Register]:
        """
        Retrieves all Registers from the system.

        Returns:
            List[Register]: A list of Register objects retrieved from system.
            Returns an empty list if no Registers are found or if an error occurs.

        Raises:
            Exception: If there's an issue with the request or processing the response.
        """

        request = register_pb2.GetAllRegistersRequest(Language=Common_pb2.English)

        try:
            response = self.stub.GetAllRegisters(request)
            registers = response.Registers
        except RpcError as e:
            logger.error(f"GRPC error during GetAllRegisters retrieval: {e}")
            return []
        except Exception as e:
            logger.error(f"Error retrieving Registers from response: {e}")
            return []

        return [self.ADAPTER.decode(obj, target_class) for obj in registers]

    def delete(self, register: Register) -> bool:
        """
        Deletes a specific Register from the system.

        Args:
            register (Register): The Register object to be deleted.

        Returns:
            bool: True if the Register is successfully deleted, False otherwise.
        """
        request = register_pb2.DeleteRegisterRequest(RegisterId=register.id, Language=Common_pb2.English)

        result = self.stub.DeleteRegister(request)
        if not result.Success:
            logger.error(f"DeleteRegister failed. Request: {request}")
            return False

        return True

    def update(self, register: Register) -> Register:
        """
        Update a register.

        Args:
            register (Register): The Register model.

        Returns:
            Register: Updated register model gotten from system.
        """
        request = self.ADAPTER.encode(register)

        result = self.stub.UpdateRegister(request)
        if not result.Success:
            logger.error(f"UpdateRegister failed. Request: {request}")
            return None

        return self.get(register.id, register.__class__)

    def get(self, register_id: str, model_class: Any) -> Optional[Register]:
        """
        Retrieves an employee by its id.

        Args:
            register_id (int): The id of the register to retrieve.

        Returns:
            Register: The requested Register object if successful, None otherwise.
        """
        request = register_pb2.GetRegisterRequest(RegisterId=register_id, Language=Common_pb2.English)

        result = self.stub.GetRegister(request)
        if not MessageToDict(result):
            return None

        return self.ADAPTER.decode(result.Register, model_class)
