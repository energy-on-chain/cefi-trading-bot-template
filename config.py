###############################################################################
# PROJECT: EOC CEFI Trading Bot Template 
# AUTHOR: Matt Hartigan
# DATE: 15-April-2022
# FILENAME: config.py
# DESCRIPTION: Defines the key parameters for this trading bot.
###############################################################################

config_params = {
    'name': 'EOC Cefi Trading Bot Template',
    'version': 'v0.1.0',    # maintain versioning based on https://semver.org/
    'in_production': False,
    'output_results_to_cloud': True,
    'cloud_bucket_name': '',    # FIXME: your value goes here
    'cloud_bucket_path': '',    # FIXME: your value goes here
    'input_price_file_path': '',    # FIXME: your value goes here
    'input_log_file_path': '',    # FIXME: your value goes here
    'input_machine_learning_file_path': '',    # FIXME: your value goes here
    'indicator_output_path': '',    # FIXME: your value goes here
    'predictions_output_path': '',    # FIXME: your value goes here
    'ohlc_file_column_list': [ "Open", "High", "Low", "Close", "Volume", "Unix", "Time"],
    'log_file_column_list': ["Open", "High", "Low", "Close", "Volume", "Unix", "Time", 'model1', 'mean', 'median', 'action', 'falconx_usd_balance', 'falconx_btc_balance', 'falconx_btc_price_quote', 'trade_net_profit', 'running_trade_net_profit', 'trade_win_or_loss'],
    'output_log_file_path': '',    # FIXME: your value goes here
    'output_log_file_temp_path': '',    # FIXME: your value goes here
    'threshold':'',    # FIXME: your numerical threshold value goes here
    'bet': 10000,    # size of each bet in USD
    'execution_hours': [0, 12],
    'data_reduction_factor': 12,
    'lookback_periods': [30, 60, 90],    # FIXME: your value goes here
    'standard_deviation': 2,
    'num_ml_predictions': 10,
    'h2o_model_dict': {    # FIXME: update absolute paths depending on machine
        'model1': '',    # FIXME: your value goes here
    },
    'h2o_jar_dict': {    # FIXME: update absolute paths depending on machine
        'model1': '',    # FIXME: your value goes here
    },
    # TODO: additional config parameters go here
}

