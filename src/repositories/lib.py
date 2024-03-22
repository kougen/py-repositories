
class Entity:
    def __init__(self, id):
        self.id = id


class FilterField:
    def __init__(self, name, field_type, default=None):
        self.name = name
        self.field_type = field_type
        self.default = default

    def serialize(self) -> dict[str, tuple]:
        return {
            self.name : (self.field_type, self.default)
        }
