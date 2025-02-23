# -*- coding: utf-8 -*-
import os
from unittest.mock import Mock

import requests


def get_stock_prices(stock_list: list) -> dict:
    api_key = os.environ.get("api_stock")

    if not api_key:
        print("Ошибка: API ключ не найден. Убедитесь, что он задан в переменной окружении.")
        return {"stock_prices": []}

    stock_prices = []
    for stock in stock_list:
        url = f"https://eodhd.com/api/real-time/{stock}.US?api_token={api_key}&fmt=json"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Ошибка запроса: статус {response.status_code} для {stock}")
            continue

        response_data = response.json()

        if response_data.get("code") != f"{stock}.US":
            print(f"Ошибка: не удалось получить данные для {stock}")
            continue

        stock_info = {
            "stock": stock,
            "price": response_data.get("close"),  # Используем поле "close" для получения текущей цены
        }

        stock_prices.append(stock_info)

    return {"stock_prices": stock_prices}


def test_successful_response():
    os.environ["api_stock"] = "fake_api_key"
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"code": "AAPL.US", "close": 150.0}
    requests.get = Mock(return_value=mock_response)

    result = get_stock_prices(["AAPL"])
    assert result == {"stock_prices": [{"stock": "AAPL", "price": 150.0}]}


# Запускаем тест
test_successful_response()
