import libs.grpc.resources.compiled_protos.Pricebook_pb2 as pricebook_pb2
from libs.grpc.api.adapters.base import DomainAdapter
from libs.grpc.hints import Discount


class ManualDiscountAdapter(DomainAdapter):
    def encode(self, model: Discount) -> pricebook_pb2.ManualDiscount:
        """
        Converts a Discount model instance into a ManualDiscount protobuf message.

        This method translates the Discount object into a protobuf format, setting up monetary
        values and configuring the discount's validity period (start and end dates).

        Parameters:
            model (Discount): The Discount model instance to be converted.

        Returns:
            pricebook_pb2.ManualDiscount: A protobuf message representing the manual discount.
        """

        discount_values_message = model.encode()

        return pricebook_pb2.ManualDiscount(
            Values=discount_values_message,
            # MaxAmountOff=amount,
            # MaxPercentOff=amount
        )

    def decode(self, model: pricebook_pb2.ManualDiscount, target_class) -> Discount:
        """
        Converts a ManualDiscount protobuf message into a Discount model instance.

        This method takes a ManualDiscount message, typically obtained from a protobuf message,
        and constructs an instance of the Discount model using the message's values.

        Parameters:
            model (pricebook_pb2.ManualDiscount): The ManualDiscount protobuf message.
            target_class: The target Discount model class.

        Returns:
            Discount: An instance of the Discount model constructed from the provided message.
        """
        # Extract the Discount object from the ManualDiscount message
        discount_values = model.Values

        # Decode the Discount instance using the extracted values
        decoded_discount = target_class.decode(discount_values)

        return decoded_discount
