import pandas as pd
import numpy as np
from companies_extractor import dynamic_companies_extractor
#import eikon as ek
import quandl as quandl
import matplotlib.pyplot as plt
import scipy.optimize as solver
import datetime as dt
from functools import reduce

class price_extractor:
    """
    Takes a list of tickers and returns a dataframe of all their respective
    price history within the specified start and end dates.
    """
    def __init__(self, companies):
        self.__companies = companies
        self.__df3, self.__e = (pd.DataFrame(),pd.DataFrame())
        self.__df = pd.DataFrame()
        self.__prices = pd.DataFrame()
        print('Initialised Price Extractor')
#
    def get_prices(self, start_date, end_date):
        # Get prices
        self.__df3 = pd.DataFrame()
        self.__df = pd.DataFrame()
        self.__prices = pd.DataFrame()
        #self.__df3, self.__e = ek.get_data(instruments = self.__companies, 
        #                               fields = ['TR.PriceClose.Date', 'TR.PriceClose', 'TR.NormalizedEbitda'],
        #                               parameters = {'SDate':'{}'.format(start_date),'EDate':'{}'.format(end_date),'Frq':'D'})
        self.__df3 = quandl.get_table('WIKI/PRICES', ticker = self.__companies,
                                      qopts = { 'columns': ['date', 'ticker', 'adj_close'] },
                                      date = { 'gte': '{}'.format(start_date), 'lte': '{}'.format(end_date) }, paginate=True)
        self.__df3.set_index('date', append=True)
        self.__df = self.__df3.pivot_table(index = 'date', columns= 'ticker', values = ['adj_close'])
        self.__df.index = pd.to_datetime(pd.DatetimeIndex(self.__df.index).date)
        self.__df = self.__df.groupby(pd.Grouper(freq='D')).last()
        self.__prices = self.__df['adj_close']
        return self.__prices

class financials_extractor:
    """
    Takes a list of tickers and returns a dataframe of all their respective
    financials (from the financial statements) published in the specified 
    start and end dates.
    """
    def get_ebitda(self, start_date, end_date):
        # Get EBITDA
        self.__df3, self.__e = ek.get_data(instruments = self.__companies, 
                                       fields = ['TR.PriceClose.Date', 'TR.PriceClose', 'TR.NormalizedEbitda'],
                                       parameters = {'SDate':'{}'.format(start_date),'EDate':'{}'.format(end_date),'Frq':'D'})
        self.__df3.set_index('Date', append=True)
        self.__df = self.__df3.pivot_table(index = 'Date', columns= 'Instrument', values = ['Price Close', 'Normalized EBITDA'])
        self.__df.index = pd.to_datetime(pd.DatetimeIndex(self.__df.index).date)
        self.__df = self.__df.groupby(pd.Grouper(freq='D')).last()
        self.__ebitda = self.__df['Normalized EBITDA']
        return self.__ebitda
