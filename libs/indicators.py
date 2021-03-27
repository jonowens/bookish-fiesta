# Library of indicator functions

# Import necessary libraries
import pandas as pd

# Bollinger Band generator function
def bollinger_band_generator(dataframe_name, rolling_window = 20, num_standard_deviation = 2):
    """Creates Bollinger Band values
    Args:
        dataframe_name (df): Single security dataframe containing at least closing prices
        rolling_window (int): Desired timeframe window used for rolling calculations
        num_standard_deviation (int): Desired number of standard deviations to calculate
    Returns:
        A dataframe of:
            original data passed to function,
            bb_upper (flt): Column of values for upper band,
            bb_middle (flt): Column of values for middle band,
            bb_lower (flt): Column of values for lower band
    """

    # Calculate middle bollinger band, mean, and standard deviation
    dataframe_name['bb_middle'] = dataframe_name['close'].rolling(window=rolling_window).mean()
    dataframe_name['bb_std'] = dataframe_name['close'].rolling(window=rolling_window).std()

    # Calculate upper bollinger band and lower bollinger band
    dataframe_name['bb_upper'] = dataframe_name['bb_middle'] + (dataframe_name['bb_std'] * num_standard_deviation)
    dataframe_name['bb_lower'] = dataframe_name['bb_middle'] - (dataframe_name['bb_std'] * num_standard_deviation)

    # Drop NaN values
    #dataframe_name.dropna(inplace=True)

    # Pop bb_std column
    dataframe_name.pop('bb_std')

    # Sort columns
    dataframe_name = dataframe_name[['open', 'high', 'low', 'close', 'volume', 'bb_upper', 'bb_middle', 'bb_lower']]

    # Return dataframe with features
    return dataframe_name

# Average True Range generator function
def average_true_range_generator(dataframe_name, span_timeframe = 20):
    """Creates Average True Range values
    Args:
        dataframe_name (df): Single security dataframe containing 'open', 'high',
            'low', and 'close' columns
        span_timeframe (int): Desired timeframe window used for moving averages
    Returns:
        A dataframe of:
            original data passed to function,
            atr (flt): Column of average true range values
    """

    # Instantiate variables
    count = 1
    true_range_list = []

    # Iterate through dataframe
    while count < len(dataframe_name.index):

        # Find help from http://auto.tradingninja.com/how-to-calculate-average-true-range-keltner-channels/
        # Determine true range for one period
        true_range = max(dataframe_name['high'][count], dataframe_name['close'][count - 1]) - min(dataframe_name['low'][count], dataframe_name['close'][count - 1])

        # Append true range value to list
        true_range_list.append(true_range)

        # Increment i
        count += 1

    # Change true range list into dataframe
    true_range_df = pd.DataFrame(true_range_list)

    # Calculate average true range based on exponential weighted moving average
    atr = pd.DataFrame(true_range_df[0].ewm(span=span_timeframe, min_periods=span_timeframe).mean())

    # Change atr to dataframe and assign column name
    atr_df = pd.DataFrame(atr)
    atr_df.columns = ['atr']

    # Reset the index of the passed dataframe
    dataframe_name.reset_index(inplace=True)
    
    # Join the average true range to the passed dataframe
    dataframe_name = dataframe_name.join(atr_df)

    # Set dataframe index
    dataframe_name.set_index('time', inplace=True)

    # Drop NaN values
    #dataframe_name.dropna(inplace=True)

    # Return dataframe with features
    return dataframe_name

# Keltner Channel generator function
def keltner_channel_generator(dataframe_name, span_timeframe = 20, deviation = 2):
    """Creates Keltner Channels with Average True Range values
    Args:
        dataframe_name (df): Single security dataframe containing 'open', 'high',
            'low', and 'close' columns
        deviation (int): Number of deviations from keltner middle line
        span_timeframe (int): Desired timeframe window used for moving averages
    Returns:
        A dataframe of:
            original data passed to function,
            atr (flt): Column of average true range values
            kc_upper (flt): Column of values for upper band,
            kc_middle (flt): Column of values for middle band,
            kc_lower (flt): Column of values for lower band
    """

    # Generate average true range values
    dataframe_name = average_true_range_generator(dataframe_name)

    # Find help from https://www.investopedia.com/terms/k/keltnerchannel.asp
    # Calculate middle keltner channel (exponential weighted moving average)
    dataframe_name['kc_middle'] = dataframe_name['close'].ewm(span=span_timeframe, min_periods=span_timeframe).mean()

    # Calculate upper keltner channel (EMA + (Deviation * Average True Range))
    dataframe_name['kc_upper'] = (dataframe_name['kc_middle'] + (deviation * dataframe_name['atr']))
            
    # Calculate lower keltner channel (EMA - (Deviation * Average True Range))
    dataframe_name['kc_lower'] = (dataframe_name['kc_middle'] - (deviation * dataframe_name['atr']))

    # Sort columns
    dataframe_name = dataframe_name[['open', 'high', 'low', 'close', 'volume', 'bb_upper', 'bb_middle', 'bb_lower', 'atr', 'kc_upper', 'kc_middle', 'kc_lower']]

    # Return dataframe with features
    return dataframe_name

# MACD generator function
def macd_generator(dataframe_name, fast = 12, slow = 26):
    """Creates MACD values
    Args:
        dataframe_name (df): Single security dataframe containing at least a 'close' column
        fast (int): Desired timeframe window used for fast exponential moving averages
        slow (int): Desired timeframe window used for slow exponential moving averages
    Returns:
        A dataframe of:
            original data passed to function,
            macd_fast (flt): Column of values for fast average
            macd_slow (flt): Column of values for slow average
            macd (flt): Column of values for macd
    Tip:
        fast = 5 and slow = 35 will provide greater sensitivity
    """

    # Calculate fast, slow, macd, signal and divergence values
    # Thank you Camden Kirkland - https://www.youtube.com/watch?v=-o7ByZc0UN8
    dataframe_name['macd_fast'] = dataframe_name['close'].ewm(span=fast).mean()
    dataframe_name['macd_slow'] = dataframe_name['close'].ewm(span=slow).mean()
    dataframe_name['macd'] = dataframe_name['macd_slow'] - dataframe_name['macd_fast']

    return dataframe_name
