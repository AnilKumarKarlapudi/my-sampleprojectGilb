from abc import ABC, abstractmethod


class GrpcToolChannel(ABC):
    """
    GRPC Tool channel.
    Basic channel for broaden integrations.
    """

    def __init__(self, stub):
        self.stub = stub


class GrpcApiChannel(GrpcToolChannel, ABC):
    """
    GRPC channel.
    Generic channel for models interactions.
    """

    @abstractmethod
    def all(self, target_class):
        """
        Retrieves all elements from the gRPC service.
        """
        raise NotImplementedError()

    @abstractmethod
    def get(self, filter):
        """
        Retrieves a specific element based on a filter.

        Args:
            filter: Filter criteria to retrieve a specific element.
        """
        raise NotImplementedError()

    @abstractmethod
    def create(self, element):
        """
        Creates a new element or a list of elements.

        Args:
            element: The element or list of elements to create.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete(self, element):
        """
        Deletes a specific element.

        Args:
            element: The element to delete.
        """
        raise NotImplementedError()

    @abstractmethod
    def update(self, element):
        """
        Updates a specific element or a list of elements.

        Args:
            element: The element or list of elements to update.
        """
        raise NotImplementedError()

    def exists(self, element) -> bool:
        """
        Checks if a specific element exists.

        Args:
            element: The element object to check for existence.
        """
        return any(instance == element for instance in self.all(element.__class__))
