# Library of indicator functions

# Import necessary libraries
import pandas as pd

# Bollinger Band generator function
def bollinger_band_generator(dataframe_name, closing_price_column_name = 'close', bollinger_band_window = 20, num_standard_deviation = 2):
    """Creates Bollinger Band values
    Args:
        dataframe_name (df): Single security dataframe containing at least closing prices
        closing_price_column_name (str): Name of column in dataframe containing closing prices
        bollinger_band_window (int): Desired timeframe window used for rolling calculations
        num_standard_deviation (int): Desired number of standard deviations to calculate
    Returns:
        A dataframe of:
            original data passed to function,
            bb_middle (flt): Column of values for middle band,
            bb_upper (flt): Column of values for upper band,
            bb_lower (flt): Column of values for lower band,
    """

    # Calculate mean and standard deviation
    dataframe_name['bb_middle'] = dataframe_name[closing_price_column_name].rolling(window=bollinger_band_window).mean()
    dataframe_name['bb_std'] = dataframe_name[closing_price_column_name].rolling(window=bollinger_band_window).std()

    # Calculate upper bollinger band and lower bollinger band
    dataframe_name['bb_upper'] = dataframe_name['bb_middle'] + (dataframe_name['bb_std'] * num_standard_deviation)
    dataframe_name['bb_lower'] = dataframe_name['bb_middle'] - (dataframe_name['bb_std'] * num_standard_deviation)

    # Drop NaN values
    dataframe_name.dropna(inplace=True)

    # Pop bb_std column
    dataframe_name.pop('bb_std')

    # Return dataframe with features
    return dataframe_name

# Average True Range generator function
def average_true_range_generator(dataframe_name, span_timeframe = 20):
    """Creates Average True Range values
    Args:
        dataframe_name (df): Single security dataframe containing 'open', 'high',
        'low', and 'close' columns
    Returns:
        A dataframe of:
            original data passed to function,
            ATR_## (flt): Column of values to calculate Keltner Channels
    """

    # Instantiate variables
    i = 0
    true_range_list = []

    # Iterate through dataframe
    while i < len(dataframe_name.index) - 1:

        # Determine true range for one period
        true_range = max(dataframe_name['high'][i + 1], dataframe_name['close'][i]) - min(dataframe_name['low'][i + 1], dataframe_name['close'][i])

        # Append true range value to list
        true_range_list.append(true_range)

        # Increment i
        i = i + 1

    # Change true range list into dataframe
    true_range_df = pd.DataFrame(true_range_list)

    # Calculate average true range based on exponential weighted moving average
    atr = true_range_df[0].ewm(span=span_timeframe, min_periods=span_timeframe).mean()

    # Change atr to dataframe and assign column name
    atr_df = pd.DataFrame(atr)
    atr_df.columns = ['atr']

    # Reset the index of the passed dataframe
    dataframe_name.reset_index(inplace=True)
    
    # Join the average true range to the passed dataframe
    dataframe_name = dataframe_name.join(atr_df)

    # Set dataframe index
    dataframe_name.set_index('time', inplace=True)

    # Return dataframe with features
    return dataframe_name

# Keltner Channel generator function
def keltner_channel_generator():
    pass