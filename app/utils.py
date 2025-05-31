# app/utils.py
import pandas as pd
import numpy as np

def generate_signal_from_csv(df: pd.DataFrame):
    """
    Reads the DataFrame, calculates EMAs, and returns a signal plus explanation.
    """
    if df.empty or len(df) < 15:
        return "HOLD", "Insufficient data"

    # Calculate EMAs
    df['ema5'] = df['close'].ewm(span=5, adjust=False).mean()
    df['ema13'] = df['close'].ewm(span=13, adjust=False).mean()

    # Determine trend
    if df['ema5'].iloc[-1] > df['ema13'].iloc[-1]:
        last3 = df['close'].iloc[-3:]
        avg_range = np.mean(df['close'].diff().abs().iloc[-50:])
        # Check consolidation
        if max(last3) - min(last3) < avg_range * 0.5:
            if df['close'].iloc[-1] > max(last3[:-1]):
                return "BUY", "Upside momentum after tight consolidation"
    elif df['ema5'].iloc[-1] < df['ema13'].iloc[-1]:
        last3 = df['close'].iloc[-3:]
        avg_range = np.mean(df['close'].diff().abs().iloc[-50:])
        if max(last3) - min(last3) < avg_range * 0.5:
            if df['close'].iloc[-1] < min(last3[:-1]):
                return "SELL", "Downside momentum after tight consolidation"
    return "HOLD", "No clear setup"
