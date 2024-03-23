from .datatable import DataTable
from jsonservice import JsonService
from .datasource import DataSource
from .lib import Entity, filter_by_fields
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
    def __init__(self, name: str, store_path: str):
        super().__init__(name)
        file_path = os.path.join(store_path, f'{name}.json')
        self.json_service = JsonService(file_path)
        current_content = self.json_service.read('content')

        if not current_content:
            self.json_service.write('content', [])

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

    def get_by_filter(self, filter: dict):
        content = self.json_service.read('content') or []
        entities = []
        for item in content:
            entities.append(convert_to_entity(item))
        return filter_by_fields(entities, filter)

    def insert(self, data: Entity):
        content = self.json_service.read('content') or []
        content.append(data.serialize())
        self.json_service.write('content', content)
        return True

    def update(self, id, data: Entity):
        content = self.json_service.read('content') or []  # type: list[dict]
        for index, item in enumerate(content):
            if item['id'] == id:
                content[index] = data.serialize()
                self.json_service.write('content', content)
                return True
        return False

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
