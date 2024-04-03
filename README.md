# Python SOLID Repository pattern implementations

This repository contains a simple implementation of the Repository pattern in Python. The implementation is based on the SOLID principles.

It supports:
- PostgreSQL
- JSON

## Usage

Check the ./scripts/main.py for a full example.

```py

# main.py

# ...

# Define the fields for the table and entities

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

```

