import pandas as pd
import pytest

from src.utils import get_cards


@pytest.mark.parametrize(
    "transactions, expected",
    [
        (
            pd.DataFrame(
                [
                    {"Номер карты": "7000 7922 8960 6361", "Статус": "OK", "Сумма операции": -1000},
                    {"Номер карты": "7158 3007 3472 6758", "Статус": "OK", "Сумма операции": -2000},
                    {"Номер карты": "7108 3007 3472 6956", "Статус": "OK", "Сумма операции": -1500},
                    {"Номер карты": "7108 3007 0000 0347 26956", "Статус": "Failed", "Сумма операции": -500},
                ]
            ),
            [
                {"last_digits": "6361", "total_spent": -1000, "cashback": -10},
                {"last_digits": "6758", "total_spent": -2000, "cashback": -20},
                {"last_digits": "6956", "total_spent": -1500, "cashback": -15},
            ],
        )
    ],
)
def test_get_cards(transactions, expected):
    assert get_cards(transactions) == expected
