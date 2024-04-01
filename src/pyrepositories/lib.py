from typing import Any
from enum import Enum


class IdTypes(Enum):
    INT = int
    STR = str
    UUID = 'uuid'


class FieldKeyTypes(Enum):
    PRIMARY = 0
    UNIQUE = 1
    REQUIRED = 2
    STANDARD = 3
    OPTIONAL = 4

    def __lt__(self, other):
        return self.value < other.value

    def __gt__(self, other):
        return self.value > other.value

    def __eq__(self, other):
        return self.value == other.value

    def __le__(self, other):
        return self.value <= other.value

    def __ge__(self, other):
        return self.value >= other.value

class FilterTypes(Enum):
    EQUAL = 0
    NOT_EQUAL = 1
    GREATER_THAN = 2
    LESS_THAN = 3
    GREATER_THAN_OR_EQUAL = 4
    LESS_THAN_OR_EQUAL = 5
    IN = 6
    NOT_IN = 7
    LIKE = 8
    NOT_LIKE = 9
    IS_NULL = 10
    IS_NOT_NULL = 11
    CONTAINS = 12
    NOT_CONTAINS = 13

class FilterCombination(Enum):
    AND = 0
    OR = 1


class FilterCondition:
    def __init__(self, key: str, value: Any, filter_type: FilterTypes = FilterTypes.EQUAL):
        self.key = key
        self.value = value
        self.filter_type = filter_type

    def __str__(self):
        return f"{self.key} {self.filter_type} {self.value}"

    def __repr__(self):
        return self.__str__()

class Filter:
    def __init__(self, conditions: list[FilterCondition], combination: FilterCombination = FilterCombination.AND):
        self.conditions = conditions
        self.combination = combination

    def __str__(self):
        return f"{self.combination} {self.conditions}"

    def __repr__(self):
        return self.__str__()

class FieldTypes(Enum):
    INT = int
    STR = str
    UUID = 'uuid'
    BOOL = bool
    FLOAT = float
    LIST = list
    DICT = dict


class FieldValue:
    def __init__(self, value: Any, entity_id: int | str):
        self.entity_id = entity_id
        self.value = value


class FieldBase:
    def __init__(self, name: str, field_type: FieldTypes, key_type: FieldKeyTypes, default: Any = None):
        self.name = name
        self.field_type = field_type
        self.key_type = key_type
        self.default = default

    def __str__(self):
        return f"{self.name} ({self.field_type}, {self.key_type})"

    def __repr__(self):
        return self.__str__()

    def serialize(self) -> dict[str, tuple]:
        return {
            self.name : (self.field_type, self.key_type, self.default)
        }



class TableField:
    def __init__(self, field: FieldBase):
        self.name = field.name
        self.field_type = field.field_type
        self.key_type = field.key_type
        self.default = field.default
        if self.key_type == FieldKeyTypes.OPTIONAL and self.default is None:
            raise ValueError(f"Field {self.name} is optional but has no default value")
        self.values = {}  # type: dict[int | str, FieldValue]

    def set_value(self, entity_id: int | str, value: Any = None):
        if self.key_type == FieldKeyTypes.REQUIRED and value is None:
            raise ValueError(f"Field {self.name} is required")

        if self.key_type == FieldKeyTypes.UNIQUE:
            if value in self.values.values():
                raise ValueError(f"Value {value} already exists in field {self.name}")

        self.values[entity_id] = FieldValue(value, entity_id)

    def get_value(self, entity_id: int | str) -> Any | None:
        return self.values.get(entity_id)

    def get_unique(self, value: Any) -> FieldValue | None:
        if self.key_type != FieldKeyTypes.UNIQUE:
            raise ValueError(f"Field {self.name} is not unique")
        for field_value in self.values.values():
            if field_value.value == value:
                return field_value
        return None

    def serialize(self) -> dict[str, tuple]:
        return {
            self.name: (self.field_type, self.key_type, self.default)
        }

    def __str__(self):
        return f"{self.name} ({self.field_type}, {self.key_type})"


class EntityField:
    def __init__(self, field: FieldBase, value: Any = None):
        self.value = value
        self.name = field.name
        self.field_type = field.field_type
        self.key_type = field.key_type
        self.default = field.default

        if self.key_type == FieldKeyTypes.OPTIONAL and self.default is None:
            raise ValueError(f"Field {self.name} is optional but has no default value")

        if self.value is None and self.default is not None:
            self.value = self.default

        if self.key_type < FieldKeyTypes.STANDARD and self.value is None:
            raise ValueError(f"Field {self.name} is required but has no value")

    def serialize(self) -> dict[str, tuple]:
        return {
            self.name: (self.field_type, self.key_type, self.default)
        }

    def __str__(self):
        return f"{self.name} ({self.field_type}, {self.key_type})"


class Error:
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.__str__()


class Entity:
    def __init__(self, fields: list[EntityField], id: int | str | None = None):
        self.id = id
        self.__fields = {}  # type: dict[str, EntityField]
        for field in fields:
            self.__fields[field.name] = field
        self.errors = []  # type: list[Error]

    def add_field(self, name: str, field: EntityField):
        self.__fields[name] = field

    def get_field(self, name: str) -> EntityField | None:
        return self.__fields.get(name)

    def get_field_value(self, name: str) -> Any:
        return self.__fields[name].value

    def set_field_value(self, name: str, value: Any):
        self.__fields[name].value = value

    def get_fields(self):
        fields = []
        for field in self.__fields.values():
            fields.append(field)
        return fields

    def matches_condition(self, key: str, value: Any, filter_type: FilterTypes) -> bool:
        field = self.get_field(key)
        if not field:
            return False

        if value == field.default or value is None or value == '' or value == []:
            return True

        if filter_type == FilterTypes.EQUAL:
            return field.value == value
        if filter_type == FilterTypes.NOT_EQUAL:
            return field.value != value
        if filter_type == FilterTypes.GREATER_THAN:
            return field.value > value
        if filter_type == FilterTypes.LESS_THAN:
            return field.value < value
        if filter_type == FilterTypes.GREATER_THAN_OR_EQUAL:
            return field.value >= value
        if filter_type == FilterTypes.LESS_THAN_OR_EQUAL:
            return field.value <= value
        if filter_type == FilterTypes.IN and isinstance(value, list):
            return field.value in value
        if filter_type == FilterTypes.NOT_IN and isinstance(value, list):
            return field.value not in value
        if filter_type == FilterTypes.IS_NULL:
            return field.value is None
        if filter_type == FilterTypes.IS_NOT_NULL:
            return field.value is not None
        if filter_type == FilterTypes.LIKE or filter_type == FilterTypes.CONTAINS:
            return value in field.value
        if filter_type == FilterTypes.NOT_LIKE or filter_type == FilterTypes.NOT_CONTAINS:
            return value not in field.value

    def matches_criteria(self, filter: Filter) -> bool:
        results = []
        for condition in filter.conditions:
            results.append(self.matches_condition(condition.key, condition.value, condition.filter_type))

        if filter.combination == FilterCombination.AND:
            return all(results)
        if filter.combination == FilterCombination.OR:
            return any(results)

        raise ValueError(f"Invalid filter combination {filter.combination}")
                

    def has_value(self, filter: Filter) -> bool:
        return self.matches_criteria(filter)

    def validate(self) -> bool:
        for field in self.__fields.values():
            if field.key_type < FieldKeyTypes.STANDARD and field.value is None:
                self.errors.append(Error(f"Field {field.name} is required"))
                return False
        return True

    def print_errors(self):
        for error in self.errors:
            print(error)

    def serialize(self) -> dict[str, Any]:
        data = {}
        data['id'] = self.id
        for field in self.__fields.values():
            data[field.name] = field.value
        return data
 
    def __str__(self):
        return str(self.serialize())

    def __repr__(self):
        return self.__str__()


def filter_by_fields(data: list[Entity], filter: Filter) -> list[Entity]:
    result = []
    for item in data:
        if item.has_value(filter):
            result.append(item)
    return result
