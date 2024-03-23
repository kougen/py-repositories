import os
import sys
from pathlib import Path


path_root = Path(__file__).parents[1]
sys.path.append(os.path.join(path_root, 'src'))

from repositories import DataSource, JsonTable, Entity


class User(Entity):
    def __init__(self, id, name, email):
        super().__init__(id)
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

table = JsonTable('users', os.path.join(path_root, 'scripts', 'data'))
datasource.add_table(table)

user = User(1, 'John Doe', 'test@asd.com')
user2 = User(2, 'Jane Doe 2', 'test3@asd.com')

result = datasource.insert('users', user)
print(result)
result = datasource.insert('users', user2)
print(result)

for user in datasource.get_all('users') or []:
    print(user)
