import os
import sys
from pathlib import Path


path_root = Path(__file__).parents[1]
sys.path.append(os.path.join(path_root, 'src'))

from repositories import DataSource, JsonTable

datasource = DataSource()

table = JsonTable('users', os.path.join(path_root, 'scripts', 'data'))

datasource.add_table(table)
