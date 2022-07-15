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
def apply_machine_learning_logic(input_df, num_predictions, standard_deviation, lookback_periods):
    
    # LOCAL CONFIG FIXME: consider deleting these
    # indicator_output_path = 'models/1hr_h2o_indicator_feed.csv'
    # predictions_output_path = 'models/projectx_1hr_h2o_predictions.csv'
    # standard_deviation = 2
    # lookback_periods = [2, 3, 5, 7, 10, 14, 20, 30, 40, 50, 75, 100, 300, 600, 1000, 2400]
    # col_list = ["Open", "High", "Low", "Close", "Volume", "Unix", "Time"]
        

    # FORMAT INPUT DATA
    print('Formatting data... [' + str(datetime.datetime.utcnow()) + ']')
    start_data = datetime.datetime.utcnow()    # track execution time
    finage_df = input_df.copy()
    # finage_df = pd.read_csv('gs://chainview-capital-dashboard-bucket-official/bots/bot_6/finage_ohlc_BTCUSD_60minute_fast.csv')    # price data
    finage_df.columns = [ "Open", "High", "Low", "Close", "Volume", "Unix", "Time"]
    finage_df['Time'] = finage_df['Time'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    finage_df = finage_df.iloc[-max(lookback_periods):]
    master_df = finage_df.copy()
    end_data = datetime.datetime.utcnow()    # track execution time


    # ADD INDICATORS
    print('Adding indicators... [' + str(datetime.datetime.utcnow()) + ']')
    start_indicators = datetime.datetime.utcnow()
    master_df = finage_df.copy()    # master data frame that will hold all cols of all indicators

    # Bollinger bands
    bollinger_band_df = finage_df.copy()       
    for period in lookback_periods:
        temp_bollinger_band_df = utils.indicators.bollinger_band(finage_df.copy(), "Close", period, standard_deviation)
        bollinger_band_df = pd.merge(bollinger_band_df, temp_bollinger_band_df, on=col_list)
    master_df = pd.merge(master_df, bollinger_band_df, on=col_list)    # add to master

    # Annualized historical volatility
    annualized_historical_volatility_df = finage_df.copy()    
    for period in lookback_periods:
        temp_annualized_historical_volatility_df = utils.indicators.annualized_historical_volatility(finage_df.copy(), "Close", period)
        annualized_historical_volatility_df = pd.merge(annualized_historical_volatility_df, temp_annualized_historical_volatility_df, on=col_list)
    master_df = pd.merge(master_df, annualized_historical_volatility_df, on=col_list)    # add to master

    # Garman klass volatility
    garman_klass_df = finage_df.copy()    
    for period in lookback_periods:
        temp_garman_klass_df = utils.indicators.garman_klass_volatility(finage_df.copy(), "Open", "High", "Low", "Close", period)
        garman_klass_df = pd.merge(garman_klass_df, temp_garman_klass_df, on=col_list)
    master_df = pd.merge(master_df, garman_klass_df, on=col_list)    # add to master

    # Simple moving average
    sma_df = finage_df.copy()    
    for period in lookback_periods:
        temp_sma_df = utils.indicators.sma(finage_df.copy(), "Close", period)
        sma_df = pd.merge(sma_df, temp_sma_df, on=col_list)
    master_df = pd.merge(master_df, sma_df, on=col_list)    # add to master

    # Zero lag exponential moving average
    zlema_df = finage_df.copy()    
    for period in lookback_periods:
        temp_zlema_df = utils.indicators.zlema(finage_df.copy(), "Close", period)
        zlema_df = pd.merge(zlema_df, temp_zlema_df, on=col_list)
    master_df = pd.merge(master_df, zlema_df, on=col_list)    # add to master

    # Volume weighted average price
    vwap_df = finage_df.copy()    
    for period in lookback_periods:
        temp_vwap_df = utils.indicators.vwap(finage_df.copy(), "Close", "High", "Low", "Volume", period)
        vwap_df = pd.merge(vwap_df, temp_vwap_df, on=col_list)
    master_df = pd.merge(master_df, vwap_df, on=col_list)    # add to master

    # Relative strength index
    rsi_df = finage_df.copy()    
    for period in lookback_periods:
        temp_rsi_df = utils.indicators.rsi(finage_df.copy(), "Close", period)
        rsi_df = pd.merge(rsi_df, temp_rsi_df, on=col_list)
    master_df = pd.merge(master_df, rsi_df, on=col_list)    # add to master

    # Commodity channel index
    cci_df = finage_df.copy()    
    for period in lookback_periods:
        temp_cci_df = utils.indicators.cci(finage_df.copy(), "High", "Low", "Close", period)
        cci_df = pd.merge(cci_df, temp_cci_df, on=col_list)
    master_df = pd.merge(master_df, cci_df, on=col_list)    # add to master

    # Money flow index
    money_flow_index_df = finage_df.copy()    
    for period in lookback_periods:
        temp_money_flow_index_df = utils.indicators.money_flow_index(finage_df.copy(), "Close", "High", "Low", "Volume", period)
        money_flow_index_df = pd.merge(money_flow_index_df, temp_money_flow_index_df, on=col_list)
    master_df = pd.merge(master_df, money_flow_index_df, on=col_list)    # add to master

    # Rate of change
    roc_df = finage_df.copy()    
    for period in lookback_periods:
        temp_roc_df = utils.indicators.roc(finage_df.copy(), "Close", period)
        roc_df = pd.merge(roc_df, temp_roc_df, on=col_list)
    master_df = pd.merge(master_df, roc_df, on=col_list)    # add to master

    # Momentum
    momentum_df = finage_df.copy()    
    for period in lookback_periods:
        temp_momentum_df = utils.indicators.momentum(finage_df.copy(), "Close", period)
        momentum_df = pd.merge(momentum_df, temp_momentum_df, on=col_list)
    master_df = pd.merge(master_df, momentum_df, on=col_list)    # add to master

    # Chande momentum oscillator
    chande_momentum_oscillator_df = finage_df.copy()    
    for period in lookback_periods:
        temp_chande_momentum_oscillator_df = utils.indicators.chande_momentum_oscillator(finage_df.copy(), "Close", period)
        chande_momentum_oscillator_df = pd.merge(chande_momentum_oscillator_df, temp_chande_momentum_oscillator_df, on=col_list)
    master_df = pd.merge(master_df, chande_momentum_oscillator_df, on=col_list)    # add to master
    end_indicators = datetime.datetime.utcnow()


    # RUN H2O
    # Format data
    master_df = master_df.iloc[-num_predictions:]
    master_df['percentage'] = (master_df['Close'].shift(periods=-1) - master_df['Close']) / master_df['Close']    # calc % changes 1 period into future
    master_df['target'] = np.where(master_df['percentage']>0,1,0)    # create binary target variable column
    master_df.insert(0, 'fold', range(1, 1 + len(master_df)))    # add fold column
    master_df.to_csv(indicator_output_path, index=False)

    # Initialize connection
    print('Running h2o... [' + str(datetime.datetime.utcnow()) + ']')
    start_h2o = datetime.datetime.utcnow()
    h2o_start = str(datetime.datetime.utcnow())
    h2o.init()

    # Load indicators
    observations = h2o.import_file(path=indicator_output_path, destination_frame='observations')

    # Load models
    # Moving average
    moving_average_model = h2o.import_mojo("models/StackedEnsemble_AllModels_1_AutoML_1_20220518_160206_mvg_avg.zip")
    moving_average_predictions = moving_average_model.predict(observations)

    # Metamodel
    meta_model = h2o.import_mojo("models/GLM_1_AutoML_1_20220521_183746_metamodel.zip")
    meta_predictions = meta_model.predict(observations)

    # CCI
    cci_model = h2o.import_mojo("models/StackedEnsemble_BestOfFamily_1_AutoML_1_20220517_122535-CCI-2020.zip")
    cci_predictions = cci_model.predict(observations)

    # Volatility
    volatility_model = h2o.import_mojo("models/StackedEnsemble_BestOfFamily_2_AutoML_1_20220519_220910_vol.zip")
    volatility_predictions = volatility_model.predict(observations)

    # Extract and output predictions
    prediction_df = pd.DataFrame()
    prediction_df['moving_average'] = moving_average_predictions.as_data_frame()['p1']
    prediction_df['meta'] = meta_predictions.as_data_frame()['p1']
    prediction_df['cci'] = cci_predictions.as_data_frame()['p1']
    prediction_df['volatility'] = volatility_predictions.as_data_frame()['p1']
    prediction_df['mean'] = prediction_df.mean(axis=1)
    prediction_df['median'] = prediction_df.median(axis=1)
    print(prediction_df)

    h2o.shutdown(prompt=False)
    end_h2o = datetime.datetime.utcnow()

    # PRINT RUNTIME STATS TO SCREEN
    print('\nRuntime breakdown...')
    print('Time spent importing data: {}'.format(end_data - start_data))
    print('Time spent calculating indicators: {}'.format(end_indicators - start_indicators))
    print('Time spent running h2o: {}'.format(end_h2o - start_h2o))
    print('Total runtime: {}'.format(end_h2o - start_data))
    
    return prediction_df













