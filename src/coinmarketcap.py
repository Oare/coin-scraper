from src.helpers.driver_initializer import DriverInitializer
from src.helpers.coins import Coin


class CoinMarketCap:

    def __init__(self, coins_count, headless):
        self.URL = "https://coinmarketcap.com/coins/?page=1"
        self.__driver = ""
        self.coins_count = coins_count
        self.coins = {}
        self.retry = 3
        self.headless = headless

    def __start_driver(self):
        self.__driver = DriverInitializer(self.headless).init()

    def __close_driver(self):
        self.__driver.close()
        self.__driver.quit()

    def __fetch_data(self):
        try:
            elements = Coin.element_list(self.__driver, self.coins_count)
            if len(elements) > 0:
                for index, url in enumerate(elements, start=1):
                    self.__driver.get(url)
                    self.coins[index] = Coin.coin_data(self.__driver)
        except Exception as ex:
            pass

    def scrap(self):
        try:
            self.__start_driver()
            self.__driver.get(self.URL)
            self.__fetch_data()
            self.__close_driver()
            return None
        except Exception as ex:
            self.__close_driver()


def run():
    CoinMarketCap(2, False).scrap()


if __name__ == '__main__':
    run()