import pandas as pd
from pathlib import Path
from enum import Enum

class TableName(Enum):
    definite_article: 
def load_table(table_name: str):
def check_declension(table_name, table_root_path, determinant, case, answer):
    table = pd.read_csv(Path(table_root_path, table_name))
    table = table.set_index("case")
    correct_form = declension_rules.get(determinant, {}).get(case)
    return correct_form == answer