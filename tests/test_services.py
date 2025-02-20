import sys
import os
from datetime import datetime

# Добавляем путь к системному пути
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from src.services import filter_transactions_by_date, calculate_cashback_by_category

def test_filter_transactions_by_date():
    transactions = [
        {'Дата операции': datetime(2021, 3, 1), 'Категория': 'Продукты', 'Сумма операции': 1000.00},
        {'Дата операции': datetime(2021, 3, 5), 'Категория': 'Развлечения', 'Сумма операции': 2000.00},
        {'Дата операции': datetime(2021, 4, 10), 'Категория': 'Продукты', 'Сумма операции': 500.00}
    ]
    filtered_transactions = filter_transactions_by_date(transactions, 2021, 3)
    assert len(filtered_transactions) == 2
    assert filtered_transactions[0]['Категория'] == 'Продукты'
    assert filtered_transactions[1]['Категория'] == 'Развлечения'

def test_calculate_cashback_by_category():
    filtered_transactions = [
        {'Дата операции': datetime(2021, 3, 1), 'Категория': 'Продукты', 'Сумма операции': 1000.00},
        {'Дата операции': datetime(2021, 3, 5), 'Категория': 'Развлечения', 'Сумма операции': 2000.00}
    ]
    cashback = calculate_cashback_by_category(filtered_transactions)

    assert isinstance(cashback, dict)
    assert 'Продукты' in cashback
    assert 'Развлечения' in cashback
    assert cashback['Продукты'] == 10.00  # Измените значение в зависимости от ваших правил начисления кэшбэка
    assert cashback['Развлечения'] == 20.00  # Измените значение в зависимости от ваших правил начисления кэшбэка
