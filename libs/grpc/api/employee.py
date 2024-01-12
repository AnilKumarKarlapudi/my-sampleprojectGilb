from hornets.utilities.log_config import logger
from typing import Any, List, Optional

from libs.grpc.resources.compiled_protos import Common_pb2, Employee_pb2
from libs.grpc.services.resources import EmployeeResource

from google.protobuf.json_format import MessageToDict
from libs.grpc.api.adapters.base import StandardAdapter
from libs.grpc.hints import Employee


class EmployeeAPI(EmployeeResource):
    ADAPTER = StandardAdapter()

    def create(self, employee: Employee) -> Employee:
        """
        Creates a new employee.

        Args:
            employee (Employee): The Employee object to be created.

        Returns:
            Employee: The newly created Employee object if successful, None otherwise.
        """
        employee_message = self.ADAPTER.encode(employee)

        request = Employee_pb2.AddEmployeeRequest(
            Language=Common_pb2.English, Employee=employee_message, BulkUpdate=False
        )

        result = self.stub.AddEmployee(request)
        if not result.Success:
            logger.error(f"AddEmployee failed. Request: {request}")
            return None

        return self.get(employee.id, employee.__class__)

    def all(self, target_class: Employee) -> List[Employee]:
        """
        Retrieves all employees.

        Returns:
            List[Employee]: A list of Employee objects. Returns an empty list if no employee are found.
        """
        request = Employee_pb2.GetEmployeesRequest(Language=Common_pb2.English)

        try:
            result = self.stub.GetEmployees(request)
            result = result.Employees
        except Exception as e:
            logger.error(f"GetEmployeesRequest failed. Request: {request}, Error: {e}")
            return []

        return [self.ADAPTER.decode(obj, target_class) for obj in result]

    def delete(self, employee: Employee) -> bool:
        """
        Deletes a specific employee.

        Args:
            employee (Employee): The Employee object to be deleted.

        Returns:
            bool: True if the deletion is successful, False otherwise.
        """

        # Ensure that employee is there
        employee = self.get(employee.id, employee.__class__)

        # Disable employee
        employee.active = False
        return self.update(employee) is not None

    def get(self, employee_id: str, model_class: Any) -> Optional[Employee]:
        """
        Retrieves an employee by its id.

        Args:
            employee_id (str): The id of the employee to retrieve.

        Returns:
            Employee: The requested Employee object if successful, None otherwise.
        """
        request = Employee_pb2.GetEmployeeRequest(EmployeeId=employee_id, Language=Common_pb2.English)

        result = self.stub.GetEmployee(request)
        if not MessageToDict(result):
            return None

        return self.ADAPTER.decode(result.Employee, model_class)

    def update(self, employee: Employee) -> Employee:
        """
        Update an employee data.

        Args:
            employee (Employee): The Employee object to be created.

        Returns:
            Employee: The updated Employee object if successful, None otherwise.
        """
        employee_message = self.ADAPTER.encode(employee)

        request = Employee_pb2.UpdateEmployeeRequest(
            Language=Common_pb2.English, Employee=employee_message, BulkUpdate=False
        )

        result = self.stub.UpdateEmployee(request)
        if not result.Success:
            logger.error(f"UpdateEmployee failed. Request: {request}")
            return None

        return self.get(employee.id, employee.__class__)

    def exists(self, employee: Employee) -> bool:
        """
        Checks if a specific employee exists.

        Args:
            employee: The employee object to check for existence.

        Returns:
            bool: Whether requested Employee id exist or not.
        """
        return self.get(employee.id, employee.__class__) is not None
