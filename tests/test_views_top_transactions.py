import pandas as pd
import pytest


def get_top_transactions(transactions: pd.DataFrame) -> list:
    successful_transactions = transactions[transactions["Статус"] == "OK"]
    top_transactions = successful_transactions.sort_values(by="Сумма платежа", ascending=False).head(5)

    top_transactions_list = [
        {
            "date": row["Дата операции"],
            "amount": row["Сумма платежа"],
            "category": row["Категория"],
            "description": row["Описание"],
        }
        for _, row in top_transactions.iterrows()
    ]
    return top_transactions_list

@pytest.fixture
def transactions():
    data = {
        "Дата операции": ["2025-02-19", "2025-02-18", "2025-02-17", "2025-02-16", "2025-02-15", "2025-02-14"],
        "Статус": ["OK", "OK", "OK", "Failed", "OK", "OK"],
        "Сумма платежа": [1000, 2000, 3000, 4000, 500, 1500],
        "Категория": ["Еда", "Транспорт", "Медицина", "Развлечения", "Еда", "Одежда"],
        "Описание": ["Обед", "Такси", "Аптека", "Кино", "Завтрак", "Футболка"]
    }
    return pd.DataFrame(data)

def test_get_top_transactions(transactions):
    result = get_top_transactions(transactions)
    expected_result = [
        {"date": "2025-02-17", "amount": 3000, "category": "Медицина", "description": "Аптека"},
        {"date": "2025-02-18", "amount": 2000, "category": "Транспорт", "description": "Такси"},
        {"date": "2025-02-14", "amount": 1500, "category": "Одежда", "description": "Футболка"},
        {"date": "2025-02-19", "amount": 1000, "category": "Еда", "description": "Обед"},
        {"date": "2025-02-15", "amount": 500, "category": "Еда", "description": "Завтрак"}
    ]
    assert result == expected_result