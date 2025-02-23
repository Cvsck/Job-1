import os
from unittest.mock import patch

import requests


def get_currency_rates() -> list:
    api_key = os.getenv("API_KEY")  # используем переменную окружения для API ключа
    currencies = ["USD", "EUR"]
    currency_rates = []

    for currency in currencies:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"
        response = requests.get(url)
        data = response.json()

        # Выводим данные для проверки
        print(f"Data for {currency}: {data}")

        if "conversion_rates" in data:
            rate = round(data["conversion_rates"].get("RUB", 0.0), 2)
            currency_rates.append({"currency": currency, "rate": rate})

    return currency_rates


@patch("requests.get")
def test_currency_conversion(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"conversion_rates": {"RUB": 91.48}}

    expected_result = [{"currency": "USD", "rate": 91.48}, {"currency": "EUR", "rate": 91.48}]

    assert get_currency_rates() == expected_result


# Вызов функции тестирования
test_currency_conversion()
