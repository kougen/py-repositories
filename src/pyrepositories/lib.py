from typing import Any
from enum import Enum


class IdTypes(Enum):
    INT = int
    STR = str
    UUID = 'uuid'


class FieldKeyTypes(Enum):
    PRIMARY = 0
    UNIQUE = 1
    REQUIRED = 2
    STANDARD = 3
    OPTIONAL = 4

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value


class FieldTypes(Enum):
    INT = int
    STR = str
    UUID = 'uuid'
    BOOL = bool
    FLOAT = float
    LIST = list
    DICT = dict


class FieldValue:
    def __init__(self, value: Any, entity_id: IdTypes):
        self.entity_id = entity_id
        self.value = value


class FieldBase:
    def __init__(self, name: str, field_type: FieldTypes, key_type: FieldKeyTypes, default: Any = None):
        self.name = name
        self.field_type = field_type
        self.key_type = key_type
        self.default = default

    def __str__(self):
        return f"{self.name} ({self.field_type}, {self.key_type})"

    def __repr__(self):
        return self.__str__()

    def serialize(self) -> dict[str, tuple]:
        return {
            self.name : (self.field_type, self.key_type, self.default)
        }



class TableField:
    def __init__(self, field: FieldBase):
        self.name = field.name
        self.field_type = field.field_type
        self.key_type = field.key_type
        self.default = field.default
        if self.key_type == FieldKeyTypes.OPTIONAL and self.default is None:
            raise ValueError(f"Field {self.name} is optional but has no default value")
        self.values = {}  # type: dict[IdTypes, FieldValue]

    def set_value(self, entity_id: IdTypes, value: Any = None):
        if self.key_type == FieldKeyTypes.REQUIRED and value is None:
            raise ValueError(f"Field {self.name} is required")

        if self.key_type == FieldKeyTypes.UNIQUE:
            if value in self.values.values():
                raise ValueError(f"Value {value} already exists in field {self.name}")

        self.values[entity_id] = FieldValue(value, entity_id)

    def get_value(self, entity_id: IdTypes) -> Any | None:
        return self.values.get(entity_id)

    def serialize(self) -> dict[str, tuple]:
        return {
            self.name: (self.field_type, self.key_type, self.default)
        }

    def __str__(self):
        return f"{self.name} ({self.field_type}, {self.key_type})"


class EntityField:
    def __init__(self, field: FieldBase, value: Any = None):
        self.value = value
        self.name = field.name
        self.field_type = field.field_type
        self.key_type = field.key_type
        self.default = field.default

        if self.key_type == FieldKeyTypes.OPTIONAL and self.default is None:
            raise ValueError(f"Field {self.name} is optional but has no default value")

        if self.value is None and self.default is not None:
            self.value = self.default

        if self.key_type < FieldKeyTypes.STANDARD and self.value is None:
            raise ValueError(f"Field {self.name} is required but has no value")

    def serialize(self) -> dict[str, tuple]:
        return {
            self.name: (self.field_type, self.key_type, self.default)
        }

    def __str__(self):
        return f"{self.name} ({self.field_type}, {self.key_type})"


class Error:
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.__str__()


class Entity:
    def __init__(self, fields: list[EntityField], id: IdTypes | None = None):
        self.id = id
        self.__fields = {}  # type: dict[str, EntityField]
        for field in fields:
            self.__fields[field.name] = field
        self.errors = []  # type: list[Error]

    def add_field(self, name: str, field: EntityField):
        self.__fields[name] = field

    def get_field(self, name: str) -> EntityField | None:
        return self.__fields.get(name)

    def get_field_value(self, name: str) -> Any:
        return self.__fields[name].value

    def set_field_value(self, name: str, value: Any):
        self.__fields[name].value = value

    def get_fields(self):
        fields = []
        for field in self.__fields.values():
            fields.append(field)
        return fields

    def matches_criteria(self, key: str, value: str) -> bool:
        field = self.get_field(key)
        if not field:
            return False
        if field.value != value:
            return False
        return True

    def has_value(self, filter: dict) -> bool:
        for key, value in filter.items():
            if not self.matches_criteria(key, value):
                return False
        return True

    def validate(self) -> bool:
        for field in self.__fields.values():
            if field.key_type < FieldKeyTypes.STANDARD and field.value is None:
                self.errors.append(Error(f"Field {field.name} is required"))
                return False
        return True

    def print_errors(self):
        for error in self.errors:
            print(error)

    def serialize(self) -> dict[str, Any]:
        data = {}
        data['id'] = self.id
        for field in self.__fields.values():
            data[field.name] = field.value
        return data
 
    def __str__(self):
        return str(self.serialize())

    def __repr__(self):
        return self.__str__()


def filter_by_fields(data: list[Entity], filter: dict) -> list[Entity]:
    result = []
    for item in data:
        if item.has_value(filter):
            result.append(item)
    return result
