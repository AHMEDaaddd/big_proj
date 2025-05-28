"""Модуль с функциями для отображения JSON-ответов на главной странице."""
import json
import logging
from datetime import datetime

import pandas as pd

from src.utils.api_client import get_currency_rates, get_stock_prices
from src.utils.xlsx_reader import load_transactions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_greeting(date_time: str) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").hour
    if 5 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def get_cards_summary(df: pd.DataFrame) -> list:
    """Возвращает список карт, трат и кешбэка по каждой из них."""
    result = []
    grouped = df.groupby("Номер карты")
    for card, group in grouped:
        spent = group["Сумма платежа"].sum()
        cashback = spent * 0.01
        result.append({"last_digits": str(card), "total_spent": round(spent, 2), "cashback": round(cashback, 2)})
    return result


def get_top_transactions(df: pd.DataFrame, top_n: int = 5) -> list:
    """Возвращает топ-5 транзакций по сумме платежа."""
    df_sorted = df.sort_values(by="Сумма платежа", ascending=False).head(top_n)
    return [
        {
            "date": row["Дата операции"].strftime("%d.%m.%Y"),
            "amount": round(row["Сумма платежа"], 2),
            "category": row["Категория"],
            "description": row["Описание"],
        }
        for _, row in df_sorted.iterrows()
    ]


def main_view(date_time: str) -> str:
    """Формирует JSON-ответ с данными: приветствие, карты, топ транзакций, валюты и акции."""
    logger.info("Loading transactions...")
    df = load_transactions()
    df = df[pd.to_datetime(df["Дата операции"]) <= pd.to_datetime(date_time)]

    logger.info("Generating greeting...")
    greeting = get_greeting(date_time)

    logger.info("Generating cards summary...")
    cards = get_cards_summary(df)

    logger.info("Getting top transactions...")
    top = get_top_transactions(df)

    logger.info("Fetching currency rates and stock prices...")
    currencies = get_currency_rates()
    stocks = get_stock_prices()

    response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top,
        "currency_rates": currencies,
        "stock_prices": stocks,
    }

    return json.dumps(response, ensure_ascii=False, indent=2)
