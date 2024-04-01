from typing import Any
from .datatable import DataTable
from jsonservice import JsonService
from .lib import Entity, IdTypes, EntityField, FieldBase, Filter
import os


def convert_to_entity(data: dict, fields: list[FieldBase]) -> Entity | None:
    if 'id' not in data:
        raise ValueError("Entity must have an id")

    fields_dict = {field.name: field for field in fields}
    entity_fields = []
    for key, field in fields_dict.items():
        entity_fields.append(EntityField(field, data.get(key)))
    entity = Entity(entity_fields, data['id'])
    if entity.validate():
        return entity

    entity.print_errors()
    return None


class JsonTable(DataTable):
    def __init__(self, name: str, store_path: str, fields: list[FieldBase], create_if_not_exists: bool = True):
        super().__init__(name, fields)
        file_path = os.path.join(store_path, f'{name}.json')
        self.json_service = JsonService(file_path, create_if_not_exists=create_if_not_exists)
        current_content = self.json_service.read('content')

        if not current_content:
            self.json_service.write('content', [])
            current_content = []

        self._refresh_fields()

    def get_all(self):
        content = self.json_service.read('content') or []
        entities = []
        for item in content:
            entities.append(convert_to_entity(item, self.field_structure))

        return entities

    def get_by_id(self, entity_id: int | str) -> Entity | None:
        content = self.json_service.read('content') or []
        for item in content:
            if item['id'] == entity_id:
                return convert_to_entity(item, self.field_structure)
        return None

    def get_unique(self, key: str, value: Any) -> Entity | None:
        field_value = self._get_unique(key, value)
        if not field_value:
            return None

        entity = self.get_by_id(field_value.entity_id)
        if not entity:
            return None
        return entity

    def insert(self, data: Entity) -> Entity | None:
        result = super().insert(data)
        if not result:
            return None
        content = self.json_service.read('content') or []
        content.append(result.serialize())
        self.json_service.write('content', content)
        return result

    def insert_many(self, data: list[Entity]) -> list[Entity] | None:
        results = []
        for entity in data:
            result = self.insert(entity)
            if not result:
                return None
            results.append(result)
        return results

    def update(self, entity_id, data: Entity) -> Entity | None:
        result = super().update(entity_id, data)
        if not result:
            return None
        content = self.json_service.read('content') or []  # type: list[dict]
        for index, item in enumerate(content):
            if item['id'] == entity_id:
                content[index] = result.serialize()
                self.json_service.write('content', content)
                return result
        return None

    def delete(self, entity_id: IdTypes) -> bool:
        content = self.json_service.read('content') or []
        for index, item in enumerate(content):
            if item['id'] == entity_id:
                del content[index]
                self.json_service.write('content', content)
                return True
        return False

    def clear(self):
        self.json_service.write('content', [])
        return True
