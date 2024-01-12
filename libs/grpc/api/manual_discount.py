from hornets.utilities.log_config import logger
from typing import List

from libs.grpc.resources.compiled_protos import Common_pb2, Pricebook_pb2 as pricebook_pb2
from libs.grpc.services.resources import PricebookResource

from google.protobuf.json_format import MessageToDict
from libs.grpc.api.adapters.manual_discount import ManualDiscountAdapter

from libs.grpc.hints import Discount


class ManualDiscountAPI(PricebookResource):
    ADAPTER = ManualDiscountAdapter()

    def create(self, discount: Discount) -> Discount:
        """
        Creates a new manual discount.

        Args:
            discount (Discount): The Discount object to be created.

        Returns:
            Discount: The newly created Discount object if successful, None otherwise.
        """
        discount_message = self.ADAPTER.encode(discount)

        request = pricebook_pb2.AddManualDiscountRequest(Language=Common_pb2.English, Discount=discount_message)

        result = self.stub.AddManualDiscount(request)

        if not result.Success:
            logger.error(f"AddManualDiscount failed. Request: {request}")
            return None

        return self.all(discount.__class__)[-1]

    def all(self, target_class) -> List[Discount]:
        """
        Retrieves all manual discounts.

        Returns:
            List[Discount]: A list of Discount objects. Returns an empty list if no discounts are found.
        """
        request = pricebook_pb2.GetManualDiscountsRequest(Language=Common_pb2.English, IncludeStoreCoupon=True)

        try:
            result = self.stub.GetManualDiscounts(request)
            result = result.Discounts
        except Exception as e:
            logger.error(f"GetManualDiscounts failed. Request: {request}, Error: {e}")
            return []

        return [self.ADAPTER.decode(obj, target_class) for obj in result]

    def delete(self, discount: Discount) -> bool:
        """
        Deletes a specific manual discount.

        Args:
            discount (Discount): The Discount object to be deleted.

        Returns:
            bool: True if the deletion is successful, False otherwise.

        Raises:
            DeleteDiscountError: If there's an error in the deletion process.
        """

        try:
            discount_id = discount.id
        except AttributeError:
            raise DeleteDiscountError("Error deleting: Discount object does not have 'id' attribute.")

        if not discount_id:
            raise DeleteDiscountError(
                "Error deleting: Discount ID is missing. Add or retrieve the id attribute first."
            )

        discount = pricebook_pb2.Discount(DiscountId=discount.id)
        manual_discount_message = pricebook_pb2.ManualDiscount(Values=discount)
        request = pricebook_pb2.DeleteManualDiscountRequest(
            Language=Common_pb2.English, Discount=manual_discount_message
        )

        try:
            result = MessageToDict(self.stub.DeleteManualDiscount(request))
            logger.debug(f"Result to DeleteManualDiscount = {result}")

            if "Success" not in result:
                raise DeleteDiscountError(f"Error deleting --> {result}")

            return result["Success"]

        except Exception as e:
            raise DeleteDiscountError(f"Error deleting: {e}")

    def get(self, name: str):
        """
        Retrieves a discount by its name. [Method not implemented]

        Args:
            name (str): The name of the Discount to retrieve.
        """
        raise NotImplementedError()

    def update(self):
        raise NotImplementedError()


class DeleteDiscountError(Exception):
    pass
