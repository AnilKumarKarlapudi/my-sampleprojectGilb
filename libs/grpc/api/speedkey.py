from hornets.utilities.log_config import logger
from typing import List
from grpc import RpcError
from libs.grpc.services.resources import RegisterResource
from libs.grpc.api.adapters.speedkey import SpeedKeyAdapter
from libs.grpc.resources.compiled_protos import Register_pb2 as register_pb2, Common_pb2
from libs.grpc.hints import SpeedKey


class SpeedKeyAPI(RegisterResource):
    ADAPTER = SpeedKeyAdapter()
    DEFAULT_MENU = 0
    DEFAULT_FILTER = register_pb2.SpeedKeyMenuFilter.SpeedKeyMenusOnly

    def create(self, model: SpeedKey, delete: bool = False) -> bool:
        """
        Creates a new set of SpeedKeys, with options to clean or delete existing entries.

        Args:
            model (SpeedKey): The SpeedKey model or a list of models to be created.
            delete (bool): Used to indicate the method that we are overriding a speedkey.

        Returns:
            bool: True if the operation is successful, False otherwise.

        Raises:
            Exception: If positions in the SpeedKeys are repeated.
        """
        # Check if I need to clean up
        clean = not model

        # Get the current speed keys and add them to the menu to avoid override
        if not clean and not delete:
            current_keys = self.all(model.__class__)
            current_keys.append(model)
        elif delete:
            current_keys = model
        else:
            current_keys = []

        request = register_pb2.UpdateSpeedKeyMenuRequest(
            Language=Common_pb2.English, SpeedKeyMenu=self.ADAPTER.encode(current_keys)
        )

        try:
            result = self.stub.UpdateSpeedKeyMenu(request)
        except RpcError as e:
            logger.error(f"GRPC error during SpeedKey creation: {e}")
            return False

        if not result.Success:
            logger.error(f"SpeedKey creation failed. Request:'{request}'")
            return False

        # Search for the speedkey I just created
        if not clean and not delete:
            return self._search_for_speedkey(model)
        else:
            return True

    def _search_for_speedkey(self, model) -> SpeedKey:
        """
        Search for a speedkey.

        Args:
            model

        Returns:
            SpeedKey: The SpeedKey object if found, None otherwise.
        """
        speed_keys = self.all(model.__class__)
        for speed_key in speed_keys:
            if speed_key.position == model.position:
                return speed_key
        return None

    def all(self, target_class: SpeedKey) -> List[SpeedKey]:
        """
        Retrieves all SpeedKeys from the SpeedKey menu.

        This method sends a request to get all SpeedKey menus with the specified language and filter.
        It then processes the response to extract and decode the SpeedKeys.

        Returns:
            List[SpeedKey]: A list of SpeedKey objects retrieved from the SpeedKey menu.
            Returns an empty list if no SpeedKeys are found or if an error occurs.

        Raises:
            Exception: If there's an issue with the request or processing the response.
        """

        request = register_pb2.GetSpeedKeyMenusRequest(
            Language=Common_pb2.English,
            Filter=self.DEFAULT_FILTER,
            IncludeSpeedKeys=True,
        )

        try:
            response = self.stub.GetSpeedKeyMenus(request)
            speedkeys = response.Menus[self.DEFAULT_MENU].SpeedKeys
        except RpcError as e:
            logger.error(f"GRPC error during SpeedKey retrieval: {e}")
            return []
        except Exception as e:
            logger.error(f"Error retrieving SpeedKeys from response: {e}")
            return []

        return self.ADAPTER.decode(speedkeys, target_class)

    def clean(self) -> bool:
        """
        Removes all SpeedKeys from the system.

        Returns:
            bool: True if all SpeedKeys are successfully removed, False otherwise.
        """
        return self.create([])

    def delete(self, model: SpeedKey) -> bool:
        """
        Deletes a specific SpeedKey from the system.

        This method removes a specified SpeedKey based on its position.
        Args:
            model (SpeedKey): The SpeedKey object to be deleted.

        Returns:
            bool: True if the SpeedKey is successfully deleted, False otherwise.

        Raises:
            Exception: If the specified SpeedKey is not found in the current list of SpeedKeys.
        """

        current_speed_keys = self.all(model.__class__)

        # Create a new list without the speed key I want to delete
        new_speed_keys = [obj for obj in current_speed_keys if obj.position != model.position]

        return self.create(new_speed_keys, delete=True)

    def update(self):
        raise NotImplementedError()

    def get(self):
        raise NotImplementedError()
