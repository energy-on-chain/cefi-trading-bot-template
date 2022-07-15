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
def apply_machine_learning(ohlc_df):
    
    # FORMAT INPUT DATA
    finage_df = ohlc_df.copy()
    finage_df.columns = config_params['ohlc_file_column_list']
    finage_df['Time'] = finage_df['Time'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))   
    finage_df = finage_df.iloc[-max(config_params['lookback_periods']):]    # clip input ohlc dataset to minimum size to speed up indicator calcs
    master_df = finage_df.copy()

    # ADD INDICATORS
    print('Calculating indicators... [' + str(datetime.datetime.utcnow()) + ']')
    start_indicators = datetime.datetime.utcnow()
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

    end_indicators = datetime.datetime.utcnow()


    # RUN H2O
    start_h2o = datetime.datetime.utcnow()
    prediction_input_df = master_df.iloc[-config_params['num_ml_predictions']:, :]

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
    end_h2o = datetime.datetime.utcnow()

    # PRINT MACHINE LEARNING RUNTIME STATS TO SCREEN
    print(prediction_dict)

    print('\nMachine Learning Runtime Breakdown...')
    print('Time spent calculating indicators: {}'.format(end_indicators - start_indicators))
    print('Time spent running h2o models (locally): {}'.format(end_h2o - start_h2o))
    print('Total machine learning module runtime: {}'.format(end_h2o - start_indicators))
    
    return prediction_dict













