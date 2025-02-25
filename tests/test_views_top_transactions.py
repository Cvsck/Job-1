import pandas as pd
import pytest
from src.utils import get_top_transactions  # импортируем функцию из вашего модуля


@pytest.fixture
def transactions():
    data = {
        "Дата операции": ["2025-02-19", "2025-02-18", "2025-02-17", "2025-02-16", "2025-02-15", "2025-02-14"],
        "Статус": ["OK", "OK", "OK", "Failed", "OK", "OK"],
        "Сумма операции": [1000, 2000, 3000, 4000, 500, 1500],
        "Категория": ["Еда", "Транспорт", "Медицина", "Развлечения", "Еда", "Одежда"],
        "Описание": ["Обед", "Такси", "Аптека", "Кино", "Завтрак", "Футболка"],
    }
    return pd.DataFrame(data)


def test_get_top_transactions(transactions):
    result = get_top_transactions(transactions)

    assert len(result) == 5  # Проверяем, что в результате 5 транзакций
