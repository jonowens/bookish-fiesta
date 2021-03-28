# Library of signal functions

# Import necessary libraries
import pandas as pd

# MACD signals
def macd(dataframe_name, signal_lag = 9):
    """Creates MACD Signals
    Args:
        dataframe_name (df): Single security dataframe containing at least a 'macd' column
        signal_lag (int): Desired lag time used for macd rolling average
    Returns:
        A dataframe of:
            original data passed to function,
            macd_signal (flt): Column of signal values,
            macd_divergence (flt): Column of macd values minus the signal values
    Tip:
        signal_lag = 5 will provide greater sensitivity
    """

    # Calculate signal and divergence values
    # Thank you Camden Kirkland - https://www.youtube.com/watch?v=-o7ByZc0UN8
    dataframe_name['macd_signal'] = dataframe_name['macd'].rolling(signal_lag).mean()
    dataframe_name['macd_divergence'] = dataframe_name['macd'] - dataframe_name['macd_signal']

    return dataframe_name

# Bollingerbands inside Keltner Channels signals
def bbands_inside_kchannels(dataframe_name):
    """Creates signals for long position
    Args:
        dataframe_name (df): Dataframe containing indicator data for Bollinger Bands and Keltner Channels
    Returns:
        A dataframe of:
            original data passed to function,
            bbkc_squeeze (flt): Signals column (1.0 = True, 0.0 = False)
    """

    # Create signal for bollinger band is inside keltner channel
    selection = dataframe_name.loc[((dataframe_name['bb_upper'] < dataframe_name['kc_upper']) & (dataframe_name['bb_lower'] >= dataframe_name['kc_lower'])), :].index
    dataframe_name['bbkc_squeeze'] = 0.0
    dataframe_name.loc[selection, 'bbkc_squeeze'] = 1.0
    
    # Return dataframe with features and target
    return dataframe_name

# Exponential Weighted Moving Average signals (up and down)
def ewma_crossovers(dataframe_name):
    """Creates up and down signals for exponential weighted moving averages
    Args:
        dataframe_name (df): Dataframe containing ewma fast and slow indicator data,
    Returns:
        A dataframe of:
            original data passed to function,
            ewma_cross_up (flt): Signals column (1.0 = True, 0.0 = False),
            ewma_cross_down (flt): Signals column (-1.0 = True, 0.0 = False)
    """

    # Create signal for crossover band (cross in the up direction)
    time_crossed_up = dataframe_name.loc[((dataframe_name['ewma_fast'] > dataframe_name['ewma_slow']) & (dataframe_name['ewma_fast'].shift(1) < dataframe_name['ewma_slow'].shift(1))), :].index
    dataframe_name['ewma_cross_up'] = 0.0
    dataframe_name.loc[time_crossed_up, 'ewma_cross_up'] = 1.0

    # Create signal for crossover band (cross in the down direction)
    time_crossed_down = dataframe_name.loc[((dataframe_name['ewma_fast'] < dataframe_name['ewma_slow']) & (dataframe_name['ewma_fast'].shift(1) > dataframe_name['ewma_slow'].shift(1))), :].index
    dataframe_name['ewma_cross_down'] = 0.0
    dataframe_name.loc[time_crossed_down, 'ewma_cross_down'] = -1.0

    return dataframe_name
