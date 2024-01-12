from abc import ABC, abstractmethod
from typing import Any, List


class DomainAdapter(ABC):
    @abstractmethod
    def encode(self, model: Any) -> Any:
        """
        Encode a domain model into a format suitable for external representation.

        Parameters:
            model (Any): The domain model to be encoded.

        Returns:
            Any: The encoded representation of the domain model.
        """
        pass

    def encode_list(self, models: List[Any]) -> List[Any]:
        """
        Encode a list of domain models into a list of representations suitable for external representation.

        Parameters:
            models (List[Any]): The list of domain models to be encoded.

        Returns:
            List[Any]: The list of encoded representations of domain models.
        """
        return [self.encode(model) for model in models]

    @abstractmethod
    def decode(self, message: Any) -> Any:
        """
        Decode an external representation into a domain model.

        Parameters:
            message (Any): The external representation to be decoded.

        Returns:
            Any: The decoded domain model.
        """
        pass

    def decode_list(self, messages: List[Any]) -> List[Any]:
        """
        Decode a list of external representations into a list of domain models.

        Parameters:
            messages (List[Any]): The list of external representations to be decoded.

        Returns:
            List[Any]: The list of decoded domain models.
        """
        return [self.decode(message) for message in messages]


class StandardAdapter(DomainAdapter):
    def encode(self, model: Any) -> Any:
        """
        Converts a model instance into a protobuf message.

        This method translates a model object into a protobuf format.

        Parameters:
            model (Any): The model instance to be converted.

        Returns:
            Any: A protobuf message representing the model.
        """

        return model.encode()

    def decode(self, message: Any, model_class: Any) -> Any:
        """
        Converts a protobuf message into a model instance.

        This method takes a message, typically obtained from a protobuf message,
        and constructs an instance of the model using the message's values.

        Parameters:
            message (Any): The protobuf message.

        Returns:
            model: An instance of the model constructed from the provided message.
        """
        # Decode the model instance using the message
        return model_class.decode(message)
