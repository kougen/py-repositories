import os
import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(os.path.join(path_root, 'src'))

from pyrepositories import DataSource, JsonTable, Entity, IdTypes


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

datasource = DataSource(id_type=IdTypes.UUID)

table = JsonTable('users', os.path.join(path_root, 'scripts', 'data'))
datasource.add_table(table)
datasource.clear('users')
user = User('John Doe', 'test@asd.com')
user2 = User('Jane Doe 2', 'test3@asd.com')

result = datasource.insert('users', user)
print(result)
result = datasource.insert('users', user2)
print(result)

for user in datasource.get_all('users') or []:
    print(user)
