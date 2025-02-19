import pandas as pd
import json
import os
from config import excel_file_path

def analyze_cashback_categories_on_excel(file_path: str, year: int, month: int) -> str:
    """
    Функция анализирует транзакции из Excel файла и рассчитывает кешбэк по категориям для указанного года и месяца.
    """
    if not os.path.exists(file_path):
        print("Файл не найден.")
        return json.dumps({"error": "Файл не найден."})

    df_read = pd.read_excel(file_path)

    necessary_columns = ['Дата операции', 'Категория', 'Сумма операции']
    for nec in necessary_columns:
        if nec not in df_read.columns:
            return json.dumps({"error": f"Отсутствует обязательный столбец: {nec}"})

    df_read['Дата операции'] = pd.to_datetime(df_read['Дата операции'], errors='coerce', dayfirst=True)

    if df_read['Дата операции'].isna().any():
        return json.dumps({"error": "Некорректные даты в данных."})

    filter_df = df_read[(df_read['Дата операции'].dt.year == year) & (df_read['Дата операции'].dt.month == month)]
    filter_df = filter_df[filter_df['Сумма операции'].abs() >= 1]

    if filter_df.empty:
        return json.dumps({})

    def calculate_cashback_by_category(filtered_data: pd.DataFrame) -> dict:
        cashback_by_category = {}
        cashback_rate = 0.01

        for _, transaction in filtered_data.iterrows():
            category = transaction['Категория']
            amount = abs(transaction['Сумма операции'])

            cashback = round(amount * cashback_rate, 2)

            if category in cashback_by_category:
                cashback_by_category[category] += cashback
            else:
                cashback_by_category[category] = cashback

        cashback_by_category = {category: round(cashback, 2) for category, cashback in cashback_by_category.items()}

        return cashback_by_category

    cashback_by_category = calculate_cashback_by_category(filter_df)
    sorted_cashback_by_category = dict(sorted(cashback_by_category.items(), key=lambda item: item[1], reverse=True))

    result_json = json.dumps(sorted_cashback_by_category, ensure_ascii=False, indent=4)

    return result_json

result = analyze_cashback_categories_on_excel(excel_file_path, 2021, 3)
print(result)
