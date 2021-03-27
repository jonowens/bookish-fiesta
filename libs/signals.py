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
            macd_signal (flt): Column of signal values
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
