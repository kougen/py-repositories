from .lib import Entity, filter_by_fields, FieldKeyTypes, FieldBase, TableField, IdTypes
from typing import Any


class DataTable:
    def __init__(self, name, field_structure: list[FieldBase]):
        self.name = name
        self.field_structure = field_structure
        self.fields = {}  # type: dict[str, TableField]

        for field in field_structure:
            self.fields[field.name] = TableField(field)

    def get_name(self) -> str:
        return self.name

    def get_all(self) -> list[Entity]:
        """Get all entities from the data source while updating the fields"""

        print("Override this method in child class")
        return []

    def get_by_id(self, entity_id) -> Entity | None:
        """Get entity by id from the data source while updating the fields"""

        print("Override this method in child class")
        return None

    def get_by_filter(self, filter: dict) -> list[Entity]:
        print(f'Filter: {filter}')
        entities = self.get_all()
        return filter_by_fields(entities, filter)

    def get_unique(self, field_name: str, value: Any) -> Entity | None:
        print("Override this method in child class")
        return None

    def insert(self, data: Entity) -> Entity | None:
        self._insert(data, self.get_all())

    def insert_many(self, data: list[Entity]) -> list[Entity] | None:
        entities = self.get_all()
        for entity in data:
            self._insert(entity, entities)
        return data

    def update(self, entity_id, data: Entity) -> Entity | None:
        print("Override this method in child class")

    def delete(self, entity_id: IdTypes) -> bool:
        print("Override this method in child class")
        return False

    def clear(self) -> bool:
        print("Override this method in child class")
        return False

    def _insert(self, data: Entity, content: list[Entity]) -> Entity | None:
        content_dict = {}
        for item in content:
            content_dict[item.id] = item

        if not data.id:
            raise ValueError("Entity must have an id")
        if data.id in content_dict:
            raise ValueError("Entity already exists")
        for field in data.get_fields():
            self.fields[field.name].set_value(data.id, field.value)
        return data
