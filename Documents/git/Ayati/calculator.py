import numpy as np
from functools import reduce
import pandas as pd

class risk_return_calculator:
    @staticmethod
    def calculate_assets_expectedreturns(returns):
            return returns.mean() * 252

    @staticmethod
    def calculate_assets_covariance(returns):
            return returns.cov() * 252

    @staticmethod
    def calculate_portfolio_expectedreturns(returns, allocations):
        return sum(returns * allocations)

    @staticmethod
    def calculate_portfolio_risk(allocations, cov):
        return np.sqrt(reduce(np.dot, [allocations, cov, allocations.T]))

    @staticmethod
    def calculate_daily_asset_returns(stock_prices, return_type):
        return np.log(stock_prices / stock_prices.shift(1))

class metrics_calculator:

    @staticmethod
    def get_sma(closing_prices, SMA):
        closing_prices = pd.DataFrame(closing_prices)
        sma = pd.DataFrame()
        for col in closing_prices.columns:
            if closing_prices[col].empty:
                pass
            else:
                sma[col] = closing_prices[col].rolling(SMA,axis=0, min_periods=1).mean()
        return sma

    @staticmethod
    def calculate_sharpe_ratio(risk, returns, risk_free_rate):
        return (returns-risk_free_rate)/risk

    @staticmethod
    def get_max_sharpe_ratio(df):
        return df.iloc[df['SharpeRatio'].astype(float).idxmax()]

    @staticmethod
    def get_min_risk(df):
        return df.iloc[df['Risk'].astype(float).idxmin()]

    @staticmethod
    def calculate_investment_return(positions,returns):
        investment_return = positions.shift(1)*returns
        investment_level = pd.DataFrame(np.exp(investment_return), 
                                        index = positions.index,
                                        columns=positions.columns).cumprod()
        #
        investment_level['Mean Return'] = investment_level.mean(axis=1)
        return investment_level
