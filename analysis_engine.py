import yfinance as yf
import pandas as pd

# 1. 輸入參數
ticker = "2330.TW"
start_date = "2024-02-01"
end_date = "2024-04-30"

# 2. 抓取歷史資料
df = yf.download(ticker, start=start_date, end=end_date)

# 若欄位有 MultiIndex，則擷取第一層欄位名稱
if isinstance(df.columns, pd.MultiIndex):
    df.columns = df.columns.get_level_values(0)

# 確認資料成功抓取
print("✅ 股價資料前幾筆：")
print(df.head())

# 3. 計算技術指標
df['MA20'] = df['Close'].rolling(window=20).mean()

# 計算 RSI（14日）
delta = df['Close'].diff()
gain = delta.where(delta > 0, 0)
loss = -delta.where(delta < 0, 0)
avg_gain = gain.rolling(window=14).mean()
avg_loss = loss.rolling(window=14).mean()
rs = avg_gain / avg_loss
rsi = 100 - (100 / (1 + rs))

# 計算 MACD（12, 26, 9 EMA）
ema12 = df['Close'].ewm(span=12, adjust=False).mean()
ema26 = df['Close'].ewm(span=26, adjust=False).mean()
macd_line = ema12 - ema26
signal_line = macd_line.ewm(span=9, adjust=False).mean()

avg_price = df['Close'].mean()

# 新增多項技術指標

# 移動平均類
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

# 波動率指標
df['STD20'] = df['Close'].rolling(window=20).std()
df['STD50'] = df['Close'].rolling(window=50).std()
df['BOLL_UP'] = df['MA20'] + 2 * df['STD20']
df['BOLL_DOWN'] = df['MA20'] - 2 * df['STD20']

# 價格區間指標
df['High-Low'] = df['High'] - df['Low']
df['Close-Open'] = df['Close'] - df['Open']

# 動量類
df['Momentum10'] = df['Close'] - df['Close'].shift(10)
df['ROC10'] = df['Close'].pct_change(periods=10) * 100

# 威廉指標（Williams %R）
high14 = df['High'].rolling(window=14).max()
low14 = df['Low'].rolling(window=14).min()
df['WilliamsR'] = (high14 - df['Close']) / (high14 - low14) * -100

# KD指標
low9 = df['Low'].rolling(window=9).min()
high9 = df['High'].rolling(window=9).max()
rsv = (df['Close'] - low9) / (high9 - low9) * 100
df['K'] = rsv.ewm(com=2).mean()
df['D'] = df['K'].ewm(com=2).mean()

# OBV 指標
df['OBV'] = (df['Close'].diff() > 0).astype(int) * df['Volume']
df['OBV'] = df['OBV'].cumsum()

# CCI
tp = (df['High'] + df['Low'] + df['Close']) / 3
ma_tp = tp.rolling(window=20).mean()
md = (tp - ma_tp).abs().rolling(window=20).mean()
df['CCI'] = (tp - ma_tp) / (0.015 * md)

# ADL（累積/分布線）
clv = ((df['Close'] - df['Low']) - (df['High'] - df['Close'])) / (df['High'] - df['Low'])
clv = clv.fillna(0)
df['ADL'] = (clv * df['Volume']).cumsum()

# 確保最後一日指標非NaN，先 dropna 只針對必要欄位
required_cols = ['MA20', 'STD20', 'CCI', 'BOLL_UP', 'BOLL_DOWN']
df = df.dropna(subset=required_cols)

if df.empty:
    raise ValueError("❌ 無法計算技術指標，因為資料量太少或全部為 NaN")

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

# 印出結果
print("\n📊 技術分析指標：")
print(f"平均價格（收盤）：{avg_price:.2f}")
print(f"RSI：{rsi:.2f}")
print(f"MACD：{macd:.2f}")
print(f"20MA 乖離率：{ma_gap:.2f}%")
print(f"Bollinger Bands：上={boll_up:.2f}, 下={boll_down:.2f}")
print(f"Williams %R：{williams_r:.2f}")
print(f"K：{k:.2f}, D：{d:.2f}")
print(f"OBV：{obv:.2f}")
print(f"CCI：{cci:.2f}")
print(f"ADL：{adl:.2f}")
