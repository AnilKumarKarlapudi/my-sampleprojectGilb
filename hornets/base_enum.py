from enum import Enum


class BaseEnum(Enum):

    def __str__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, str):
            return self.value == other
        return super().__eq__(other)

    def __hash__(self):
        return hash(self.value)

    @classmethod
    def from_string(cls, value):
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        else:
            raise KeyError(f"No enum member with value '{value}'")
