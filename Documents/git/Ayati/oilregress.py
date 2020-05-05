# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 14:12:21 2020

@author: iles_
"""

import eikon as ek
import pandas as pd  
import numpy as np
from companies_extractor import webpage_companies_extractor
import settings

class Data:
    def __init__(self):
        self.__rics = webpage_companies_extractor().get_companies_list()

    def get_prices_ebitda(self):
        # Get Prices and EBITDA
        rics = self.__rics
        df3, e = ek.get_data(instruments = rics, 
                             fields = ['TR.PriceClose.Date', 'TR.PriceClose', 'TR.NormalizedEbitda'],
                             parameters = {'SDate':'2015-04-28','EDate':'2020-04-28','Frq':'W'})
        df3.set_index('Date', append=True)
        df = df3.pivot_table(index = 'Date', columns= 'Instrument', values = ['Price Close', 'Normalized EBITDA'])
        df.index = pd.to_datetime(pd.DatetimeIndex(df.index).date)
        df = df.groupby(pd.Grouper(freq='W')).last()
        return df

dff = Data().get_prices_ebitda()
