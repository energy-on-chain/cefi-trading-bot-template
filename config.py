###############################################################################
# PROJECT: CVC Project X 24hr Trading Bot
# AUTHOR: Matt Hartigan
# DATE: 15-July-2022
# FILENAME: config.py
# DESCRIPTION: Defines the key parameters for this trading bot.
###############################################################################

config_params = {
    'name': 'CVC Project X 24hr Trading Bot',
    'version': 'v0.1.0',    # maintain versioning based on https://semver.org/
    'in_production': False,
    'output_results_to_cloud': True,
    'cloud_bucket_name': 'chainview-capital-dashboard-bucket-official',
    'cloud_bucket_path': 'bots/project_x_24hr/',
    'input_price_file_path': 'gs://chainview-capital-dashboard-bucket-official/data/finage_fast/finage_ohlc_BTCUSD_24hr_fast.csv',
    'input_log_file_path': 'gs://chainview-capital-dashboard-bucket-official/bots/project_x_24hr/cvc_project_x_24hr_results_log.csv',
    'input_machine_learning_file_path': None,    # FIXME: there is no external machine learning file in this full-python implementation of the bot (it's all done inside the bot)
    'indicator_output_path': None,     # FIXME: unnecessary, consider deleting  
    'predictions_output_path': None,   # FIXME: unnecessary, consider deleting
    'log_file_column_list': ["Open", "High", "Low", "Close", "Volume", "Unix", "Time", 'moving_average', 'meta', 'cci', 'volatility', 'top_variables', 'roc_momentum', 'rsi', '', 'median', 'action', 'falconx_usd_balance', 'falconx_btc_balance', 'falconx_btc_price_quote', 'trade_net_profit', 'running_trade_net_profit', 'trade_win_or_loss'],
    'output_log_file_path': 'bots/project_x_24hr/cvc_project_x_24hr_results_log.csv',
    'output_log_file_temp_path': 'tmp/cvc_project_x_24hr_results_log.csv',
    'threshold': 0.5,    # buy when median signal is at or above this level
    'bet': 1100,    # size of each bet in USD
    'execution_hours': [0],
    'data_reduction_factor': 24,
    'lookback_periods': [2, 3, 5, 7, 10, 14, 20, 30, 40, 50, 75, 100, 300, 600, 1000, 2400],
    'standard_deviation': 2,
    'num_ml_predictions': 1,
    'ml_dict': {
        'moving_average': 'models/24hr/',
        'meta': 'models/24hr/',
        'volatility': 'models/24hr/',
        'roc_momentum': 'models/24hr/',
        'rsi': 'models/24hr/',
    },
    'h2o_jar_dict': {
        'moving_average': 'models/24hr/',
        'meta': 'models/24hr/',
        'volatility': 'models/24hr/',
        'roc_momentum': 'models/24hr/',
        'rsi': 'models/24hr/',
    },
    # TODO: additional config parameters go here
}

