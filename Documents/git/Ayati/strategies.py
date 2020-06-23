# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 22:45:29 2020

@author: iles_
"""
import pandas as pd
import numpy as np

class strategies:
    """ A collection of functions which signal the automated trading 
    transactions."""
    def __init__(self):
        pass

    @staticmethod
    def strategy_sma(closing_prices, sma1, sma2):
        positions = pd.DataFrame()
        for col in closing_prices.columns:
            positions[col] = np.where(sma1[col] > sma2[col], 1, -1)
        return positions
