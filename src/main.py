import json
import pandas as pd
from src.utils import greet, get_cards, get_top_transactions, get_currency_rates, get_stock_prices


def main():
    # Загрузить данные из Excel файла
    transactions_data_path = "C:/Users/Макс/my_prj/Job-1/data/operations.xlsx"
    transactions = pd.read_excel(transactions_data_path)

    user_settings_path = "C:/Users/Макс/my_prj/Job-1/data/user_settings.json"

    result = {
        "greeting": greet(),
        "cards": get_cards(transactions),
        "top_transactions": get_top_transactions(transactions),
        "currency_rates": get_currency_rates(user_settings_path),
        "stock_prices": get_stock_prices(user_settings_path)
    }

    print(json.dumps(result, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
