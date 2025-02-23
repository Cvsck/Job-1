import json
from datetime import datetime
from typing import Any, Dict, List, Optional
from openpyxl import load_workbook

def parse_date(date_str: Optional[str]) -> Optional[datetime]:
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

    # Сортировка категорий по убыванию кешбэка
    sorted_cashback_by_category = dict(sorted(cashback_by_category.items(), key=lambda item: item[1], reverse=True))

    return {category: round(cashback, 2) for category, cashback in sorted_cashback_by_category.items()}

def analyze_cashback_categories(transactions_data: List[Dict[str, Any]], filter_year: int, filter_month: int) -> Dict[str, float]:
    """Основная функция анализа кешбэка по категориям."""
    for record in transactions_data:
        record["Дата операции"] = parse_date(record.get("Дата операции") or record.get("Дата платежа"))

    filtered_transactions = filter_transactions_by_date(transactions_data, filter_year, filter_month)

    if not filtered_transactions:
        return {}

    cashback_by_category = calculate_cashback_by_category(filtered_transactions)
    return cashback_by_category

def load_data_from_excel(excel_file_path: str) -> List[Dict[str, Any]]:
    """Загрузка данных из Excel файла."""
    workbook = load_workbook(excel_file_path)
    sheet = workbook.active

    header = [cell.value for cell in sheet[1]]
    data = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        data.append(dict(zip(header, row)))

    return data

def save_result_to_file(result: Dict[str, float], output_path: str) -> None:
    """Сохранение результата в файл JSON."""
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # Здесь вы можете указать путь к вашему Excel файлу и указать выходной путь для JSON файла
    excel_file_path = "C:/Users/Макс/my_prj/Job-1/data/operations.xlsx"
    output_file_path = "../data/cashback_results.json"
    year = 2021
    month = 2

    transactions = load_data_from_excel(excel_file_path)
    cashback_results = analyze_cashback_categories(transactions, year, month)
    save_result_to_file(cashback_results, output_file_path)
