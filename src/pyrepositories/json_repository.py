from .datatable import DataTable
from jsonservice import JsonService
from .datasource import DataSource
from .lib import Entity, Field
import os

def convert_to_entity(data: dict) -> Entity:
    if 'id' not in data:
        raise ValueError("Entity must have an id")

    entity = Entity(data['id'])
    for key, value in data.items():
        if key != 'id':
            entity.add_field(key, value)
    return entity

class JsonTable(DataTable):
    def __init__(self, name: str, store_path: str, fields: list[Field], create_if_not_exists: bool = False):
        super().__init__(name, fields)
        file_path = os.path.join(store_path, f'{name}.json')
        self.json_service = JsonService(file_path, create_if_not_exists=create_if_not_exists)
        current_content = self.json_service.read('content')

        if not current_content:
            self.json_service.write('content', [])
            current_content = []

        for content in current_content:
            entity = convert_to_entity(content)
            for field in entity.fields.values():
                if entity.id is not None:
                    self.fields[field.name].set_value(entity.id, field.value)

    def get_all(self):
        content = self.json_service.read('content') or []
        entities = []
        for item in content:
            entities.append(convert_to_entity(item))
        return entities

    def get_by_id(self, id):
        content = self.json_service.read('content') or []
        for item in content:
            if item['id'] == id:
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

    def update(self, id, data: Entity) -> Entity | None:
        result = super().update(id, data)
        if not result:
            return None
        content = self.json_service.read('content') or []  # type: list[dict]
        for index, item in enumerate(content):
            if item['id'] == id:
                content[index] = result.serialize()
                self.json_service.write('content', content)
                return result
        return None

    def delete(self, id):
        content = self.json_service.read('content') or []
        for index, item in enumerate(content):
            if item['id'] == id:
                del content[index]
                self.json_service.write('content', content)
                return True
        return False

    def clear(self):
        self.json_service.write('content', [])
        return True
