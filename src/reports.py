import logging
from datetime import datetime
from functools import wraps
from typing import Optional

import pandas as pd
from dateutil.relativedelta import relativedelta

# Настройка логирования
logging.basicConfig(level=logging.INFO)


# Декоратор для записи отчета в файл
def log_report_to_file(default_filename: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logging.info(f"Вызов функции {func.__name__} с аргументами: {args}, {kwargs}")
            filename = kwargs.pop("filename", default_filename)

            result = func(*args, **kwargs)

            if filename is None:
                filename = f"../data/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

            result.to_json(filename, orient="records", force_ascii=False, indent=4)
            logging.info(f"Отчет записан в файл: {filename}")
            return result

        return wrapper

    return decorator


@log_report_to_file("../data/spending_by_category_report.json")
def spending_by_category(
    transaction_data: pd.DataFrame, category: str, start_date: Optional[str] = None, end_date: Optional[str] = None
) -> pd.DataFrame:
    """
    Функция для получения трат по категории за заданный период
    """
    logging.info(f"Фильтрация транзакций по категории: {category}")

    if end_date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    if start_date is None:
        start_date = end_date - relativedelta(months=3)
    else:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

    logging.info(f"Период фильтрации: с {start_date} по {end_date}")

    # Преобразуем столбец 'Дата операции' в datetime и игнорируем некорректные значения
    transaction_data["Дата операции"] = pd.to_datetime(
        transaction_data["Дата операции"], dayfirst=True, errors="coerce"
    )

    # Отфильтровываем некорректные значения в столбце 'Дата операции'
    transaction_data = transaction_data.dropna(subset=["Дата операции"])

    filtered_transactions = transaction_data[
        (transaction_data["Категория"] == category)
        & (transaction_data["Дата операции"] >= start_date)
        & (transaction_data["Дата операции"] <= end_date)
    ]

    logging.info(f"Количество найденных транзакций: {len(filtered_transactions)}")

    return filtered_transactions
