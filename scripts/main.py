import os
import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(os.path.join(path_root, 'src'))

from pyrepositories import DataSource, JsonTable, Entity, FieldBase, FieldTypes, FieldKeyTypes, EntityField, Filter, FilterCondition, FilterTypes, FilterCombination


fields = [
    FieldBase('name', FieldTypes.STR, FieldKeyTypes.REQUIRED),
    FieldBase('email', FieldTypes.STR, FieldKeyTypes.UNIQUE),
    FieldBase('username', FieldTypes.STR, FieldKeyTypes.UNIQUE),
    FieldBase('comment', FieldTypes.STR, FieldKeyTypes.OPTIONAL, '')
]


class User(Entity):
    def __init__(self, name: str, email: str, username: str | None = None):
        entity_fields = [
            EntityField(fields[0], name),
            EntityField(fields[1], email),
            EntityField(fields[2], username),
            EntityField(fields[3])
        ]
        super().__init__(entity_fields)
        self.name = name
        self.email = email
        self.username = username

    @property
    def name(self):
        return self.get_field_value('name')

    @property
    def email(self):
        return self.get_field_value('email')

    @property
    def username(self):
        return self.get_field_value('username')

    @name.setter
    def name(self, name):
        self.set_field_value('name', name)

    @email.setter
    def email(self, email):
        self.set_field_value('email', email)

    @username.setter
    def username(self, username):
        self.set_field_value('username', username)


datasource = DataSource()
table = JsonTable('users', os.path.join(path_root, 'scripts', 'data'), fields)
datasource.add_table(table)

datasource.clear('users')

dummy_users = [
    User('John Doe', 'test@asd.com', 'johndoe'),
    User('Jane Doe', 'test3@asd.com', 'janedoe'),
    User('Mary Poppins', 'poppinst@industry.com', 'marypoppins'),
]

for user in dummy_users:
    datasource.insert('users', user)

filters = [
    Filter([
        FilterCondition('name', 'Doe', FilterTypes.CONTAINS),
        FilterCondition('email', 'test@asd.com', FilterTypes.EQUAL)
    ]),
    Filter([
        FilterCondition('name', 'Mary', FilterTypes.CONTAINS),
    ])
]

for user in datasource.get_by_filters('users', filters):
    print(user)

print("Unique") 
mary = datasource.get_unique('users', 'username', 'marypoppins')
print(mary)

print(fields[0].field_type.content_type)

first_user = datasource.get_all('users')[0]
d_result = datasource.delete('users', fist_user.id)
print(d_result)
print("After delete")
print(datasource.get_all('users'))

