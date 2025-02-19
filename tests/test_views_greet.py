from datetime import datetime

import pandas as pd
import pytest


def greet(current_time=None):
    if current_time is None:
        current_time = datetime.now()
    current_hour = current_time.hour
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def test_greet_morning():
    assert greet(datetime(2025, 2, 19, 8, 0, 0)) == "Доброе утро"

def test_greet_afternoon():
    assert greet(datetime(2025, 2, 19, 14, 0, 0)) == "Добрый день"

def test_greet_evening():
    assert greet(datetime(2025, 2, 19, 19, 0, 0)) == "Добрый вечер"

def test_greet_night():
    assert greet(datetime(2025, 2, 19, 2, 0, 0)) == "Доброй ночи"
