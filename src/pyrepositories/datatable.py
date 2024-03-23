from .lib import Entity, FilterField
from typing import Any

class DataTable:
    def __init__(self, name):
        self.name = name
        self.filter_fields = [] #type: list[FilterField]

    def set_filter_fields(self, fields: dict[str, tuple]):
        for key, value in fields.items():
            if not isinstance(value, tuple):
                raise ValueError("Value must be a tuple")
            default = None
            if len(value) == 2:
                default = value[1]
            if len(value) > 2:
                raise ValueError("Value must be a tuple of length 2")
            self.filter_fields.append(FilterField(key, value[0], default))

    def add_filter_field(self, field: FilterField):
        self.filter_fields.append(field)

    def get_filter_fields(self):
        formatted = {}
        for field in self.filter_fields:
            formatted.update(field.serialize())
        return formatted

    def get_name(self) -> str:
        return self.name

    def get_all(self) -> list:
        print("Override this method in child class")
        return []

    def get_by_id(self, id) -> Any | None:
        print("Override this method in child class")
        return None

    def get_by_filter(self, filter: dict) -> list:
        print("Override this method in child class")
        return []

    def insert(self, data: Entity) -> bool:
        print("Override this method in child class")
        return False

    def update(self, id, data: Entity) -> bool:
        print("Override this method in child class")
        return False

    def delete(self, id) -> bool:
        print("Override this method in child class")
        return False

    def clear(self) -> bool:
        print("Override this method in child class")
        return False
