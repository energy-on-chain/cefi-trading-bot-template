###############################################################################
# PROJECT: CVC Project X 2hr Trading Bot
# AUTHOR: Matt Hartigan
# DATE: 6-July-2022
# FILENAME: run.py
# DESCRIPTION: Main runfile and entry point for bot.
###############################################################################
import os
import time
import datetime
import requests
import schedule
import pandas as pd
import numpy as np

from exchanges.falconx import get_falconx_connection
from strategy import apply_strategy
from performance import evaluate_performance
from config import config_params


# AUTHENTICATE 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="credentials.json"


def alive():
    print(config_params['name'] + ' - ' + config_params['version'] + ' is busy printing money... [' + str(datetime.datetime.utcnow()) + ']')


def run():

    runtime_dict = {}    # place to log the runtimes for each section of interest in the bot
    current_hour = int(datetime.datetime.utcnow().hour)
    if current_hour in config_params['execution_hours']:

        print(config_params['name'] + ' - ' + config_params['version'] + ' is scheduled to run this hour! [' + str(datetime.datetime.utcnow()) + ']')

        # Connect exchanges
        print('\nConnecting exchanges... [' + str(datetime.datetime.utcnow()) + ']')
        runtime_dict['start_exchanges'] = datetime.datetime.utcnow()
        falconx_connection = get_falconx_connection()

        # Connect data and model file(s)
        print('Connecting data... [' + str(datetime.datetime.utcnow()) + ']')
        finage_df = pd.read_csv(config_params['input_price_file_path'])    # price data for log file 
        history_df = pd.read_csv(config_params['input_log_file_path'])    # historical bot output file

        # # Apply machine learning
        # print('Applying machine learning... [' + str(datetime.datetime.utcnow()) + ']')
        # print('FIXME: machine learning is performed in R for the current version of this bot')

        # # Apply strategy
        # print('Applying strategy... [' + str(datetime.datetime.utcnow()) + ']')
        # runtime_dict['start_strategy'] = datetime.datetime.utcnow()
        # strategy_result_df = apply_strategy(
        #     falconx_connection,
        #     finage_df,
        #     history_df,
        #     ml_df,
        #     )
        # runtime_dict['end_strategy'] = datetime.datetime.utcnow()
        # runtime_dict['strategy_runtime'] = runtime_dict['end_strategy'] - runtime_dict['start_strategy']

        # # Evaluate performance
        # print('Evaluating performance... [' + str(datetime.datetime.utcnow()) + ']')
        # runtime_dict['start_performance'] = datetime.datetime.utcnow()
        # evaluate_performance(
        #     strategy_result_df,
        #     )
        # runtime_dict['end_performance'] = datetime.datetime.utcnow()
        # runtime_dict['performance_runtime'] = runtime_dict['end_performance'] - runtime_dict['start_performance']

        # # Log total runtime
        # runtime_dict['total_runtime'] = runtime_dict['end_performance'] - runtime_dict['start_exchanges']
        # print('Run complete! [' + str(datetime.datetime.utcnow()) + ']')
        # for key, value in runtime_dict.items():
        #     if 'runtime' in key:
        #         print('{}: {}'.format(key, value))

    else: 
        print(config_params['name'] + ' - ' + config_params['version'] + ' is NOT scheduled to run this hour! [' + str(datetime.datetime.utcnow()) + ']')


# ENTRY POINT
if config_params['in_production']:
    schedule.every(1).minutes.do(alive)    
    schedule.every().hour.at(":01").do(run)    
    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    run()



# TODO:
#