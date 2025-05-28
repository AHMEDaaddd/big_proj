"""Модуль с функциями отчетов по тратам."""
import json
import logging
from datetime import datetime
from typing import Any, Callable, Optional

import pandas as pd
from pandas import DataFrame

logger = logging.getLogger(__name__)


def save_report(filename: Optional[str] = None) -> Callable:
    """Декоратор для сохранения результата функции-отчета в JSON-файл."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
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
def spending_by_category(transactions: DataFrame, category: str, date: Optional[str] = None) -> DataFrame:
    """Возвращает траты по категории за последние 3 месяца от указанной даты."""
    ts = pd.to_datetime(datetime.now()) if date is None else pd.to_datetime(date)
    period = ts - pd.DateOffset(months=3)
    df = transactions.copy()
    df["Дата операция"] = pd.to_datetime(df["Дата операция"], dayfirst=True)
    mask = (df["Дата операция"] >= period) & (df["Дата операция"] <= ts) & (df["Категория"] == category)
    return df.loc[mask]


@save_report()
def spending_by_weekday(transactions: DataFrame, date: Optional[str] = None) -> DataFrame:
    """Возвращает средние траты по дням недели за 3 месяца от указанной даты."""
    ts = pd.to_datetime(datetime.now()) if date is None else pd.to_datetime(date)
    period = ts - pd.DateOffset(months=3)
    df = transactions.copy()
    df["Дата операция"] = pd.to_datetime(df["Дата операция"], dayfirst=True)
    df = df[(df["Дата операция"] >= period) & (df["Дата операция"] <= ts)]
    df["День недели"] = df["Дата операция"].dt.day_name()
    return df.groupby("День недели")["Сумма платежа"].mean().reset_index(name="Средняя сумма")


@save_report()
def spending_by_workday(transactions: DataFrame, date: Optional[str] = None) -> DataFrame:
    """Возвращает средние траты в рабочие и выходные дни за 3 месяца от даты."""
    ts = pd.to_datetime(datetime.now()) if date is None else pd.to_datetime(date)
    period = ts - pd.DateOffset(months=3)
    df = transactions.copy()
    df["Дата операция"] = pd.to_datetime(df["Дата операция"], dayfirst=True)
    df = df[(df["Дата операция"] >= period) & (df["Дата операция"] <= ts)]
    df["Тип дня"] = df["Дата операция"].dt.dayofweek.apply(lambda x: "Рабочий" if x < 5 else "Выходной")
    return df.groupby("Тип дня")["Сумма платежа"].mean().reset_index(name="Средняя сумма")
