from .datatable import DataTable
from .lib import Entity, IdTypes
import random
import string
from uuid import uuid4 as get_uuid


def get_random_string_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))


def get_sequential_id(data):
    return len(data) + 1


def get_id(id_type: IdTypes, data: list[Entity]):
    if id_type == IdTypes.INT:
        return get_sequential_id(data)
    elif id_type == IdTypes.STR:
        return get_random_string_id()
    elif id_type == IdTypes.UUID:
        return str(get_uuid())
    else:
        raise ValueError("Invalid id_type")


class DataSource:
    def __init__(self, auto_increment=True, id_type: IdTypes = IdTypes.INT):
        if id_type not in IdTypes:
            raise ValueError("Invalid id_type")

        self.id_type = id_type
        self.tables = [] #type: list[DataTable]
        self.auto_increment = auto_increment

    def add_table(self, table: DataTable):
        if table not in self.tables:
            self.tables.append(table)

    def drop(self, table_name: str):
        for table in self.tables:
            if table.get_name() == table_name:
                self.tables.remove(table)
                return True

        return False

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

    def clear(self, table_name):
        table = self.get_table(table_name)
        if table:
            return table.clear()
        else:
            return None
