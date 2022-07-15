###############################################################################
# PROJECT: CVC Project X 24hr Trading Bot
# AUTHOR: Matt Hartigan
# DATE: 15-Jun-2022
# FILENAME: machine_learning.py
# DESCRIPTION: Performs the machine learning for project x 24h trading bot.
###############################################################################
import os
import pandas as pd
import numpy as np
import h2o
from google.cloud import storage
import datetime
import statistics as stats
import math

import utils.indicators
from config import config_params


# FUNCTIONS
def calculate_indicators(ohlc_df):
    """ Uses the input ohlc time history to calculate indicator values for all the
    lookback periods specified in the project config file. """

    # FORMAT INPUT DATA
    finage_df = ohlc_df.copy()
    finage_df.columns = config_params['ohlc_file_column_list']
    finage_df['Time'] = finage_df['Time'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))   
    finage_df = finage_df.iloc[-max(config_params['lookback_periods']):]    # clip input ohlc dataset to minimum size to speed up indicator calcs
    master_df = finage_df.copy()

    # ADD INDICATORS
    print('Calculating indicators... [' + str(datetime.datetime.utcnow()) + ']')
    master_df = finage_df.copy()    # master data frame that will hold all cols of all indicators

    # Bollinger bands
    bollinger_band_df = finage_df.copy()       
    for period in config_params['lookback_periods']:
        temp_bollinger_band_df = utils.indicators.bollinger_band(finage_df.copy(), "Close", period, config_params['standard_deviation'])
        bollinger_band_df = pd.merge(bollinger_band_df, temp_bollinger_band_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, bollinger_band_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Annualized historical volatility
    annualized_historical_volatility_df = finage_df.copy()    
    for period in config_params['lookback_periods']:
        temp_annualized_historical_volatility_df = utils.indicators.annualized_historical_volatility(finage_df.copy(), "Close", period)
        annualized_historical_volatility_df = pd.merge(annualized_historical_volatility_df, temp_annualized_historical_volatility_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, annualized_historical_volatility_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Garman klass volatility
    garman_klass_df = finage_df.copy()    
    for period in config_params['lookback_periods']:
        temp_garman_klass_df = utils.indicators.garman_klass_volatility(finage_df.copy(), "Open", "High", "Low", "Close", period)
        garman_klass_df = pd.merge(garman_klass_df, temp_garman_klass_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, garman_klass_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Simple moving average
    sma_df = finage_df.copy()    
    for period in config_params['lookback_periods']:
        temp_sma_df = utils.indicators.sma(finage_df.copy(), "Close", period)
        sma_df = pd.merge(sma_df, temp_sma_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, sma_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Zero lag exponential moving average FIXME: turn back on
    zlema_df = finage_df.copy()    
    for period in config_params['lookback_periods']:
        temp_zlema_df = utils.indicators.zlema(finage_df.copy(), "Close", period)
        zlema_df = pd.merge(zlema_df, temp_zlema_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, zlema_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Volume weighted average price
    vwap_df = finage_df.copy()    
    for period in config_params['lookback_periods']:
        temp_vwap_df = utils.indicators.vwap(finage_df.copy(), "Close", "High", "Low", "Volume", period)
        vwap_df = pd.merge(vwap_df, temp_vwap_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, vwap_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Relative strength index
    rsi_df = finage_df.copy()    
    for period in config_params['lookback_periods']:
        temp_rsi_df = utils.indicators.rsi(finage_df.copy(), "Close", period)
        rsi_df = pd.merge(rsi_df, temp_rsi_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, rsi_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Commodity channel index
    cci_df = finage_df.copy()    
    for period in config_params['lookback_periods']:
        temp_cci_df = utils.indicators.cci(finage_df.copy(), "High", "Low", "Close", period)
        cci_df = pd.merge(cci_df, temp_cci_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, cci_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Money flow index
    money_flow_index_df = finage_df.copy()    
    for period in config_params['lookback_periods']:
        temp_money_flow_index_df = utils.indicators.money_flow_index(finage_df.copy(), "Close", "High", "Low", "Volume", period)
        money_flow_index_df = pd.merge(money_flow_index_df, temp_money_flow_index_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, money_flow_index_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Rate of change
    roc_df = finage_df.copy()    
    for period in config_params['lookback_periods']:
        temp_roc_df = utils.indicators.roc(finage_df.copy(), "Close", period)
        roc_df = pd.merge(roc_df, temp_roc_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, roc_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Momentum
    momentum_df = finage_df.copy()    
    for period in config_params['lookback_periods']:
        temp_momentum_df = utils.indicators.momentum(finage_df.copy(), "Close", period)
        momentum_df = pd.merge(momentum_df, temp_momentum_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, momentum_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Chande momentum oscillator
    chande_momentum_oscillator_df = finage_df.copy()    
    for period in config_params['lookback_periods']:
        temp_chande_momentum_oscillator_df = utils.indicators.chande_momentum_oscillator(finage_df.copy(), "Close", period)
        chande_momentum_oscillator_df = pd.merge(chande_momentum_oscillator_df, temp_chande_momentum_oscillator_df, on=config_params['ohlc_file_column_list'])
    master_df = pd.merge(master_df, chande_momentum_oscillator_df, on=config_params['ohlc_file_column_list'])    # add to master

    # Add additional cols
    master_df['C1'] = (master_df['Close'].shift(periods=-1) - master_df['Close']) / master_df['Close']    # calc % changes 1 period into future
    master_df['target'] = np.where(master_df['C1']>0,1,0)    # create binary target variable column
    # master_df.insert(0, 'fold', range(1, 1 + len(master_df)))    # add fold column
    master_df.to_csv(config_params['indicator_output_path'], index=False)    # output to local models file as csv

    prediction_input_df = master_df.iloc[-config_params['num_ml_predictions']:, :]    # trim down to just necessary predictions
    
    return prediction_input_df


def apply_online_machine_learning(prediction_input_df):
    """ Use h2o to calculate model predictions values by connecting to their servers online. """

    # RUN H2O
    # Initialize connection
    h2o.init()

    # Load indicators
    observations = h2o.import_file(path=config_params['indicator_output_path'], destination_frame='observations')

    # Load models
    # Moving average
    moving_average_model = h2o.import_mojo(config_params['h2o_model_dict']['moving_average'])
    moving_average_predictions = moving_average_model.predict(observations)

    # Metamodel
    meta_model = h2o.import_mojo(config_params['h2o_model_dict']['meta'])
    meta_predictions = meta_model.predict(observations)

    # RSI
    rsi_model = h2o.import_mojo(config_params['h2o_model_dict']['rsi'])
    rsi_predictions = rsi_model.predict(observations)

    # ROC momentum
    roc_momentum_model = h2o.import_mojo(config_params['h2o_model_dict']['roc_momentum'])
    roc_momentum_predictions = roc_momentum_model.predict(observations)

    # Volatility
    volatility_model = h2o.import_mojo(config_params['h2o_model_dict']['volatility'])
    volatility_predictions = volatility_model.predict(observations)

    # Extract and output predictions
    prediction_df = pd.DataFrame()
    prediction_df['moving_average'] = moving_average_predictions.as_data_frame()['p1']
    prediction_df['meta'] = meta_predictions.as_data_frame()['p1']
    prediction_df['rsi'] = rsi_predictions.as_data_frame()['p1']
    prediction_df['roc_momentum'] = roc_momentum_predictions.as_data_frame()['p1']
    prediction_df['volatility'] = volatility_predictions.as_data_frame()['p1']
    prediction_list = [
        prediction_df['meta'].iloc[-1],
        prediction_df['moving_average'].iloc[-1],
        prediction_df['volatility'].iloc[-1],
        prediction_df['rsi'].iloc[-1],
        prediction_df['roc_momentum'].iloc[-1],
    ]

    prediction_dict = {
        'meta': prediction_df['meta'].iloc[-1],
        'moving_average': prediction_df['moving_average'].iloc[-1],
        'volatility': prediction_df['volatility'].iloc[-1],
        'rsi': prediction_df['rsi'].iloc[-1],
        'roc_momentum': prediction_df['roc_momentum'].iloc[-1],
        'cci': None,
        'top_variables': None,
        'mean': stats.mean(prediction_list),
        'median': stats.median(prediction_list),
    }
    
    return prediction_dict


def apply_offline_machine_learning(prediction_input_df):
    """ Use h2o to calculate model prediction values without connecting to h2o servers. """

    # Model 1 - meta
    m1_df = h2o.mojo_predict_pandas(
        prediction_input_df, 
        config_params['h2o_model_dict']['meta'],
        config_params['h2o_jar_dict']['meta'],
    )
    m1_prediction = m1_df['p1'].iloc[-1]
    print()

    # Model 2 - moving average
    m2_df = h2o.mojo_predict_pandas(
        prediction_input_df, 
        config_params['h2o_model_dict']['moving_average'],
        config_params['h2o_jar_dict']['moving_average'],
    )
    m2_prediction = m2_df['p1'].iloc[-1]
    print()

    # Model 3 - volatility
    m3_df = h2o.mojo_predict_pandas(
        prediction_input_df, 
        config_params['h2o_model_dict']['volatility'],
        config_params['h2o_jar_dict']['volatility'],
    )
    m3_prediction = m3_df['p1'].iloc[-1]
    print()

    # Model 4 - rsi
    m4_df = h2o.mojo_predict_pandas(
        prediction_input_df, 
        config_params['h2o_model_dict']['rsi'],
        config_params['h2o_jar_dict']['rsi'],
    )
    m4_prediction = m4_df['p1'].iloc[-1]
    print()

    # Model 5 - roc momentum
    m5_df = h2o.mojo_predict_pandas(
        prediction_input_df, 
        config_params['h2o_model_dict']['roc_momentum'],
        config_params['h2o_jar_dict']['roc_momentum'],
    )
    m5_prediction = m5_df['p1'].iloc[-1]
    print()

    prediction_dict = {
        'meta': m1_prediction,
        'moving_average': m2_prediction,
        'volatility': m3_prediction,
        'rsi': m4_prediction,
        'roc_momentum': m5_prediction,
        'cci': None,
        'top_variables': None,
        'mean': stats.mean([m1_prediction, m2_prediction, m3_prediction, m4_prediction, m5_prediction]),
        'median': stats.median([m1_prediction, m2_prediction, m3_prediction, m4_prediction, m5_prediction]),
    }

    return prediction_dict













