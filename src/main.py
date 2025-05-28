"""Точка входа в приложение. Отображает главную страницу на основе переданной даты."""
import logging
import sys

from src.views import main_view

logging.basicConfig(level=logging.INFO)


def run() -> None:
    """Запускает отображение JSON-ответа главной страницы по переданной дате."""
    if len(sys.argv) < 2:
        print("❗ Пожалуйста, укажите дату и время в формате YYYY-MM-DD HH:MM:SS")
        return

    date_time = sys.argv[1]
    try:
        result = main_view(date_time)
        print(result)
    except Exception as e:
        logging.error(f"Ошибка: {e}")


if __name__ == "__main__":
    run()
