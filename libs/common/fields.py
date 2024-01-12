from datetime import datetime
import math
from typing import Type, Any, NewType, List

from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.json_format import MessageToDict

from libs.common.enums import InterfaceEnum
from libs.common.constants import PK_FIELD_NOT_AVAILABLE
from hornets.utilities.log_config import logger

Money = NewType("Money", Any)
Telephone = NewType("Telephone", Any)
MessageList = NewType("MessageList", Any)
Message = NewType("Message", Any)
DomainModel = NewType("DomainModel", Any)


class Field:
    """
    Base class representing a generic field.

    Attributes:
    - target_field (str): The name of the target field.
    - domain_type (Type): The type used for encoding the field.
    - target_type (Type): The type used for decoding the field.
    """

    def __init__(
        self,
        domain_type: Type = int,
        target_type: Type = int,
        target_field: str = PK_FIELD_NOT_AVAILABLE,
    ):
        self.target_field = target_field
        self.domain_type = domain_type
        self.target_type = target_type

    def encode(self, value: Any) -> Any:
        if value is None:
            logger.debug(f"Encode None value for field {self.target_field}")
            return value
        return self.target_type(value)

    def decode(self, value: Any) -> Any:
        if value is None:
            logger.debug(f"Decoded None value for field {self.target_field}")
            return value
        return self.domain_type(value)


class MoneyField(Field):
    """
    Class representing a field for handling monetary values.

    Attributes:
    - money_class (Type[Money]): The class representing the monetary value.
    """

    NANO = 1e9

    def __init__(
        self,
        money_class: Type[Money],
        target_field: str = PK_FIELD_NOT_AVAILABLE,
    ):
        self.money_class = money_class
        super().__init__(target_field=target_field, domain_type=float, target_type=Money)

    def encode(self, value: float) -> Money:
        units, nanos = self.encode_amount(value)
        return self.money_class(currency_code="USD", units=units, nanos=nanos)

    def decode(self, value: Money) -> float:
        result = 0.0
        if not isinstance(value, dict):
            try:
                value = dict(value)
            except TypeError:
                value = MessageToDict(value)
            except Exception:
                raise Exception(f"Could not decode money payload with value: '{value}'")

        if "nanos" in value:
            result = int(value["nanos"]) / self.NANO
        if "units" in value:
            result += int(value["units"])
        return result

    @staticmethod
    def encode_amount(amount: float):
        """
        Encode the given monetary amount into units and nanos.

        Parameters:
        - amount (float): The monetary amount to encode.

        Returns:
        Tuple containing units and nanos.
        """
        if isinstance(amount, int):
            amount = float(amount)

        if not isinstance(amount, float):
            raise TypeError("Amount should be float")

        sign = 1 if amount >= 0 else -1
        amount = abs(amount)

        fractional_part, integer_part = math.modf(amount)

        units = int(sign * integer_part)
        nanos = int(sign * fractional_part * 1e9)

        return units, nanos


class EnumeratedField(Field):
    """
    Class representing a field for handling enumerated values.

    Attributes:
    - enumerated (InterfaceEnum): The enumerated type.
    """

    def __init__(
        self,
        enumerated: type[InterfaceEnum],
        target_field: str = PK_FIELD_NOT_AVAILABLE,
    ):
        super().__init__(target_field=target_field, domain_type=enumerated, target_type=int)

    def encode(self, value: InterfaceEnum) -> int:
        if not isinstance(value, self.domain_type):
            raise TypeError(f"{self.domain_type} instance should be provided to encode enumerated field")
        return value.backend

    def decode(self, value: int) -> InterfaceEnum:
        if value is None:
            value = 0
        return self.domain_type.from_value(int(value))


class TimestampField(Field):
    """
    Class representing a field for handling timestamp values.
    """

    def __init__(self, target_field: str = PK_FIELD_NOT_AVAILABLE):
        super().__init__(target_field=target_field, domain_type=datetime, target_type=Timestamp)

    def encode(self, value: datetime) -> Timestamp:
        if not isinstance(value, datetime):
            raise TypeError("datetime instance should be provided to encode a timestamp field")

        # TODO
        # Should we take into account nanos?

        timestamp = Timestamp()
        timestamp.seconds = int(value.timestamp())
        timestamp.nanos = 0
        return timestamp

    def decode(self, value: Timestamp) -> datetime:
        if not isinstance(value, Timestamp):
            raise TypeError("'google.protobuf.timestamp_pb2' instance should be provided")

        # TODO
        # Should we take into account nanos?

        return datetime.fromtimestamp(int(value.seconds))


class ListField(Field):
    """
    Class representing a field with a list of objects.
    Attributes:
    - element_field (Field): The field descriptor of the list elements.
    """

    def __init__(
        self,
        element_field: Field,
        target_field: str = PK_FIELD_NOT_AVAILABLE,
    ):
        self.element_field = element_field
        super().__init__(target_field=target_field)

    def encode(self, value: List) -> MessageList:
        return [self.element_field.encode(item) for item in value]

    def decode(self, value: MessageList) -> List:
        return [self.element_field.decode(item) for item in value]


class ComposeField(Field):
    """
    Class representing composed field. This field includes a model that should have mapping information!
    Attributes:
    - model (DomainModel): The model to encode inside the field.
    - target_type (Message): The type that the model should be encoded to.
    - target_field (str): Name of the field where the compose model will be encoded/decoded to.
    """

    def __init__(
        self,
        model: DomainModel,
        target_field: str = PK_FIELD_NOT_AVAILABLE,
    ):
        super().__init__(target_field=target_field, domain_type=model)

    def encode(self, model: DomainModel) -> Message:
        return model.encode()

    def decode(self, values: Message) -> DomainModel:
        return self.domain_type.decode(values)
