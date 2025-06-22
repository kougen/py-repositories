from typing import Any

from .datatable import DataTable
from .datasource import DataSource
from .lib import Entity, IdTypes, EntityField, FieldBase, Filter


class PgTable(DataTable):
    def __init__(self, name: str, fields: list[FieldBase]):
        super().__init__(name, fields)

    def get_name(self) -> str:
        return super().get_name()

    def get_all(self) -> list[Entity]:
        return super().get_all()

    def get_by_id(self, entity_id: int | str) -> Entity | None:
        return super().get_by_id(entity_id)

    def get_unique(self, key: str, value: Any) -> Entity | None:
        return super().get_unique(key, value)

    def get_by_filter(self, filters: Filter) -> list[Entity]:
        return super().get_by_filter(filters)

    def insert(self, data: Entity) -> Entity | None:
        return super().insert(data)

    def insert_many(self, data: list[Entity]) -> list[Entity] | None:
        return super().insert_many(data)

    def update(self, entity_id, data: Entity) -> Entity | None:
        return super().update(entity_id, data)

    def delete(self, entity_id: IdTypes) -> bool:
        return super().delete(entity_id)

    def clear(self) -> bool:
        return super().clear()


class PgRepository(DataSource):
    def __init__(self, auto_increment=True, id_type: IdTypes = IdTypes.INT):
        super().__init__(auto_increment, id_type)

    def add_table(self, table: DataTable):
        super().add_table(table)

    def drop(self, table_name: str):
        return super().drop(table_name)

    def get_table(self, name: str) -> DataTable | None:
        return super().get_table(name)

    def get_all(self, table_name: str):
        return super().get_all(table_name)

    def get_by_id(self, table_name: str, _id: int | str):
        return super().get_by_id(table_name, _id)

    def get_by_filter(self, table_name: str, _filter: Filter):
        return super().get_by_filter(table_name, _filter)

    def get_by_filters(self, table_name: str, filters: list[Filter]):
        return super().get_by_filters(table_name, filters)

    def get_unique(self, table_name: str, field_name: str, value: any):
        return super().get_unique(table_name, field_name, value)

    def insert(self, table_name: str, data: Entity):
        return super().insert(table_name, data)

    def update(self, table_name, _id: int | str, data: Entity):
        return super().update(table_name, _id, data)

    def delete(self, table_name, _id):
        return super().delete(table_name, _id)

    def clear(self, table_name):
        return super().clear(table_name)
