def add_sma(df, column="Close", window=20):
    df[f"SMA_{window}"] = df[column].rolling(window).mean()
    return df

def add_bollinger_bands(df, column="Close", window=20, num_std=2):
    sma = df[column].rolling(window).mean()
    std = df[column].rolling(window).std()

    df[f"BB_Upper"] = sma + num_std * std
    df[f"BB_Lower"] = sma - num_std * std

    return df

def add_rsi(df, column="Close", period=14):
    delta = df[column].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))
    return df

def add_stochastic(df, k_period=14, d_period=3):
    low_min = df["Low"].rolling(window=k_period).min()
    high_max = df["High"].rolling(window=k_period).max()

    # Fast %K
    df["Stoch_%K"] = (df["Close"] - low_min) * 100 / (high_max - low_min)

    # Slow %D
    df["Stoch_%D"] = df["Stoch_%K"].rolling(window=d_period).mean()

    return df

def add_all_indicators(df):
    df = add_sma(df, window=20)
    df = add_sma(df, window=50)
    df = add_bollinger_bands(df, window=20)

    df = add_rsi(df, period=14)
    df = add_stochastic(df, k_period=14, d_period=3)

    return df