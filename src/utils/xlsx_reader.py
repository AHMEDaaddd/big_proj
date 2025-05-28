"""Модуль для чтения Excel-файла с транзакциями."""
from pathlib import Path

import pandas as pd




def load_transactions(file_path: str = "data/operations.xlsx") -> pd.DataFrame:
    """Загружает Excel-файл в DataFrame и обрабатывает названия столбцов."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Файл {file_path} не найден.")

    df = pd.read_excel(path)
    df.columns = df.columns.str.strip()
    return df
