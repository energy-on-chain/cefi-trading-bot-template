###############################################################################
# PROJECT: CVC Project X 2hr Trading Bot
# AUTHOR: Matt Hartigan
# DATE: 6-July-2022
# FILENAME: performance.py
# DESCRIPTION: Evalates how the trade strategy performed.
###############################################################################
import os
import shutil
import pandas as pd
import datetime

from google.cloud import storage

from config import config_params


def evaluate_performance(df):
    """ Evaluate the performance of an individual trading bot. """

    # Setup cloud connection
    storage_client = storage.Client()
    bucket = storage_client.bucket(config_params['cloud_bucket_name'])

    # Create dir for temp files if it doesn't already exist
    if not os.path.exists(os.path.join(os.getcwd(), 'tmp')):    
        os.mkdir(os.path.join(os.getcwd(), 'tmp'))

    # Evaluate individual results and output to cloud
    df.loc[df['action'] == 'Sell', 'trade_net_profit'] = pd.to_numeric(df['usd_received'])  - config_params['bet']
    df.loc[df['action'] == 'Buy', 'trade_net_profit'] = 0   
    df.loc[df['action'] == 'Hold', 'trade_net_profit'] = 0   
    df.loc[df['action'] == 'No Action', 'trade_net_profit'] = 0   

    # Identify winning and losing trades
    df['trade_win_or_loss'] = None    # default value
    df.loc[(df['action'] == 'Sell') & (df['trade_net_profit'] > 0), 'trade_win_or_loss'] = 'Win'
    df.loc[(df['action'] == 'Sell') & (df['trade_net_profit'] < 0), 'trade_win_or_loss'] = 'Loss'

    # Calculate running balances
    df['running_trade_net_profit'] = df['trade_net_profit'].cumsum()

    # Create cloud blob
    blob = bucket.blob(config_params['output_log_file_path'])

    # Create local file
    local_file = config_params['output_log_file_temp_path']
    df.to_csv(local_file, index=False)

    # Upload to cloud
    if config_params['in_production'] or config_params['output_results_to_cloud']:
        print('Writing results to cloud... [' + str(datetime.datetime.utcnow()) + ']')
        blob.upload_from_filename(local_file)   

    # Tear down temp dir
    shutil.rmtree(os.path.join(os.getcwd(), 'tmp'))

