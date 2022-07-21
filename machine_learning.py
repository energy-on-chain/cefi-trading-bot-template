###############################################################################
# PROJECT: EOC CEFI Trading Bot Template 
# AUTHOR: Matt Hartigan
# DATE: 15-April-2022
# FILENAME: machine_learning.py
# DESCRIPTION: Performs the machine learning for the bot.
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
    # FIXME: magic goes here...
    
    return master_df


def apply_online_machine_learning(prediction_input_df):
    """ Use h2o to calculate model predictions values by connecting to their servers online. """

    # RUN H2O
    # Initialize connection
    h2o.init()

    # Load indicators
    observations = h2o.import_file(path=config_params['indicator_output_path'], destination_frame='observations')

    # Load models
    # Model 1
    model1 = h2o.import_mojo(config_params['h2o_model_dict']['model1'])
    model1_predictions = model1.predict(observations)
    # FIXME: additional models go here with same pattern

    # Extract and output predictions
    prediction_df = pd.DataFrame()
    prediction_df['model1'] = model1_predictions.as_data_frame()['p1']
    # FIXME: additional model predictions go here with same pattern
    prediction_list = [
        prediction_df['model'].iloc[-1],
        # FIXME: additional model predictions go here with same pattern
    ]

    prediction_dict = {
        'model1': prediction_df['model1'].iloc[-1],
        # FIXME: additional model predictions go here with same pattern
        'mean': stats.mean(prediction_list),
        'median': stats.median(prediction_list),
    }
    
    return prediction_dict

