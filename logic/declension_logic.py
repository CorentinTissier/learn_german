import pandas as pd
from pathlib import Path
from enum import Enum


# Base directory for CSV files 
TABLE_DIR = Path("data", "csv", "tables")


class Gender(Enum):
    MASCULINE = 'Masculine'
    FEMININE = 'Feminine'
    NEUTER = 'Neuter'


class Case(Enum):
    NOMINATIVE = 'Nominative'
    ACCUSATIVE = 'Accusative'
    DATIVE = 'Dative'
    GENITIVE = 'Genitive'


class TableName(Enum):
    DEFINITE_ARTICLE = 'definite article'
    INDEFINITE_ARTICLE = 'indefinite article'

def convert_name_to_file(table_name: TableName) -> str: 
    table_file = table_name.value.lower().replace(" ", "_") + ".csv"
    return table_file


def load_table(table_name: TableName):
    table_file = convert_name_to_file(table_name)
    table_path = TABLE_DIR / table_file
    
    # Load the table
    try:
        table = pd.read_csv(table_path)

    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {table_path} was not found.")
    
    except Exception as e:
        raise RuntimeError(f"An error occurred while loading the table: {e}")
    
    table = table.set_index("Case")
    
    return table


def check_declension(
        table: pd.DataFrame, 
        gender: Gender, 
        case: Case, 
        answer: str) -> bool:
    correct_form = table.loc[case.value, gender.value]
    return correct_form == answer
