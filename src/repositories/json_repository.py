from .datatable import DataTable
from jsonservice import JsonService
from .datasource import DataSource
import os

class JsonTable(DataTable):
    def __init__(self, name: str, store_path: str):
        super().__init__(name)
        file_path = os.path.join(store_path, f'{name}.json')
        self.json_service = JsonService(file_path)
        current_content = self.json_service.read('content')

        if not current_content:
            self.json_service.write('content', [])

    def get_all(self):
        return self.json_service.read('content') or []

    def get_by_id(self, id):
        content = self.json_service.read('content') or []
        for item in content:
            if item['id'] == id:
                return item
        return None

    def get_by_filter(self, filter: dict):
        content = self.json_service.read('content') or []
        result = []
        for item in content:
            match = True
            for key, value in filter.items():
                if item.get(key) != value:
                    match = False
                    break
            if match:
                result.append(item)
        return result

    def insert(self, data):
        content = self.json_service.read('content') or []
        content.append(data)
        self.json_service.write('content', content)
        return True

    def update(self, id, data):
        content = self.json_service.read('content') or []
        for index, item in enumerate(content):
            if item['id'] == id:
                content[index] = data
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
