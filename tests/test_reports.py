import os
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pandas as pd
import pytest

from src.reports import spending_by_category


# Создаем тестовые данные для транзакций
@pytest.fixture
def transaction_data():
    data = {
        "Дата операции": ["2022-01-10", "2022-02-15", "2022-03-20", "2022-01-25", "2022-04-05"],
        "Категория": ["Супермаркеты", "Супермаркеты", "Супермаркеты", "Рестораны", "Супермаркеты"],
        "Сумма": [100, 150, 200, 250, 300],
    }
    # Преобразуем столбец 'Дата операции' в datetime с явным указанием формата
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%Y-%m-%d", errors="coerce")
    return df


def test_spending_by_category(transaction_data):
    # Удаляем файл отчета, если он существует
    if os.path.exists("../data/spending_by_category_report.json"):
        os.remove("../data/spending_by_category_report.json")

    # Выполняем тестируемую функцию
    result = spending_by_category(
        transaction_data, category="Супермаркеты", start_date="2022-01-01", end_date="2022-03-31"
    )

    # Проверяем, что результат содержит правильное количество записей
    assert len(result) == 3

    # Проверяем, что файл отчета был создан
    assert os.path.exists("../data/spending_by_category_report.json")

    # Проверяем, что содержимое файла соответствует ожиданиям
    report_data = pd.read_json("../data/spending_by_category_report.json", orient="records")
    assert len(report_data) == 3
    assert report_data["Категория"].tolist() == ["Супермаркеты", "Супермаркеты", "Супермаркеты"]
    assert report_data["Сумма"].tolist() == [100, 150, 200]


if __name__ == "__main__":
    pytest.main()
