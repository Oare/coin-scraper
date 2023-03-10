import time
import datetime

from src.helpers.analyzer import Analyzer
from src.helpers.config import Config
from src.helpers.driver_initializer import DriverInitializer
from src.helpers.file import File
from src.helpers.logger import Logger
from src.helpers.coins import Coin
from src.helpers.db import MysqlDb
from src.helpers.cleaner import Cleaner


class CoinMarketCap:

    def __init__(self, config):
        self.URL = f"https://coinmarketcap.com/coins/?page={config.START_PAGE_NO}"
        self.config = config
        self.driver = DriverInitializer(config.HEADLESS).init()
        self.coins = {}
        self.entry_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def fetch_data(self):
        try:
            elements = Coin.element_list(self.driver, self.config.COIN_LIMIT)
            for index, url in enumerate(elements, start=1):
                self.driver.get(url)
                self.coins[index] = Coin.coin_data(self.driver, self.entry_datetime, self.config)
                time.sleep(self.config.TIME_SLEEP)
        except Exception as e:
            Logger().error("Error in fetch_data method : {}".format(e))

    def scrape(self):
        try:
            self.driver.get(self.URL)
            self.fetch_data()
        except Exception as e:
            Logger().error("Error in scrape method : {}".format(e))
        finally:
            self.driver.close()
            self.driver.quit()
        data = dict(list(self.coins.items())[0:int(self.config.COIN_LIMIT)])
        return data


def run():
    config = Config()

    if config.ANALYZER_MODE in ['disabled', 'scrape-analyze']:
        Cleaner.data_cleanup(config)
        entries = CoinMarketCap(config).scrape()

        if config.DATA_FILE_USE:
            File.write_csv(filename=config.DATA_FILE_NAME, data=entries, directory=config.DATA_DIRECTORY)

        if config.DATA_DB_USE:
            db = MysqlDb(config)
            db.save_data(entries)

    if config.ANALYZER_MODE in ['analyze', 'scrape-analyze']:
        analyzer = Analyzer(config)
        analyzer.execute()


if __name__ == '__main__':
    run()
