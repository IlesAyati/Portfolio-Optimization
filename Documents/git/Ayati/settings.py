import numpy as np
import datetime as dt
from calculator import risk_return_calculator
import configparser as cp
import eikon as ek

class settings:
    cfg = cp.ConfigParser()
    cfg.read('eikon.cfg')
    ek.set_app_key(cfg['eikon']['app_id'])
    PriceEvent = 'Adj Close'
    ReturnType = 'Geometric'
    Optimisersettings = {}
    OptimiserType = 'OLS'
    CompaniesUrl = 'https://www.oslobors.no/markedsaktivitet/#/list/shares/quotelist/ob/all/all/false'
    NumberOfPortfolios = 100000 #0000#0
    API = 'eikon'
    YearsToGoBack = 5
    RiskFreeRate = 0.019
    SMA1 = 8
    SMA2 = 21
    SMA3 = 200
    Interval = 'Daily'
    CompanyFetchMode = "PreFixed" #Auto
    MyCompanies = ['NOD.OL', 'KOA.OL', 'AMSCA.OL', 'B2H.OL', 'GOGLT.OL', 'FKRAFT.OL', 'VEI.OL', 'ASETEK.OL', 'FRO.OL']
    PortfolioOptimisationPath = "PortfolioOptimisation.xlsx"
    RiskFunction = risk_return_calculator.calculate_portfolio_risk
    ReturnFunction = risk_return_calculator.calculate_portfolio_expectedreturns
    AssetsExpectedReturnsFunction = risk_return_calculator.calculate_assets_expectedreturns
    AssetsCovarianceFunction = risk_return_calculator.calculate_assets_covariance
    DailyAssetsReturnsFunction = risk_return_calculator.calculate_daily_asset_returns

    @staticmethod
    def get_my_targets():
        return np.arange(0, 1.5, 0.05)

    @staticmethod
    def get_end_date():
        return dt.date.today()

    @staticmethod
    def get_start_date(end_date):
        return end_date - dt.timedelta(days=settings.YearsToGoBack*365)
    
