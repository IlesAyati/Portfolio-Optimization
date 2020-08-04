import pandas as pd
import numpy as np
from settings import settings
#import eikon as ek
import quandl

class dynamic_companies_extractor:
    def __init__(self):
        self.API = settings.get_user_choice()
        print('Initialised Companies Extractor using {} API'.format(self.API))
        pass

    def get_companies_list(self, current_portfolio=None):
        if self.API == 'eikon':
            # Get list of tickers OSEBX using eikon
            rics, ee =  ek.get_data(instruments = '0#.OSEBX',
                                    fields = ['TR.RIC'])
            rics.drop(columns = 'Instrument', inplace=True)
            pass
        elif self.API == 'quandl':
            # Get list of tickers S&P500 using quandl
            financials = pd.read_csv('constituents-financials_csv.csv').to_dict()
            rics = list(financials['Symbol'].values())
            current_portfolio = rics[60:100]
            return current_portfolio
        else:
            print('Could not fetch companies!')

class static_companies_extractor:
    def __init__(self, my_companies):
        self.__my_companies = my_companies

    def get_companies_list(self, current_portfolio=None):
        return self.__my_companies #pd.DataFrame({'Ticker':self.__my_companies})
