import logging
from datetime import datetime

from config import excel_file_path
from src.views import get_main_page

# Настройка логирования
logging.basicConfig(
    filename="../logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


def main():
    # Путь к файлу с транзакциями
    transactions_file_path = excel_file_path

    # Параметры для анализа (год и месяц)
    current_year = datetime.now().year
    current_month = datetime.now().month

    logging.info(f"Запуск программы {current_month}/{current_year}.")

    logging.info("Получаем данные для главной страницы")
    main_page = get_main_page(date=datetime.now().strftime("%Y-%m-%d"), transactions_path=transactions_file_path)
    logging.info(main_page)  # Логируем результат

    print(main_page)  # Выводим результат на экран


if __name__ == "__main__":
    main()
