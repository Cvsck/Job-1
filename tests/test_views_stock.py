import json
from unittest.mock import patch, mock_open

import requests

from src.utils import get_stock_prices  # Замените your_module на актуальный путь к вашему модулю

@patch("requests.get")
@patch("builtins.open", new_callable=mock_open, read_data='{"user_stocks": ["AAPL", "AMZN"]}')
def test_get_stock_prices(mock_open, mock_get):
    def mock_get_side_effect(url):
        if "AAPL" in url:
            return MockResponse({"code": "AAPL.US", "close": 150.0}, 200)
        elif "AMZN" in url:
            return MockResponse({"code": "AMZN.US", "close": 3300.0}, 200)

    mock_get.side_effect = mock_get_side_effect

    expected_result = {
        "stock_prices": [
            {"stock": "AAPL", "price": 150.0},
            {"stock": "AMZN", "price": 3300.0}
        ]
    }

    # Передаем любой путь, так как содержимое файла мокируется
    assert get_stock_prices("dummy_path") == expected_result

# Вспомогательная функция для мока ответов
def MockResponse(json_data, status_code=200):
    response = requests.Response()
    response.status_code = 200
    response._content = json.dumps(json_data).encode()
    return response

# Вызов функции тестирования
test_get_stock_prices()
