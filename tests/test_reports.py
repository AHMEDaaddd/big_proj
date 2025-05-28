import json
import logging
from datetime import datetime
from typing import Callable, Optional

import pandas as pd

logger = logging.getLogger(__name__)


def save_report(filename: Optional[str] = None) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            output_file = filename or f"{func.__name__}_output.json"
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    if isinstance(result, pd.DataFrame):
                        result.to_json(f, force_ascii=False, orient="records", indent=2)
                    else:
                        json.dump(result, f, ensure_ascii=False, indent=2)
                logger.info(f"Отчет сохранен в файл {output_file}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета: {e}")
            return result

        return wrapper

    return decorator


@save_report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    date = pd.to_datetime(date or datetime.now())
    period = date - pd.DateOffset(months=3)
    df = transactions.copy()
    df["Дата операция"] = pd.to_datetime(df["Дата операция"], dayfirst=True)
    mask = (df["Дата операция"] >= period) & (df["Дата операция"] <= date) & (df["Категория"] == category)
    return df.loc[mask]


@save_report()
def spending_by_weekday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    date = pd.to_datetime(date or datetime.now())
    period = date - pd.DateOffset(months=3)
    df = transactions.copy()
    df["Дата операция"] = pd.to_datetime(df["Дата операция"], dayfirst=True)
    df = df[(df["Дата операция"] >= period) & (df["Дата операция"] <= date)]
    df["День недели"] = df["Дата операция"].dt.day_name()
    return df.groupby("День недели")["Сумма платежа"].mean().reset_index(name="Средняя сумма")


@save_report()
def spending_by_workday(transactions: pd.DataFrame, date: Optional[str] = None) -> pd.DataFrame:
    date = pd.to_datetime(date or datetime.now())
    period = date - pd.DateOffset(months=3)
    df = transactions.copy()
    df["Дата операция"] = pd.to_datetime(df["Дата операция"], dayfirst=True)
    df = df[(df["Дата операция"] >= period) & (df["Дата операция"] <= date)]
    df["Тип дня"] = df["Дата операция"].dt.dayofweek.apply(lambda x: "Рабочий" if x < 5 else "Выходной")
    return df.groupby("Тип дня")["Сумма платежа"].mean().reset_index(name="Средняя сумма")
