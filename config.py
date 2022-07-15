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
    'indicator_output_path': 'models/ml_predictions.csv',     # FIXME: unnecessary, consider deleting  
    'predictions_output_path': None,   # FIXME: unnecessary, consider deleting
    'ohlc_file_column_list': [ "Open", "High", "Low", "Close", "Volume", "Unix", "Time"],
    'log_file_column_list': ["Open", "High", "Low", "Close", "Volume", "Unix", "Time", 'moving_average', 'meta', 'cci', 'volatility', 'top_variables', 'roc_momentum', 'rsi', '', 'median', 'action', 'falconx_usd_balance', 'falconx_btc_balance', 'falconx_btc_price_quote', 'trade_net_profit', 'running_trade_net_profit', 'trade_win_or_loss'],
    'output_log_file_path': 'bots/project_x_24hr/cvc_project_x_24hr_results_log.csv',
    'output_log_file_temp_path': 'tmp/cvc_project_x_24hr_results_log.csv',
    'threshold': 0.5,    # buy when median signal is at or above this level
    'bet': 1100,    # size of each bet in USD
    'execution_hours': [0],
    'data_reduction_factor': 24,
    'lookback_periods': [2, 3, 5, 7, 10, 14, 20, 30, 40, 50, 75, 100, 300, 600, 1000, 2400],
    'standard_deviation': 2,
    'num_ml_predictions': 10,
    'h2o_model_dict': {    # FIXME: update absolute paths depending on machine
        'meta': '/Users/hartimat/Documents/Energy On Chain/Projects/21-01 ChainviewCapital/codebase/cvc-projectx-24h/models/XGBoost_2_AutoML_1_20220714_73150_24hr_metamodel_py.zip',
        'moving_average': '/Users/hartimat/Documents/Energy On Chain/Projects/21-01 ChainviewCapital/codebase/cvc-projectx-24h/models/StackedEnsemble_BestOfFamily_6_AutoML_1_20220714_143405_24hr_mvg_avg_py.zip',
        'volatility': '/Users/hartimat/Documents/Energy On Chain/Projects/21-01 ChainviewCapital/codebase/cvc-projectx-24h/models/StackedEnsemble_BestOfFamily_4_AutoML_1_20220714_110310_24hr_volatility_py.zip',
        'rsi': '/Users/hartimat/Documents/Energy On Chain/Projects/21-01 ChainviewCapital/codebase/cvc-projectx-24h/models/XGBoost_grid_1_AutoML_1_20220715_73813_model_13_24hr_RSI_py.zip',
        'roc_momentum': '/Users/hartimat/Documents/Energy On Chain/Projects/21-01 ChainviewCapital/codebase/cvc-projectx-24h/models/GBM_grid_1_AutoML_1_20220715_103353_model_5_24hr_ROC_py.zip',
    },
    'h2o_jar_dict': {    # FIXME: update absolute paths depending on machine
        'meta': '/Users/hartimat/Documents/Energy On Chain/Projects/21-01 ChainviewCapital/codebase/cvc-projectx-24h/models/h2o-genmodel_24hr_metamodel_py.jar',
        'moving_average': '/Users/hartimat/Documents/Energy On Chain/Projects/21-01 ChainviewCapital/codebase/cvc-projectx-24h/models/h2o-genmodel_24hr_mvg_avg_py.jar',
        'volatility': '/Users/hartimat/Documents/Energy On Chain/Projects/21-01 ChainviewCapital/codebase/cvc-projectx-24h/models/h2o-genmodel_24hr_volatility_py.jar',
        'rsi': '/Users/hartimat/Documents/Energy On Chain/Projects/21-01 ChainviewCapital/codebase/cvc-projectx-24h/models/h2o-genmodel_24hrx_RSI_py.jar',
        'roc_momentum': '/Users/hartimat/Documents/Energy On Chain/Projects/21-01 ChainviewCapital/codebase/cvc-projectx-24h/models/h2o-genmodel_24hr_ROC_py.jar',
    },
    # TODO: additional config parameters go here
}

