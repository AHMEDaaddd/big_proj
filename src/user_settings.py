"""Модуль для загрузки пользовательских настроек из JSON."""
import json
from typing import Any, Dict


def get_user_settings(path: str = "bank_project/user_settings.json") -> Dict[str, Any]:
    """Загружает пользовательские настройки из JSON-файла."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
        return dict(data)
