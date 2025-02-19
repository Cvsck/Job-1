import json
from unittest.mock import patch

import pandas as pd
import pytest

from src.services import analyze_cashback_categories_on_excel


@pytest.fixture
def test_data():
    data = {
        'Дата операции': ['01.01.2025', '15.01.2025', '20.01.2025'],
        'Категория': ['Еда', 'Транспорт', 'Еда'],
        'Сумма операции': [100, 50, 150]
    }
    df = pd.DataFrame(data)
    return df


@patch('os.path.exists')
@patch('pandas.read_excel')
def test_analyze_cashback(mock_read_excel, mock_path_exists, test_data):
    mock_path_exists.return_value = True
    mock_read_excel.return_value = test_data

    result = analyze_cashback_categories_on_excel("dummy_path.xlsx", 2025, 1)

    expected_result = json.dumps({
        'Еда': 2.50,
        'Транспорт': 0.50
    }, ensure_ascii=False, indent=4)
    assert json.loads(result) == json.loads(expected_result), "Тест 'Корректные данные и результат' провален."


if __name__ == '__main__':
    pytest.main()