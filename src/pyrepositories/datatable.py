from .lib import Entity, filter_by_fields, FieldKeyTypes, FieldBase, TableField, IdTypes, Filter, FieldValue
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

    def get_by_id(self, entity_id: int | str) -> Entity | None:
        """Get entity by id from the data source while updating the fields"""

        print("Override this method in child class")
        return None

    def get_unique(self, key: str, value: Any) -> Entity | None:
        """Get entity by unique key from the data source"""

        print("Override this method in child class")
        return None

    def get_by_filter(self, filters: Filter) -> list[Entity]:
        print(f'Filter: {filters}')
        entities = self.get_all()
        return filter_by_fields(entities, filters)

    def insert(self, data: Entity) -> Entity | None:
        return self._insert(data, self.get_all())

    def insert_many(self, data: list[Entity]) -> list[Entity] | None:
        entities = self.get_all()
        for entity in data:
            self._insert(entity, entities)
        return data

    def update(self, entity_id, data: Entity) -> Entity | None:
        print("Override this method in child class")
        return None

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

    def _get_unique(self, field_name: str, value: Any) -> FieldValue | None:
        for field in [field for field in self.fields.values() if field.key_type == FieldKeyTypes.UNIQUE]:
            if field.name == field_name:
               return field.get_unique(value)
        print(f"No record found with {field_name} = {value}")
        return None

    def _refresh_fields(self):
        entities = self.get_all()
        for entity in entities:
            for field in entity.get_fields():
                if entity.id is not None:
                    self.fields[field.name].set_value(entity.id, field.value)
