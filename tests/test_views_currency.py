import json
from unittest.mock import patch, mock_open
import pytest
from src.utils import get_currency_rates

@patch("requests.get")
@patch("builtins.open", new_callable=mock_open, read_data='{"user_currencies": ["USD", "EUR"]}')
def test_currency_conversion(mock_open, mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "conversion_rates": {"RUB": 91.48}
    }

    expected_result = [
        {"currency": "USD", "rate": 91.48},
        {"currency": "EUR", "rate": 91.48}
    ]

    # Передаем любой путь, так как содержимое файла мокается
    assert get_currency_rates("dummy_path") == expected_result

# Вызов функции тестирования
test_currency_conversion()
