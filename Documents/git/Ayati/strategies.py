# -*- coding: utf-8 -*-
"""
Created on Mon Jun 22 22:45:29 2020

@author: iles_
"""
import pandas as pd
from scipy.stats import linregress
import numpy as np
import pandas_datareader as pdr
from calculator import risk_return_calculator

class strategies:
    """ A collection of functions that the automated trading 
    transaction pattern. Positions are == 1 for "BUY" orders 
    and -1 for "SELL" orders. """

    def __init__(self):
        pass

    @staticmethod
    def strategy_sma(closing_prices, sma1, sma2):
        """
        Simple Moving Average Strategy:
            - Buy when short-horizon sma crosses above long-horizon sma.
            - Sell when short-horizon sma crosses below long-horizon sma.
            - Assumes a 5% transaction cost.
        """
        positions = pd.DataFrame()
        for col in closing_prices.columns:
            positions[col] = np.where(sma1[col] > sma2[col], 1, -1)
        positions.index = closing_prices.index
        return positions*0.95 # Discount for transaction cost

    @staticmethod
    def strategy_capm(returns, start_date):
        """
        CAPM using lagged optimal market portfolio tracker to predict 
        company stock return. Positions are assigned as follows:
            - Buy when predicted return > expected return
            - Sell when predicted return < expected return
            - No transaction costs. For now.
        """
        mkt_return = pdr.get_data_famafrench('F-F_Research_Data_Factors_daily',
                                             start='1-1-2010')[0]['Mkt-RF']/100
        rf = pdr.get_data_famafrench('F-F_Research_Data_Factors_daily',
                                             start='1-1-2010', end=start_date)[0]['RF']
        ols_capm = {'slope': None, 'intercept': None, 'r_value': None,
                    'p_value': None, 'std_err': None}
        returns = returns.shift(1)
        for ret in returns.columns:
            slope, intercept, r_value, p_value, std_err = linregress(mkt_return, y=returns[ret])
            ols_capm['slope'].add(slope)
            ols_capm['intercept'].add(intercept)
            ols_capm['r_value'].add(r_value)
            ols_capm['p_value'].add(p_value)
            ols_capm['std_err'].add(std_err)
        return ols_capm
