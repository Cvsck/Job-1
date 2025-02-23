import logging
from datetime import datetime
from dateutil.relativedelta import relativedelta
from functools import wraps
from typing import Optional

import pandas as pd

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Декоратор для записи отчета в файл
def log_report_to_file(default_filename: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Извлекаем имя файла из аргументов, если передано
            filename = kwargs.pop('filename', default_filename)

            result = func(*args, **kwargs)

            # Если имя файла не передано, используем текущее время для имени файла
            if filename is None:
                filename = f"../data/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            # Записываем результат в файл
            result.to_json(filename, orient="records", force_ascii=False, indent=4)
            logging.info(f"Отчет записан в файл: {filename}")
            return result

        return wrapper

    return decorator

# Функция для получения трат по категории за заданный период
@log_report_to_file("../data/spending_by_category_report.json")  # Можно передать имя файла
def spending_by_category(transaction_data: pd.DataFrame, category: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> pd.DataFrame:
    # Если конечная дата не передана, используем текущую дату
    if end_date is None:
        end_date = datetime.now()
    else:
        # Преобразуем строку в объект datetime, если конечная дата передана
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # Если начальная дата не передана, используем дату 3 месяца назад
    if start_date is None:
        start_date = end_date - relativedelta(months=3)
    else:
        # Преобразуем строку в объект datetime, если начальная дата передана
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    # Убедимся, что столбец 'Дата операции' преобразован в тип datetime
    transaction_data["Дата операции"] = pd.to_datetime(transaction_data["Дата операции"], dayfirst=True, errors="coerce")

    # Фильтруем транзакции по категории и диапазону дат
    filtered_transactions = transaction_data[
        (transaction_data["Категория"] == category) &
        (transaction_data["Дата операции"] >= start_date) &
        (transaction_data["Дата операции"] <= end_date)
    ]

    return filtered_transactions

# Пример использования скрипта
if __name__ == "__main__":
    # Здесь создаем пример DataFrame с транзакциями для тестирования
    data_path = "C:/Users/Макс/my_prj/Job-1/data/operations.xlsx"
    transactions = pd.read_excel(data_path)  # Используем pd.read_excel для чтения данных

    # Получаем отчет по категории "Еда" за 2021 год
    report = spending_by_category(transactions, category="Супермаркеты", start_date="2021-01-01", end_date="2021-12-31")
    print(report)
