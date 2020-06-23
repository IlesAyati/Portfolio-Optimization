import pandas as pd
import numpy as np
from companies_extractor import eikon_companies_extractor
import eikon as ek
import matplotlib.pyplot as plt
import scipy.optimize as solver
import datetime as dt
from functools import reduce

class price_extractor:
    """ Returns a dictionary of price history keyed by RICS. """
    def __init__(self, companies):
        self.__companies = companies
        self.__df3, self.__e = (pd.DataFrame(),pd.DataFrame())
        self.__df = pd.DataFrame()
        self.__prices = pd.DataFrame()
        print('Initialised Price Extractor')

    def get_prices(self, start_date, end_date):
        # Get Prices and EBITDA
        self.__df3 = pd.DataFrame()
        self.__df = pd.DataFrame()
        self.__prices = pd.DataFrame()
        self.__df3, self.__e = ek.get_data(instruments = self.__companies, 
                                       fields = ['TR.PriceClose.Date', 'TR.PriceClose', 'TR.NormalizedEbitda'],
                                       parameters = {'SDate':'{}'.format(start_date),'EDate':'{}'.format(end_date),'Frq':'D'})
        self.__df3.set_index('Date', append=True)
        self.__df = self.__df3.pivot_table(index = 'Date', columns= 'Instrument', values = ['Price Close', 'Normalized EBITDA'])
        self.__df.index = pd.to_datetime(pd.DatetimeIndex(self.__df.index).date)
        self.__df = self.__df.groupby(pd.Grouper(freq='D')).last()
        self.__prices = self.__df['Price Close']
        return self.__prices

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
