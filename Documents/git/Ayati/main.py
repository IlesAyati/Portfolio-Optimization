from settings import settings
from object_factory import object_factory
from mappers import portfolios_allocation_mapper

def generate_optimum_portfolio():
    """ Stepwise generation of optimum portfolios, using the monte carlo
    approach and then a Markowitz optimization approach. """
    # Initialize objects with the settings
    obj_factory = object_factory(settings)
    ce = obj_factory.get_companies_extractor()
    cp = obj_factory.get_charts_plotter()
    mcs = obj_factory.get_portfolio_generator()
    fr = obj_factory.get_file_repository()
    mc = obj_factory.get_metrics_calculator()
    st = obj_factory.get_strategies()

    print('1. Get companies')
    companies = ce.get_companies_list()
    price_extractor = obj_factory.get_price_extractor(companies)

    print('2. Get company stock prices')
    end_date = settings.get_end_date()
    start_date = settings.get_start_date(end_date)
    closing_prices = price_extractor.get_prices(start_date, end_date)
    sma1 = mc.get_sma(closing_prices, settings.SMA1)
    sma2 = mc.get_sma(closing_prices, settings.SMA2)

    # Plot stock prices & save data to a file
    #cp.plot_prices(closing_prices)
    positions = st.strategy_sma(closing_prices, sma1, sma2)
    #cp.plot_sma(sma1,sma2,positions)
    #fr.save_to_file(closing_prices, 'StockPrices')

    print('3. Calculate Daily Returns')
    returns = settings.DailyAssetsReturnsFunction(closing_prices, settings.ReturnType)
    # Calculate return of investment
    investments = mc.calculate_investment_return(positions,returns)
    # sdsdsd
    #ols_capm = st.strategy_capm(returns, start_date)
    # Plot stock prices & save data to a file
    cp.plot_investments(investments)
    #cp.plot_returns(returns)
    fr.save_to_file(returns, 'Returns')

    print('4. Calculate Expected Mean Return & Covariance')
    expected_returns = settings.AssetsExpectedReturnsFunction(returns)
    covariance = settings.AssetsCovarianceFunction(returns)

    # Plot & Save covariance to file
    #cp.plot_correlation_matrix(returns)
    fr.save_to_file(covariance, 'Covariances')

    print('5. Use Monte Carlo Simulation')
    # Generate portfolios with allocations
    portfolios_allocations_df = mcs.generate_portfolios(expected_returns, covariance, settings.RiskFreeRate)
    portfolio_risk_return_ratio_df = portfolios_allocation_mapper.map_to_risk_return_ratios(portfolios_allocations_df)

    # Plot portfolios, print max sharpe portfolio & save data
    #cp.plot_portfolios(portfolio_risk_return_ratio_df)
    max_sharpe_portfolio = mc.get_max_sharpe_ratio(portfolio_risk_return_ratio_df)['Portfolio']
    max_shape_ratio_allocations = portfolios_allocations_df[[ 'Symbol', max_sharpe_portfolio]]
    print(max_shape_ratio_allocations)
    portfolios_allocations_df = portfolios_allocations_df.T
    fr.save_to_file(portfolios_allocations_df, 'MonteCarloPortfolios')
    fr.save_to_file(portfolio_risk_return_ratio_df, 'MonteCarloPortfolioRatios')

    print('6. Use an optimiser')
    # Generate portfolios
    targets = settings.get_my_targets()
    optimiser = obj_factory.get_optimiser(targets, len(expected_returns.index))
    portfolios_allocations_df = optimiser.generate_portfolios(expected_returns, covariance, settings.RiskFreeRate)
    portfolio_risk_return_ratio_df = portfolios_allocation_mapper.map_to_risk_return_ratios(portfolios_allocations_df)
    max_sharpe_portfolio = mc.get_max_sharpe_ratio(portfolio_risk_return_ratio_df)['Portfolio']
    max_shape_ratio_allocations = portfolios_allocations_df[[ 'Symbol', max_sharpe_portfolio]]
    print(max_shape_ratio_allocations)

    # Plot efficient frontiers
    #cp.plot_efficient_frontier(portfolio_risk_return_ratio_df)
    #cp.show_plots()

    # Save data
    print('7. Saving Data')
    portfolios_allocations_df = portfolios_allocations_df.T
    fr.save_to_file(portfolios_allocations_df, 'OptimisationPortfolios')
    fr.close()

generate_optimum_portfolio()