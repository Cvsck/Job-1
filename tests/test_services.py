import os
import sys

from src.services import analyze_cashback_categories

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
transaction_data = [{"Дата операции": "15.12.2021", "Категория": "Переводы", "Сумма операции": 181186}]


def test_get_cashback_categories_dict():
    result = analyze_cashback_categories(transaction_data, 2021, 12)
    assert result == {"Переводы": 1811.86}


if __name__ == "__main__":
    test_get_cashback_categories_dict()
    print("Test passed")
