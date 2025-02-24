import json
import logging

import pandas as pd

from src.utils import get_cards, get_currency_rates, get_stock_prices, get_top_transactions, greet

# Настроить логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    logging.info("Начало выполнения программы")

    # Загрузить данные из Excel файла
    transactions_data_path = "C:/Users/Макс/my_prj/Job-1/data/operations.xlsx"
    logging.info("Загрузка данных из файла: %s", transactions_data_path)
    transactions = pd.read_excel(transactions_data_path)

    user_settings_path = "C:/Users/Макс/my_prj/Job-1/data/user_settings.json"
    logging.info("Загрузка данных из файла: %s", user_settings_path)

    result = {
        "greeting": greet(),
        "cards": get_cards(transactions),
        "top_transactions": get_top_transactions(transactions),
        "currency_rates": get_currency_rates(user_settings_path),
        "stock_prices": get_stock_prices(user_settings_path),
    }

    logging.info("Результаты: %s", json.dumps(result, indent=4, ensure_ascii=False))

    print(json.dumps(result, indent=4, ensure_ascii=False))

    logging.info("Конец выполнения программы")


if __name__ == "__main__":
    main()
