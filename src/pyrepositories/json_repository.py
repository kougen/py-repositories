from .datatable import DataTable
from jsonservice import JsonService
from .lib import Entity, IdTypes, EntityField, FieldBase
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

        for content in current_content:
            entity = convert_to_entity(content, fields)
            if not entity:
                print(f"Could not convert entity: {content}")
                continue
            for field in entity.get_fields():
                if entity.id is not None:
                    self.fields[field.name].set_value(entity.id, field.value)

    def get_all(self):
        content = self.json_service.read('content') or []
        entities = []
        for item in content:
            entities.append(convert_to_entity(item, self.field_structure))
        return entities

    def get_by_id(self, entity_id: IdTypes) -> Entity | None:
        content = self.json_service.read('content') or []
        for item in content:
            if item['id'] == entity_id:
                return item
        return None

    def insert(self, data: Entity) -> Entity | None:
        result = super().insert(data)
        if not result:
            return None
        content = self.json_service.read('content') or []
        content.append(result.serialize())
        self.json_service.write('content', content)
        return result

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
