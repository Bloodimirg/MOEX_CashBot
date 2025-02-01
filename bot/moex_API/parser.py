import requests
from requests.exceptions import ConnectTimeout, RequestException


class MoexAPI:
    """Парсер московской биржи"""

    def __init__(self):
        self.url = "https://iss.moex.com/iss/engines/stock/markets/"
        self.headers = {'User-Agent': 'HH-User-Agent'}

    def check_bond_ticker(self, ticker):
        """Проверка существования облигации и формирование ответа с данными"""
        url = self.url + f"bonds/securities/{ticker}.json"
        try:
            response = requests.get(url, headers=self.headers).json()

            security_data = [{k: r[i] for i, k in enumerate(response['securities']['columns'])} for r in
                             response['securities']['data']]

            market_data = [{k: r[i] for i, k in enumerate(response['marketdata']['columns'])} for r in
                           response['marketdata']['data']]

            combined_data = []
            for sec, market in zip(security_data, market_data):
                combined_entry = {**sec, **market}
                combined_data.append(combined_entry)
            # если не получили данные хотя бы из securities
            if not security_data:
                return None, "Данные этой облигации не доступны"

            return combined_data, None

        except ConnectTimeout:
            return None, "Ошибка соединения с сервером. Попробуйте позже."
        except RequestException as e:
            return None, f"Произошла ошибка: {str(e)}"
        except Exception as e:
            return None, f"Неизвестная ошибка: {str(e)}"

    def check_stock_ticker(self, ticker):
        """Проверка существования акции и формирование ответа с данными"""
        # url = self.url + f"shares/securities/{ticker}.json"
        # response = requests.get(url, headers=self.headers).json()
        # stock_data = [{k: r[i] for i, k in enumerate(response['marketdata']['columns'])} for r in
        #               response['marketdata']['data']]
        # if not stock_data:
        #     return None, f"Не существующая акция"
        #
        # return stock_data, None


if __name__ == "__main__":
    tiker = MoexAPI()
    # тестовая облигация
    print(tiker.check_bond_ticker('RU000A106UW3'))
