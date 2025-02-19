import pandas as pd
import pytest


def get_cards(transactions: pd.DataFrame) -> list:
        card_data = {}
        for _, row in transactions.iterrows():
            card_number = row["Номер карты"]
            if row["Статус"] == "OK" and row["Сумма операции"] > 0:
                card_number = str(card_number).replace(" ", "")
                last_4_digits = card_number[-4:]

                if card_number not in card_data:
                    card_data[card_number] = {"last_4_digits": last_4_digits, "total_spent": 0, "cashback": 0}
                card_data[card_number]["total_spent"] += row["Сумма операции"]
                card_data[card_number]["cashback"] += row["Сумма операции"] // 100

        result = []
        for card_number, card_info in card_data.items():
            result.append(
                {
                    "last_digits": card_info["last_4_digits"],
                    "total_spent": round(card_info["total_spent"], 2),
                    "cashback": round(card_info["cashback"], 2),
                }
            )
        return result


@pytest.mark.parametrize(
    'transactions, expected', [
        (pd.DataFrame([
            {"Номер карты": "7000 7922 8960 6361", "Статус": "OK", "Сумма операции": 1000},
            {"Номер карты": "7158 3007 3472 6758", "Статус": "OK", "Сумма операции": 2000},
            {"Номер карты": "7108 3007 3472 6956", "Статус": "OK", "Сумма операции": 1500},
            {"Номер карты": "7108 3007 0000 0347 26956", "Статус": "Failed", "Сумма операции": 500}
        ]), [
             {"last_digits": "6361", "total_spent": 1000, "cashback": 10},
             {"last_digits": "6758", "total_spent": 2000, "cashback": 20},
             {"last_digits": "6956", "total_spent": 1500, "cashback": 15}
         ])
    ]
)
def test_get_cards(transactions, expected):
    assert get_cards(transactions) == expected