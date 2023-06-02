
import pandas as pd

from src.base.enums import Exchange
from src.base.interfaces import ExchangeProxy
from src.proxy import BinanceSpotProxy, KucoinSpotProxy
from src.base.results import ServiceResult
import src.base.errors as error


class DataManager():

    def __init__(self, config: 'list[dict]'):

        self.__exchanges: 'dict[str, ExchangeProxy]' = {}

        for exchange_config in config:
            exchange_name = exchange_config['exchange']
            
            #TODO: check for valid exchange names.
            exchange = Exchange(exchange_name)

            symbols_config = exchange_config['symbols']
            exchange_proxy = self.__get_exchange_proxy(exchange, symbols_config)

            self.__exchanges[exchange.value] = exchange_proxy                    


    def __get_exchange_proxy(self, exchange: Exchange, symbols_config: 'list[dict]'):

        if exchange is Exchange.BinanceSpot:
            return BinanceSpotProxy(symbols_config)
        elif exchange is Exchange.BinanceFutures:
            raise NotImplementedError()
        elif exchange is Exchange.KucoinSpot:
            raise KucoinSpotProxy(symbols_config)
        elif exchange is Exchange.KucoinFutures:
            raise NotImplementedError()


    def __get_exchange(self, exchange_name: str):

        if exchange_name in self.__exchanges:
            return self.__exchanges[exchange_name]
        else:
            return None


    def get_candles(self, exchange_name: str, symbol_name: str, timeframe: str, count: int):
        
        exchange = self.__get_exchange(exchange_name)
        if exchange is None:
            return ServiceResult[pd.DataFrame](success=False, message=error.INVALID_EXCHANGE)

        return exchange.get_candles(symbol_name, timeframe, count)

        
        


