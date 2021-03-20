# Library of indicator functions

# Bollinger Band generator function
def bollinger_band_generator(dataframe_name, closing_price_column_name = 'close', bollinger_band_window = 20, num_standard_deviation = 2):
    """Creates Bollinger Band function
    Args:
        dataframe_name (dict): Single security dataframe containing at least closing prices
        closing_price_column_name (str): Name of column in dataframe containing closing prices
        bollinger_band_window (int): Desired timeframe window used for rolling calculations
        num_standard_deviation (int): Desired number of standard deviations to calculate
    Returns:
        A dataframe of:
            original data passed to function,
            bb_middle (flt): Column of values for middle band,
            bb_std (flt): Column of values to calculate standard deviation,
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

    # Return dataframe with features and target
    return dataframe_name
