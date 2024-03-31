from typing import Any
from enum import Enum


class IdTypes(Enum):
    INT = int
    STR = str
    UUID = 'uuid'

class FieldKeyTypes(Enum):
    PRIMARY = 'primary'
    UNIQUE = 'unique'
    STANDARD = 'standard'
    REQUIRED = 'required'
    OPTIONAL = 'optional'

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

class Field:
    def __init__(self, name: str, field_type: FieldTypes, key_type: FieldKeyTypes, default: Any = None):
        self.name = name
        self.field_type = field_type
        self.key_type = key_type
        self.default = default
        if key_type == FieldKeyTypes.OPTIONAL and default is None:
            raise ValueError(f"Field {name} is optional but has no default value")
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

    def __str__(self):
        return f"{self.name} ({self.field_type}, {self.key_type})"

    def __repr__(self):
        return self.__str__()

    def serialize(self) -> dict[str, tuple]:
        return {
            self.name : (self.field_type, self.key_type, self.default)
        }

class EntityField:
    def __init__(self, name: str, field_type: FieldTypes, key_type: FieldKeyTypes, value: Any = None, default: Any = None):
        self.name = name
        self.field_type = field_type
        self.key_type = key_type
        self.default = default
        self.value = value

    def serialize(self) -> dict[str, tuple]:
        return {
            self.name : (self.field_type, self.key_type, self.default)
        }

class Entity:
    def __init__(self, id: IdTypes | None = None):
        self.id = id
        self.fields = {}  # type: dict[str, EntityField]

    def add_field(self, name: str, field: EntityField):
        self.fields[name] = field

    def get_field(self, name: str) -> EntityField | None:
        return self.fields.get(name)

    def matches_criteria(self, key: str, value: str) -> bool:
        if isinstance(self.fields[key], str):
            return value.lower() in self.fields[key].value.lower()
        else:
            return value == self.fields[key]

    def has_value(self, filter: dict) -> bool:
        for key, value in filter.items():
            if not self.matches_criteria(key, value):
                return False
        return True

    def serialize(self) -> dict[str, Any]:
        data = {}
        data['id'] = self.id
        for field in self.fields.values():
            data[field.name] = field.value
        return data
 
    def __str__(self):
        return str(self.serialize())

    def __repr__(self):
        return self.__str__()


class FilterField:
    def __init__(self, name, field_type, default=None):
        self.name = name
        self.field_type = field_type
        self.default = default

    def serialize(self) -> dict[str, tuple]:
        return {
            self.name : (self.field_type, self.default)
        }


def filter_by_fields(data: list[Entity], filter: dict) -> list[Entity]:
    result = []
    for item in data:
        if item.has_value(filter):
            result.append(item)
    return result
