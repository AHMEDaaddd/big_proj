from src.views import get_greeting


def test_get_greeting():
    assert get_greeting("2025-05-28 08:00:00") == "Доброе утро"
    assert get_greeting("2025-05-28 14:00:00") == "Добрый день"
    assert get_greeting("2025-05-28 20:00:00") == "Добрый вечер"
    assert get_greeting("2025-05-28 02:00:00") == "Доброй ночи"
