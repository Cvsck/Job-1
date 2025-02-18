import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv


from config import excel_file_path

# Загрузка переменных окружения из файла .env
load_dotenv()


def get_main_page(date: str, transactions_path: str) -> str:
    """
    Главная функция, которая принимает на вход дату и путь к файлу с транзакциями,
    возвращает JSON-ответ и топ-5 транзакций.
    """

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

    greeting = greet()

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

    def get_top_transactions(transactions: pd.DataFrame) -> list:
        successful_transactions = transactions[transactions["Статус"] == "OK"]
        top_transactions = successful_transactions.sort_values(by="Сумма платежа", ascending=False).head(5)

        top_transactions_list = [
            {
                "date": row["Дата операции"],
                "amount": row["Сумма платежа"],
                "category": row["Категория"],
                "description": row["Описание"],
            }
            for _, row in top_transactions.iterrows()
        ]
        return top_transactions_list

    def get_currency_rates() -> list:
        apikey = os.getenv("API_KEY")

        if not apikey:
            print("Ошибка: API ключ не найден. Убедитесь, что он задан в переменной окружения.")
            return []

        url = f"https://v6.exchangerate-api.com/v6/{apikey}/latest/USD"
        headers = {"apikey": f"{apikey}"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Ошибка запроса: статус {response.status_code}")
            return []

        response_data = response.json()

        if response_data["result"] != "success":
            print("Ошибка: не удалось получить курсы валют")
            return []

        currencies = ["USD", "EUR"]
        currency_rates = []
        for currency in currencies:
            if currency in response_data["conversion_rates"]:
                currency_rates.append({"currency": currency, "rate": response_data["conversion_rates"][currency]})
        return currency_rates

    def get_stock_prices(stocks: list) -> dict:
        api_key = os.environ.get("api_stock")

        if not api_key:
            print("Ошибка: API ключ не найден. Убедитесь, что он задан в переменной окружения.")
            return {"stock_prices": []}

        stock_prices = []
        for stock in stocks:
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

    stocks = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]

    df_transactions = pd.read_excel(excel_file_path)

    cards = get_cards(df_transactions)
    top_transactions = get_top_transactions(df_transactions)
    currency_rates = get_currency_rates()  # Получаем курсы валют
    stock_prices = get_stock_prices(stocks)
    final_response = {
        "greeting": greeting,
        "cards": cards,
        "top_transactions": top_transactions,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices,
    }

    return json.dumps(final_response, ensure_ascii=False, indent=4)
