import yfinance as yf
import pandas as pd
import ta  # technical analysis library

# 1. 輸入參數
ticker = "2330.TW"
start_date = "2024-04-01"
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
rsi = ta.momentum.RSIIndicator(close=df['Close'].squeeze(), window=14).rsi().iloc[-1]
macd = ta.trend.MACD(close=df['Close'].squeeze()).macd().iloc[-1]
avg_price = df['Close'].mean()
ma_gap = ((df['Close'].iloc[-1] - df['MA20'].iloc[-1]) / df['MA20'].iloc[-1]) * 100

# 印出結果
print("\n📊 技術分析指標：")
print(f"平均價格（收盤）：{avg_price:.2f}")
print(f"RSI：{rsi:.2f}")
print(f"MACD：{macd:.2f}")
print(f"20MA 乖離率：{ma_gap:.2f}%")
