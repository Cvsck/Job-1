import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()


def greet() -> str:
    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


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

    print(f"Карты обработаны: {result}")
    return result


def get_top_transactions(transactions: pd.DataFrame) -> list:
    successful_transactions = transactions[transactions["Статус"] == "OK"]
    top_transactions = successful_transactions.sort_values(by="Сумма операции", ascending=False).head(5)

    top_transactions_list = [
        {
            "date": row["Дата операции"],
            "amount": row["Сумма операции"],
            "category": row["Категория"],
            "description": row["Описание"],
        }
        for _, row in top_transactions.iterrows()
    ]

    print(f"Топ транзакций: {top_transactions_list}")
    return top_transactions_list


def get_currency_rates(user_settings_path: str) -> list:
    with open(user_settings_path, "r") as f:
        user_settings = json.load(f)

    # Берем только доллар и евро из JSON файла
    currencies = [currency for currency in user_settings.get("currencies", []) if currency in ["USD", "EUR"]]
    api_key = os.getenv("API_KEY")
    currency_rates = []

    for currency in currencies:
        url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{currency}"
        response = requests.get(url)
        data = response.json()

        # Логирование ответа
        print(f"Ответ от API для {currency}: {data}")

        if "conversion_rates" in data:
            rate = round(data["conversion_rates"].get("RUB", 0.0), 2)
            currency_rates.append({"currency": currency, "rate": rate})

    return currency_rates


def get_stock_prices(user_settings_path: str) -> dict:
    with open(user_settings_path, "r") as f:
        user_settings = json.load(f)

    stocks = user_settings.get("stocks", ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"])
    api_key = os.environ.get("api_stock")

    if not api_key:
        print("Ошибка: API ключ не найден. Убедитесь, что он задан в переменной окружения.")
        return {"stock_prices": []}

    stock_prices = []
    for stock in stocks:
        url = f"https://eodhd.com/api/real-time/{stock}.US?api_token={api_key}&fmt=json"
        response = requests.get(url)

        # Логирование ответа
        print(f"Ответ от API для {stock}: {response.json()}")

        if response.status_code != 200:
            print(f"Ошибка запроса: статус {response.status_code} для {stock}")
            continue

        response_data = response.json()

        if response_data.get("code") != f"{stock}.US":
            print(f"Ошибка: не удалось получить данные для {stock}")
            continue

        stock_info = {
            "stock": stock,
            "price": response_data.get("close"),
        }

        stock_prices.append(stock_info)

    return {"stock_prices": stock_prices}
