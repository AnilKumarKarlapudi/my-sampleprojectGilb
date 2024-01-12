import libs.grpc.resources.compiled_protos.Register_pb2 as register_pb2
from libs.grpc.api.adapters.base import DomainAdapter

DEFAULT_MENU_ID = 1
DEFAULT_LEVEL = 1
DEFAULT_DESCRIPTION = "Default"


class SpeedKeyAdapter(DomainAdapter):
    """
    Adapter for encoding and decoding SpeedKey objects.
    """

    def encode(self, models):
        """
        Encode a list of SpeedKey models into a SpeedKeyMenu.

        Args:
            models (List): List of SpeedKey models to be encoded.

        Returns:
            register_pb2.SpeedKeyMenu: Encoded SpeedKeyMenu.
        """
        speedkeys = [model.encode() for model in models]

        return register_pb2.SpeedKeyMenu(
            MenuId=DEFAULT_MENU_ID,
            Level=DEFAULT_LEVEL,
            Description=DEFAULT_DESCRIPTION,
            SpeedKeys=speedkeys,
        )

    def decode(self, objects, target_class):
        """
        Decode a list of SpeedKey objects from a SpeedKeyMenu.

        Args:
            objects (List): List of encoded SpeedKey objects.
            target_class: Target class for decoding.

        Returns:
            List: Decoded SpeedKey objects.
        """
        return [target_class.decode(model) for model in objects]
