from typing import Any
from enum import Enum


class IdTypes(Enum):
    INT = int
    STR = str
    UUID = 'uuid'


class Entity:
    def __init__(self, id: int | str | None = None):
        self.id = id
        self.fields = {}

    def add_field(self, name: str, value: Any):
        self.fields[name] = value

    def get_field(self, name: str) -> Any:
        return self.fields.get(name)

    def has_value(self, filter: dict) -> bool:
        for key, value in filter.items():
            if value is None or value != "":
                continue
            if key not in self.fields:
                continue
            if value in self.fields[key]:
                return True
        return False

    def serialize(self) -> dict[str, Any]:
        return {
            'id': self.id,
            **self.fields
        }
 
    def __str__(self):
        return str(self.serialize())

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
