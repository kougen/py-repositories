from .datatable import DataTable
from .lib import Entity
import random
import string


def get_random_string_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


def get_sequential_id(data):
    return len(data) + 1


def get_id(id_type, data):
    if id_type == int:
        return get_sequential_id(data)
    else:
        return get_random_string_id()


class DataSource:
    def __init__(self, auto_increment=True, id_type=int):
        if id_type not in [int, str]:
            raise ValueError("id_type must be either int or str")

        self.id_type = id_type
        self.tables = [] #type: list[DataTable]
        self.auto_increment = auto_increment

    def add_table(self, table: DataTable):
        if table not in self.tables:
            self.tables.append(table)

    def remove_table(self, table):
        if table in self.tables:
            self.tables.remove(table)

    def get_table(self, name: str) -> DataTable | None:
        for table in self.tables:
            if table.get_name() == name:
                return table

        return None

    def get_all(self, table_name: str):
        table = self.get_table(table_name)
        if table:
            return table.get_all()
        else:
            return None

    def get_by_id(self, table_name: str, id: int | str):
        table = self.get_table(table_name)
        if table:
            return table.get_by_id(id)
        else:
            return None

    def get_by_filter(self, table_name: str, filter: dict):
        table = self.get_table(table_name)
        if table:
            return table.get_by_filter(filter)
        else:
            return None

    def insert(self, table_name: str, data: Entity):
        table = self.get_table(table_name)
        if not table:
            raise ValueError("Table not found")

        if self.auto_increment:
            data.id = get_id(self.id_type, table.get_all())
        else:
            if not data.id:
                raise ValueError("Entity must have an id")
            if table.get_by_id(data.id):
                return False
        return table.insert(data)

    def update(self, table_name, id: int | str, data: Entity):
        table = self.get_table(table_name)
        if table:
            return table.update(id, data)
        else:
            return None

    def delete(self, table_name, id):
        table = self.get_table(table_name)
        if table:
            return table.delete(id)
        else:
            return None
