"""Модуль с сервисными функциями: кешбэк, инвесткопилка, поиск."""
import json
import logging
import re
from datetime import datetime
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


def cashback_categories(data: List[Dict[str, Any]], year: int, month: int) -> str:
    """Вычисляет сумму кешбэка по категориям за указанный месяц."""
    result: dict[str, float] = {}
    for tx in data:
        date = datetime.strptime(str(tx["Дата операции"]), "%Y-%m-%d")
        if date.year == year and date.month == month:
            category = tx["Категория"]
            amount = tx.get("Сумма платежа", 0)
            cashback = amount * 0.01
            result[category] = result.get(category, 0) + cashback
    return json.dumps(result, ensure_ascii=False, indent=2)


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """Рассчитывает сумму округления по операциям в инвесткопилку."""
    total = 0.0
    for tx in transactions:
        date = tx["Дата операции"]
        if date.startswith(month):
            amount = float(tx.get("Сумма операции", 0))
            rounded = ((amount // limit) + 1) * limit
            total += rounded - amount
    return round(total, 2)


def simple_search(transactions: List[Dict[str, Any]], query: str) -> str:
    """Возвращает транзакции, содержащие запрос в описании или категории."""
    query_lower = query.lower()
    result = [
        tx
        for tx in transactions
        if query_lower in str(tx.get("Описание", "")).lower() or query_lower in str(tx.get("Категория", "")).lower()
    ]
    return json.dumps(result, ensure_ascii=False, indent=2)


def search_phone_numbers(transactions: List[Dict[str, Any]]) -> str:
    """Возвращает транзакции, содержащие телефонные номера."""
    pattern = r"\+7\s?\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{2}[-\s]?\d{2}"
    result = [tx for tx in transactions if re.search(pattern, str(tx.get("Описание", "")))]
    return json.dumps(result, ensure_ascii=False, indent=2)


def search_private_transfers(transactions: List[Dict[str, Any]]) -> str:
    """Возвращает переводы физическим лицам с именем и инициалом."""
    pattern = r"\b[А-ЯЁ][а-яё]+\s[А-ЯЁ]\."
    result = [
        tx
        for tx in transactions
        if tx.get("Категория") == "Переводы" and re.search(pattern, str(tx.get("Описание", "")))
    ]
    return json.dumps(result, ensure_ascii=False, indent=2)
