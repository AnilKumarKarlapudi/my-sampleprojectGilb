import json
from typing import Any, Optional, TypeVar, Dict

from libs.infra.db.schemas import Field
from libs.infra.db.schemas import ModelPK
from libs.infra.db.schemas import SQLRecord
from libs.infra.db.utils import get_annotated_fields

# Alias for any type that extends from SQLModel
Model = TypeVar("Model", bound="SQLModel")


class SerializableModel(object):
    """
    Serializable model with to_map and to_json methods to be overwritten.
    """

    def __init__(self, *args, **kwargs):
        """
        Empty constructor for SerializableModel
        """
        pass

    def to_map(self) -> dict:
        """
        Default implementation.

        :returns: object as a dictionary
        """
        return self.__dict__

    def to_json(self) -> str:
        """
        Default implementation.

        :returns: object as json string
        """
        return json.dumps(self.__dict__)


class SQLModel(SerializableModel):
    """
    SQL Model wrapper for tables.
    """

    class META:
        """
        Model metadata placeholder
        """

        db: str  # required
        table_name: str  # required
        pk: ModelPK  # required
        columns: Dict[str, Field]  # required

        @classmethod
        def get_pk(cls) -> str:
            """
            Gets the Primary  Key's column name of the Model.

            :return: str - Model's primary key column name
            """
            return cls.get_column_name(cls.pk.field)

        @classmethod
        def get_column_name(cls, field_name: str) -> Optional[str]:
            """
            Get the SQL column name from the given Model field name.

            :param field_name: str - Model field name
            :return: Optional[str] - SQL column name if field name exists in Model and if SQL column names is defined
            """
            for name, field in cls.columns.items():
                if field.name == field_name:
                    return name

    @classmethod
    def loads(cls, record: SQLRecord) -> "SQLModel":
        """
        Creates a new SQLModel instance from a SQLRecord.

        :param record: SQLRecord - SQL raw record
        :returns: SQLModel - initialized and validated model
        """
        model = cls()

        for column in record.columns:
            value = record.record.get(column)
            field = cls.META.columns.get(column)
            if field:
                t = cls.get_cls_from_field(field.name)
                setattr(model, field.name, t(value))

        model.validate()
        return model

    @classmethod
    def get_cls_from_field(cls, field_name: str) -> Optional[type]:
        """
        Get class type from the given field name in the model.
        The field must be annotated, declared in the children class.

        Example:
        >>> class User(SQLModel):
        >>>     uid: int  # This is an annotated field

        So, if we use this method:
        >>> User.get_cls_from_field('uid')  # This will return: <type: 'int'>

        :param field_name: str - field name to examine
        :return: Optional[type] - type class of the field
        """
        for field in cls.__annotations__.keys():
            if field == field_name:
                return cls.__annotations__[field]

    def validate(self):
        """
        Validates model against the META inner class.
        """
        meta = getattr(self, "META")
        if not meta:
            raise KeyError("Missing META in SQLModel")

        if not meta.table_name:
            raise KeyError("Missing table_name in META for SQLModel")

        if not meta.pk:
            raise KeyError("Missing pk in META for SQLModel")

        if not meta.pk.field:
            raise KeyError("Missing pk.field in META for SQLModel")

        if meta.pk.field not in get_annotated_fields(type(self)):
            raise KeyError(f"{meta.pk.field} is not a field in SQLModel")

        if not meta.columns.get(meta.get_pk()):
            raise KeyError("Missing pk.column in META for SQLModel")

    @property
    def pk(self) -> Optional[Any]:
        """
        Get Model's Primary Key value
        """
        return getattr(self, self.META.pk.field)

    def __eq__(self, other: Optional["Model"]) -> bool:
        """
        Override __eq__ method for any Model
        """
        if other is None:
            return False

        return all(
            [getattr(self, field, None) == getattr(other, field, None) for field in type(self).__annotations__.keys()]
        )
