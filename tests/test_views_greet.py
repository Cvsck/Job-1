from datetime import datetime
from unittest.mock import patch

from src.utils import greet


def test_greet_morning():
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 2, 19, 8, 0, 0)
        assert greet() == "Доброе утро"


def test_greet_afternoon():
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 2, 19, 14, 0, 0)
        assert greet() == "Добрый день"


def test_greet_evening():
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 2, 19, 19, 0, 0)
        assert greet() == "Добрый вечер"


def test_greet_night():
    with patch("src.utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 2, 19, 2, 0, 0)
        assert greet() == "Доброй ночи"
