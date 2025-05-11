import yfinance as yf
import pandas as pd

# 1. Input parameters
ticker = "2330.TW"
start_date = "2024-02-01"
end_date = "2024-04-30"

# 2. Fetch historical data
df = yf.download(ticker, start=start_date, end=end_date)

# If columns have MultiIndex, extract the first level column names
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# Confirm successful data retrieval
print("✅ Stock price data preview:")
print(df.head())

# 3. Calculate technical indicators
df['MA20'] = df['Close'].rolling(window=20).mean()

# Calculate RSI (14 days)
delta = df['Close'].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

# Calculate MACD (12, 26, 9 EMA)
ema12 = df['Close'].ewm(span=12, adjust=False).mean()
ema26 = df['Close'].ewm(span=26, adjust=False).mean()
macd_line = ema12 - ema26
signal_line = macd_line.ewm(span=9, adjust=False).mean()

avg_price = df['Close'].mean()

# Add multiple technical indicators

# Moving averages
df['MA5'] = df['Close'].rolling(window=5).mean()
df['MA10'] = df['Close'].rolling(window=10).mean()
df['MA30'] = df['Close'].rolling(window=30).mean()
df['MA60'] = df['Close'].rolling(window=60).mean()
df['MA120'] = df['Close'].rolling(window=120).mean()

# EMA
df['EMA5'] = df['Close'].ewm(span=5, adjust=False).mean()
df['EMA10'] = df['Close'].ewm(span=10, adjust=False).mean()
df['EMA30'] = df['Close'].ewm(span=30, adjust=False).mean()
df['EMA60'] = df['Close'].ewm(span=60, adjust=False).mean()
df['EMA120'] = df['Close'].ewm(span=120, adjust=False).mean()

# Volatility indicators
df['STD20'] = df['Close'].rolling(window=20).std()
df['STD50'] = df['Close'].rolling(window=50).std()
df['BOLL_UP'] = df['MA20'] + 2 * df['STD20']
df['BOLL_DOWN'] = df['MA20'] - 2 * df['STD20']

# Price range indicators
df['High-Low'] = df['High'] - df['Low']
df['Close-Open'] = df['Close'] - df['Open']

# Momentum indicators
df['Momentum10'] = df['Close'] - df['Close'].shift(10)
df['ROC10'] = df['Close'].pct_change(periods=10) * 100

# Williams %R indicator
high14 = df['High'].rolling(window=14).max()
low14 = df['Low'].rolling(window=14).min()
df['WilliamsR'] = (high14 - df['Close']) / (high14 - low14) * -100

# KD indicator
low9 = df['Low'].rolling(window=9).min()
high9 = df['High'].rolling(window=9).max()
rsv = (df['Close'] - low9) / (high9 - low9) * 100
df['K'] = rsv.ewm(com=2).mean()
df['D'] = df['K'].ewm(com=2).mean()

# OBV indicator
df['OBV'] = (df['Close'].diff() > 0).astype(int) * df['Volume']
df['OBV'] = df['OBV'].cumsum()

# CCI
tp = (df['High'] + df['Low'] + df['Close']) / 3
ma_tp = tp.rolling(window=20).mean()
md = (tp - ma_tp).abs().rolling(window=20).mean()
df['CCI'] = (tp - ma_tp) / (0.015 * md)

# ADL (Accumulation/Distribution Line)
clv = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
clv = clv.fillna(0)
df['ADL'] = (clv * df['Volume']).cumsum()

# Ensure the last day's indicators are not NaN, dropna only for necessary columns
required_cols = ['MA20', 'STD20', 'CCI', 'BOLL_UP', 'BOLL_DOWN']
df = df.dropna(subset=required_cols)

if df.empty:
    raise ValueError("❌ Cannot calculate technical indicators because data is insufficient or all NaN")

rsi = rsi.loc[df.index[-1]]
macd = macd_line.loc[df.index[-1]]
ma_gap = ((df['Close'].iloc[-1] - df['MA20'].iloc[-1]) / df['MA20'].iloc[-1]) * 100
boll_up = df['BOLL_UP'].iloc[-1]
boll_down = df['BOLL_DOWN'].iloc[-1]
williams_r = df['WilliamsR'].iloc[-1]
k = df['K'].iloc[-1]
d = df['D'].iloc[-1]
obv = df['OBV'].iloc[-1]
cci = df['CCI'].iloc[-1]
adl = df['ADL'].iloc[-1]

# Print results
print("\n📊 Technical analysis indicators:")
print(f"Average price (Close): {avg_price:.2f}")
print(f"RSI: {rsi:.2f}")
print(f"MACD: {macd:.2f}")
print(f"20MA deviation rate: {ma_gap:.2f}%")
print(f"Bollinger Bands: Upper={boll_up:.2f}, Lower={boll_down:.2f}")
print(f"Williams %R: {williams_r:.2f}")
print(f"K: {k:.2f}, D: {d:.2f}")
print(f"OBV: {obv:.2f}")
print(f"CCI: {cci:.2f}")
print(f"ADL: {adl:.2f}")
