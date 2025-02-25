import json
import logging
from datetime import datetime

import pandas as pd

from config import excel_file_path, user_settings
from src.reports import spending_by_category
from src.services import analyze_cashback_categories, load_data_from_excel, save_result_to_file
from src.utils import get_cards, get_currency_rates, get_stock_prices, get_top_transactions, greet

# Настроить логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def filter_transactions_by_date(transactions, start_date, end_date):
    """
    Фильтрация операций по диапазону дат
    """
    return transactions[(transactions["date"] >= start_date) & (transactions["date"] <= end_date)]


def main(date_time_str: str):
    """
    Вызов основной функции
    """
    try:
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S")
        logging.info(f"Начало выполнения программы с датой и временем: {date_time}")
    except ValueError as e:
        logging.error(f"Неправильный формат даты и времени: {e}")
        return

    logging.info("Начало выполнения программы")

    # Загрузить данные из Excel файла
    transactions_data_path = excel_file_path
    logging.info("Загрузка данных из файла: %s", transactions_data_path)
    transactions = pd.read_excel(transactions_data_path)

    # Преобразовать столбец с датами в формат datetime
    transactions["date"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Фильтровать операции по дате
    start_date = date_time.replace(day=1).strftime("%Y-%m-%d %H:%M:%S")
    filtered_transactions = filter_transactions_by_date(transactions, start_date, date_time_str)

    # Загрузить данные из JSON файла
    user_settings_path = user_settings
    logging.info("Загрузка данных из файла: %s", user_settings_path)

    # Собрать результаты
    result = {
        "greeting": greet(),  # Получить приветствие
        "cards": get_cards(filtered_transactions),  # Получить карты
        "top_transactions": get_top_transactions(filtered_transactions),  # Получить топ транзакций
        "currency_rates": get_currency_rates(user_settings_path),  # Получить валютные курсы
        "stock_prices": get_stock_prices(user_settings_path),  # Получить цены акций
    }

    logging.info("Результаты: %s", json.dumps(result, indent=4, ensure_ascii=False))

    # Сохранить результаты в JSON файл
    with open("../data/result.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print("Результаты сохранены в файл result.json")

    logging.info("Конец выполнения программы")

    # Вызов функции spending_by_category
    logging.info("Начало выполнения скрипта для анализа трат")
    data_path = excel_file_path
    logging.info(f"Загрузка данных из файла: {data_path}")
    transactions = pd.read_excel(data_path)

    report = spending_by_category(
        transactions, category="Супермаркеты", start_date="2021-01-01", end_date="2021-12-31"
    )
    logging.info("Генерация отчета завершена")
    print(report)

    # Вызов функций из модуля service
    logging.info("Начало выполнения скрипта для анализа кешбэка")
    transactions = load_data_from_excel(data_path)
    year_input = 2020
    month_input = 2
    cashback_results = analyze_cashback_categories(transactions, year_input, month_input)

    json_output_path = "../data/cashback_results.json"
    save_result_to_file(cashback_results, json_output_path)

    logging.info("Генерация отчета завершена")
    print(cashback_results)

    logging.info("Конец выполнения скрипта")


if __name__ == "__main__":
    main("2021-12-26 22:09:56")  # Пример вызова основной функции с датой и временем
