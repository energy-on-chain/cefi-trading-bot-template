###############################################################################
# PROJECT: CVC Project X 2hr Trading Bot
# AUTHOR: Matt Hartigan
# DATE: 6-July-2022
# FILENAME: individual_strategy.py
# DESCRIPTION: Defines criteria for bot entering / exiting trades.
###############################################################################
import pandas as pd
import numpy as np

from exchanges.falconx import get_falconx_btc_price_quote, get_all_falconx_accounts, get_single_falconx_account_balance, get_falconx_token_pairs, place_falconx_market_order
from config import config_params


def calculate_amount_to_sell():
    """ Calculates and returns the amount of BTC we want to sell on exchange based
    on the input logfile history. """
    # Get or otherwise calculate the amount of BTC bought... keep that in the logfile somewhere
    # Access this value and return it
    pass


def apply_strategy(exchange_connection, input_df, log_file_df, ml_df):
    """ Apply the strategy logic. Returns df with relevant results. """

    # Get current trade status (i.e. are we in an open position or not)
    trade_status = log_file_df['action'].iloc[-1]    # get trade status
    mean = ml_df['mean'].iloc[-1]    
    median = ml_df['median'].iloc[-1]    
    action = ''

    # Identify what trade action to take next
    if median > config_params['threshold']:    # in trade zone
        if trade_status == 'No Action':
            action = 'Buy'
            if config_params['in_production']:
                print('Buying ${} of BTC on FalconX.'.format(config_params['bet']))
                response = place_falconx_market_order(exchange_connection, config_params['bet'], ['BTC', 'USD'], 'buy')
                usd_received = 0
                btc_received = response['quantity_requested']['value']
                falconx_btc_price_quote = response['buy_price']
        elif trade_status == 'Buy':
            action = 'Sell'    
            if config_params['in_production']:
                print('Selling BTC on FalconX.')
                response = place_falconx_market_order(exchange_connection, log_file_df['btc_received'].iloc[-1], ['BTC', 'USD'], 'sell')    # sell all the btc received for the original purchase
                usd_received = response['position_in']['value']
                btc_received = 0 
                falconx_btc_price_quote = response['sell_price']
        elif trade_status == 'Sell':
            action = 'Buy'
            if config_params['in_production']:
                print('Buying ${} of BTC on FalconX.'.format(config_params['bet']))
                response = place_falconx_market_order(exchange_connection, config_params['bet'], ['BTC', 'USD'], 'buy')
                usd_received = 0
                btc_received = response['quantity_requested']['value']
                falconx_btc_price_quote = response['buy_price']
    else:    # not in trade zone
        if trade_status == 'No Action':
            action = 'No Action'
            usd_received = 0
            btc_received = 0
            falconx_btc_price_quote = get_falconx_btc_price_quote(exchange_connection)[0]
        elif trade_status == 'Buy':
            action = 'Sell'
            if config_params['in_production']:
                print('Selling BTC on FalconX.')
                response = place_falconx_market_order(exchange_connection, log_file_df['btc_received'].iloc[-1], ['BTC', 'USD'], 'sell')
                usd_received = response['position_in']['value']
                btc_received = 0 
                falconx_btc_price_quote = response['sell_price']
        elif trade_status == 'Sell':
            action = 'No Action'
            usd_received = 0
            btc_received = 0
            falconx_btc_price_quote = get_falconx_btc_price_quote(exchange_connection)[0]

    # Create new results row to append to log file
    input_df.columns = ["Open", "High", "Low", "Close", "Volume", "Unix", "Time"]
    new_entry = input_df.loc[input_df.index[-1], ["Open", "High", "Low", "Close", "Volume", "Unix", "Time"]].to_list()    # add ohlc
    new_entry = new_entry + ml_df.loc[ml_df.index[-1], ['moving_average', 'meta', 'cci', 'volatility', 'top_variables', 'roc_momentum', 'rsi', 'mean', 'median']].to_list()    # add ml
    new_entry = new_entry + [action]    # add action
    falconx_usd_balance = get_single_falconx_account_balance(exchange_connection, 'USD')    # add exchange state  
    falconx_btc_balance = get_single_falconx_account_balance(exchange_connection, 'BTC') 
    new_entry = new_entry + [falconx_usd_balance, falconx_btc_balance, falconx_btc_price_quote, usd_received, btc_received]
    new_entry = new_entry + [0, 0, np.nan]    # add placeholders for performance stats

    df = log_file_df.copy()    # append and return resulting df
    df.loc[len(df)] = new_entry
    print(df)

    return df
