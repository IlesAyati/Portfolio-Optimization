import pandas as pd
from settings import settings
import eikon as ek

class eikon_companies_extractor:
    def __init__(self):
        print('Initialised Companies Extractor')
        pass

    def get_companies_list(current_portfolio=None):
        # Get list of tickers OSEBX
        rics, ee =  ek.get_data(instruments = '0#.OSEBX',
                                fields = ['TR.RIC'])
        rics.drop(columns = 'Instrument', inplace=True)
        return list(rics['RIC'])

class static_companies_extractor:
    def __init__(self, my_companies):
        self.__my_companies = my_companies

    def get_companies_list(self, current_portfolio=None):
        return self.__my_companies #pd.DataFrame({'Ticker':self.__my_companies})
