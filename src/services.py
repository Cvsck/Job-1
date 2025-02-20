import json
import os
from datetime import datetime
from typing import Any, Dict, List

from openpyxl import load_workbook


def parse_date(date_str: str) -> datetime:
    """Преобразование строки даты в объект datetime."""
    if date_str is None:
        return None
    try:
        return datetime.strptime(date_str, "%d.%m.%Y")
    except (ValueError, TypeError):
        try:
            return datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
        except (ValueError, TypeError):
            return None


def filter_transactions_by_date(transactions: List[Dict[str, Any]], year: int, month: int) -> List[Dict[str, Any]]:
    """Фильтрация транзакций по году и месяцу."""
    return [
        record
        for record in transactions
        if record["Дата операции"]
        and isinstance(record["Дата операции"], datetime)
        and record["Дата операции"].year == year
        and record["Дата операции"].month == month
        and abs(record["Сумма операции"]) >= 1
    ]


def calculate_cashback_by_category(filtered_transactions: List[Dict[str, Any]]) -> Dict[str, float]:
    """Расчет кешбэка по категориям."""
    cashback_by_category = {}
    cashback_rate = 0.01

    for transaction in filtered_transactions:
        category = transaction["Категория"]
        amount = abs(transaction["Сумма операции"])

        cashback = amount * cashback_rate

        if category in cashback_by_category:
            cashback_by_category[category] += cashback
        else:
            cashback_by_category[category] = cashback

    return {category: round(cashback, 2) for category, cashback in cashback_by_category.items()}


def analyze_cashback_categories(transactions_data: List[Dict[str, Any]], filter_year: int, filter_month: int) -> str:
    """Основная функция анализа кешбэка по категориям."""
    for record in transactions_data:
        record["Дата операции"] = parse_date(record.get("Дата операции") or record.get("Дата платежа"))

    filtered_transactions = filter_transactions_by_date(transactions_data, filter_year, filter_month)

    if not filtered_transactions:
        return json.dumps({})

    cashback_by_category = calculate_cashback_by_category(filtered_transactions)

    result_json = json.dumps(cashback_by_category, ensure_ascii=False, indent=4)

    return result_json


def load_data_from_excel(excel_file_path: str) -> List[Dict[str, Any]]:
    """Загрузка данных из Excel файла."""
    if not os.path.exists(excel_file_path):
        raise FileNotFoundError(f"Файл не найден: {excel_file_path}")

    workbook = load_workbook(excel_file_path)
    sheet = workbook.active

    header = [cell.value for cell in sheet[1]]
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data.append(dict(zip(header, row)))

    return data


def save_result_to_file(result: str, output_file_path: str) -> None:
    """Сохранение результата в файл JSON."""
    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write(result)


if __name__ == "__main__":
    try:
        excel_path = "C:\\Users\\Макс\\my_prj\\Job-1\\data\\operations.xlsx"
        output_file_path = "C:\\Users\\Макс\\my_prj\\Job-1\\data\\result.json"
        print(f"Загрузка данных из файла: {excel_path}")
        transaction_records = load_data_from_excel(excel_path)
        print(f"Данные загружены: {transaction_records}")
        year_2021 = 2021
        month_march = 3
        result = analyze_cashback_categories(transaction_records, year_2021, month_march)
        print(f"Результат анализа: {result}")
        save_result_to_file(result, output_file_path)
        print(f"Результат сохранен в файл: {output_file_path}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
