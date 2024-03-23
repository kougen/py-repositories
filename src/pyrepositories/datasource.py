from .datatable import DataTable

class DataSource:
    def __init__(self):
        self.tables = [] #type: list[DataTable]

    def add_table(self, table: DataTable):
        if table not in self.tables:
            self.tables.append(table)

    def remove_table(self, table):
        if table in self.tables:
            self.tables.remove(table)

    def get_table(self, name) -> DataTable | None:
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

    def get_by_id(self, table_name: str, id):
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

    def insert(self, table_name: str, data):
        table = self.get_table(table_name)
        if table:
            return table.insert(data)
        else:
            return None

    def update(self, table_name, id, data):
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
