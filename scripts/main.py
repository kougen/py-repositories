import os
import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(os.path.join(path_root, 'src'))

from pyrepositories import DataSource, JsonTable, Entity, IdTypes, FilterField, Field, FieldKeyTypes, FieldTypes


class User(Entity):
    def __init__(self, name, email):
        self.fields = {
            'name': name,
            'email': email
        }

    @property
    def name(self):
        return self.fields.get('name')

    @property
    def email(self):
        return self.fields.get('email')

    @name.setter
    def name(self, name):
        self.fields['name'] = name

    @email.setter
    def email(self, email):
        self.fields['email'] = email

datasource = DataSource()
fields = [
    Field('name', FieldTypes.STR, FieldKeyTypes.REQUIRED),
    Field('email', FieldTypes.STR, FieldKeyTypes.UNIQUE),
    Field('username', FieldTypes.STR, FieldKeyTypes.UNIQUE)
]

table = JsonTable('users', os.path.join(path_root, 'scripts', 'data'), fields, True)
# table.add_filter_field(FilterField("name", str, ""))
# table.add_filter_field(FilterField("email", str, ""))
datasource.add_table(table)

datasource.clear('users')

dummy_users = [
    User('John Doe', 'test@asd.com'),
    User('Jane Doe', 'test3@asd.com'),
    User('Mary Poppins', 'poppinst@industry.com')
]

for user in dummy_users:
    datasource.insert('users', user)

# for user in datasource.get_by_filter('users', {'name': '', 'email': ''}):
#     print(user)

# fist_user = datasource.get_all('users')[0]
# d_result = datasource.delete('users', fist_user.id)
# print(d_result)
# print("After delete")
print(datasource.get_all('users'))

