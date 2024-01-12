from enum import Enum
from hornets.utilities.log_config import logger


class InterfaceEnum(Enum):
    @property
    def backend(self):
        return self.value[0]

    @property
    def frontend(self):
        return self.value[1]

    @classmethod
    def from_value(cls, value: int, default_value=0):
        if value is None:
            return cls.from_value(default_value)

        for enum_member in cls:
            if enum_member.value[0] == value:
                return enum_member

        # TODO
        # This piece of code should be removed once we covered all enums from Passport

        logger.debug(f"Unknown value {value} for {cls.__name__} enum. Returning default: {default_value}.")
        return cls.from_value(default_value)

    def __hash__(self):
        return hash(self.value)

    def __str__(self):
        return f"<{self.__class__.__name__}.{self.name}: {self.value}>"

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)
