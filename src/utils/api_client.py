"""Модуль для получения данных с внешних API (валюты, акции)."""
import logging
import os
from typing import Dict, List

import requests
from dotenv import load_dotenv

from src.user_settings import get_user_settings

load_dotenv()
logger = logging.getLogger(__name__)


def get_currency_rates() -> List[Dict[str, float]]:
    """Получает текущие курсы валют пользователя через API."""
    settings = get_user_settings()
    currencies = settings.get("user_currencies", ["USD", "EUR"])
    url = "https://api.apilayer.com/exchangerates_data/latest"
    headers = {"apikey": os.getenv("EXCHANGE_API_KEY")}
    params = {"base": "RUB", "symbols": ",".join(currencies)}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()["rates"]
        return [{"currency": c, "rate": round(1 / data[c], 2)} for c in currencies]
    except Exception as e:
        logger.error(f"Ошибка при получении валют: {e}")
        return [{"currency": c, "rate": 0.0} for c in currencies]


def get_stock_prices() -> List[Dict[str, float]]:
    """Получает цены акций пользователя через API."""
    settings = get_user_settings()
    stocks = settings.get("user_stocks", [])
    api_key = os.getenv("STOCK_API_KEY")
    results = []

    for stock in stocks:
        url = f"https://www.alphavantage.co/query"
        params = {"function": "GLOBAL_QUOTE", "symbol": stock, "apikey": api_key}
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            quote = response.json().get("Global Quote", {})
            price = round(float(quote.get("05. price", 0.0)), 2)
            results.append({"stock": stock, "price": price})
        except Exception as e:
            logger.error(f"Ошибка при получении цены акции {stock}: {e}")
            results.append({"stock": stock, "price": 0.0})

    return results
