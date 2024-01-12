from typing import Dict, Literal, Any, NewType, List, Type

from libs.common.fields import Field
from libs.common.constants import PK_FIELD_NOT_AVAILABLE
from libs.grpc.services.models import GrpcApiChannel
from hornets.utilities.log_config import logger


Operator = NewType("Operator", Any)  # eq, lt, gt, le, ge
GRPCMessage = NewType("GRPCMessage", Any)


class TemplateModel:
    """
    Base class for domain models.
    """

    class META:
        resource: Literal["grpc", "db", "rest"]
        mapping: Dict[str, Field]
        pk_field: str = PK_FIELD_NOT_AVAILABLE
        target_message: GRPCMessage

    def __init__(self, **kwargs):
        for field_name, field_value in kwargs.items():
            setattr(self, field_name, field_value)

    # Casters
    @classmethod
    def decode(cls, resource):
        """
        Decode a resource into a TemplateModel instance.

        Parameters:
        - resource: The resource to decode.

        Returns:
        A TemplateModel instance.
        """
        if isinstance(resource, cls):
            raise TypeError("Decoding from the same type is not possible")
        model = {}

        fields = cls.__annotations__.keys()

        if not fields:
            raise Exception("Could not encode an empty model")

        for field_name in fields:
            if field_name in cls.META.mapping:
                resource_field = cls.META.mapping[field_name]
                value = getattr(resource, resource_field.target_field, None)
                if value is not None:
                    model[field_name] = resource_field.decode(value)
            else:
                logger.warning(f"{field_name} from {cls} is not mapped.")
        return cls(**model)

    def encode(self):
        """
        Encode a TemplateModel instance into a target type (gprc message).

        Returns:
        An instance of the target type.
        """

        target_type = self.META.target_message

        if not target_type:
            raise Exception(f"Unknown target message for {self.__class__.__name__}")

        encoded_model = {}

        fields = self.__annotations__.keys()

        if not fields:
            raise Exception("Could not decode an empty model")

        for field_name in fields:
            if field_name in self.META.mapping:
                resource_field = self.META.mapping[field_name]
                value = getattr(self, field_name, None)
                if value is not None:
                    encoded_model[resource_field.target_field] = resource_field.encode(value)
            else:
                logger.warning(f"{field_name} from {self.__class__} is not mapped.")

        encoded_model = self._check_id(encoded_model)

        try:
            return target_type(**encoded_model)
        except Exception as e:
            logger.error(f"Error encoding into: {target_type.__class__.__name__} --> {e}")

    def _check_id(self, model):
        pk_field = self.META.pk_field
        # If the model has an id field, set it to a high value
        if pk_field != PK_FIELD_NOT_AVAILABLE:
            if pk_field not in model:
                try:
                    model[pk_field] = 9999
                except Exception as e:
                    logger.warning(f"Could not set id for {self.__class__.__name__} --> {e}")
        return model

    # API Methods
    @classmethod
    def all(cls, api: GrpcApiChannel) -> List["TemplateModel"]:
        """
        Retrieve all instances of the TemplateModel from the API.

        Parameters:
        - api: The API instance.

        Returns:
        A list of TemplateModel instances.
        """
        return api.all(target_class=cls)

    @classmethod
    def count(cls, api: GrpcApiChannel) -> int:
        """
        Retrieve the count of instances of the TemplateModel from the API.

        Parameters:
        - api: The API instance.

        Returns:
        The count of TemplateModel instances.
        """
        return len(api.all(target_class=cls))

    def exists(self, api: GrpcApiChannel) -> bool:
        """
        Check if the TemplateModel instance exists in the API.

        Parameters:
        - api: The API instance.

        Returns:
        True if the instance exists, False otherwise.
        """
        return api.exists(self)

    def save(self, api: GrpcApiChannel) -> Type["TemplateModel"]:
        """
        Save the TemplateModel instance in the API.

        Parameters:
        - api: The API instance.

        Returns:
        The result of the save operation.
        """
        if self.exists(api):
            return api.update(self)

        result = api.create(self)

        if hasattr(self, "id"):
            self.id = result.id

        return result

    def delete(self, api: GrpcApiChannel) -> bool:
        """
        Delete the TemplateModel instance from the API.

        Parameters:
        - api: The API instance.

        Returns:
        True if the delete operation is successful, False otherwise.
        """
        try:
            api.delete(self)
            if hasattr(self, "id"):
                self.id = -1
        except Exception:
            return False
        return True

    @classmethod
    def filter(cls, api: GrpcApiChannel, filters: List["ModelFilter"]):
        """
        Filter instances of the TemplateModel from the API.

        Parameters:
        - api: The API instance.
        - filters: List of ModelFilter instances for filtering.

        Returns:
        A filtered list of TemplateModel instances.
        """
        instances = api.all(target_class=cls)
        result = instances.copy()

        try:
            for filter in filters:
                result = [
                    instance for instance in result if filter.operator(getattr(instance, filter.field), filter.value)
                ]
        except Exception:
            logger.error(f"Error filtering {cls.__name__} by {filter.field} = {filter.value}")
            return []

        return result

    def __eq__(self, other) -> bool:
        """
        Compare TemplateModel instances for equality.

        Parameters:
        - other: The other instance to compare.

        Returns:
        True if the instances are equal, False otherwise.
        """
        if isinstance(other, self.__class__):
            self_attributes = vars(self)
            other_attributes = vars(other)
            return self_attributes == other_attributes
        return False


class ModelFilter:
    """
    Filter class for filtering instances of TemplateModel.

    Attributes:
    - field: The field to filter on.
    - value: The value to compare with.
    - operator: The comparison operator.
    """

    def __init__(self, field: str, value: Any, operator: Operator):
        self.field = field
        self.value = value
        self.operator = operator  # eq, lt, gt, le, ge
