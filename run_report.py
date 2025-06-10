import yfinance as yf
import pandas as pd
import numpy as np
import logging
import datetime
import os
import requests


os.environ["OPENROUTER_API_KEY"] = "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"
# Configure logging at INFO level for terminal output
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def get_technical_indicators(ticker, start_date, end_date):
    ticker = ticker.strip().upper()
    from datetime import datetime, timedelta
    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    today = datetime.today()
    # 若 end_dt 在今天之後，調整為今天
    if end_dt > today:
        end_dt = today
    if end_dt <= start_dt:
        end_dt = start_dt + timedelta(days=1)
    start_date = start_dt.strftime("%Y-%m-%d")
    end_date = end_dt.strftime("%Y-%m-%d")
    from datetime import timedelta
    end_param = (end_dt + timedelta(days=1)).strftime("%Y-%m-%d")

    # 檢查開始日是否在未來，若是則直接回傳空值
    if start_dt >= today:
        logging.warning(f"⚠️ 輸入開始日 {start_date} 在未來，無法取得資料")
        return {key: np.nan for key in [
            "avg_price", "rsi", "macd", "ma_gap", "boll_up", "boll_down",
            "williams_r", "k", "d", "obv", "cci", "adl"
        ]}
    df = yf.download(ticker, start=start_date, end=end_param)
    # If columns are a MultiIndex like ('Close','AAPL'), flatten to first level
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    logging.info(f"Downloaded {len(df)} rows for {ticker} from {start_date} to {end_date}, columns: {df.columns.tolist()}")
    # Fallback to adjusted close if raw close missing
    if 'Close' not in df.columns and 'Adj Close' in df.columns:
        df['Close'] = df['Adj Close']
    # Ensure volume exists, else set volume to zeros
    if 'Volume' not in df.columns:
        df['Volume'] = 0
    if df.empty or 'Close' not in df.columns:
        logging.warning(f"⚠️ 無法下載資料，ticker: {ticker}, 日期：{start_date} ~ {end_date}")
        # continue to downstream to produce NaNs

    # Detailed logging of DataFrame after fallback logic
    logging.info(f"DataFrame shape: {df.shape}, columns: {df.columns.tolist()}")
    logging.info(f"Close head: {df['Close'].head().tolist()}")
    logging.info(f"Volume head: {df['Volume'].head().tolist()}")

    close = df["Close"]
    volume = df["Volume"]

    avg_price = close.mean()

    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    try:
        rsi = (100 - (100 / (1 + rs))).iloc[-1]
    except Exception:
        rsi = np.nan

    exp1 = close.ewm(span=12, adjust=False).mean()
    exp2 = close.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    macd = macd.iloc[-1] if not macd.empty else np.nan

    ma20 = close.rolling(window=20).mean()
    ma_gap_series = (close - ma20) / ma20 * 100
    ma_gap = ma_gap_series.iloc[-1] if not ma_gap_series.empty else np.nan

    std = close.rolling(window=20).std()
    boll_up_series = ma20 + 2 * std
    boll_down_series = ma20 - 2 * std
    boll_up = boll_up_series.iloc[-1] if not boll_up_series.empty else np.nan
    boll_down = boll_down_series.iloc[-1] if not boll_down_series.empty else np.nan

    high14 = df['High'].rolling(14).max()
    low14 = df['Low'].rolling(14).min()
    williams_r_series = ((high14 - close) / (high14 - low14) * -100)
    williams_r = williams_r_series.iloc[-1] if not williams_r_series.empty else np.nan

    low_min = df['Low'].rolling(window=9).min()
    high_max = df['High'].rolling(window=9).max()
    rsv = (close - low_min) / (high_max - low_min) * 100
    k_series = rsv.ewm(com=2).mean()
    k = k_series.iloc[-1] if not k_series.empty else np.nan
    d_series = k_series.ewm(com=2).mean()
    d = d_series.iloc[-1] if not d_series.empty else np.nan

    obv_series = (np.sign(close.diff()) * volume).fillna(0).cumsum()
    obv = obv_series.iloc[-1] if not obv_series.empty else np.nan

    tp = (df['High'] + df['Low'] + close) / 3
    cci_series = (close - tp.rolling(20).mean()) / (0.015 * tp.rolling(20).std())
    cci = cci_series.iloc[-1] if not cci_series.empty else np.nan

    mfm = ((close - df['Low']) - (df['High'] - close)) / (df['High'] - df['Low'])
    mfv = mfm * volume
    adl_series = mfv.cumsum()
    adl = adl_series.iloc[-1] if not adl_series.empty else np.nan

    logging.info(f"avg_price: {avg_price}")
    logging.info(f"rsi: {rsi}")
    logging.info(f"macd: {macd}")
    logging.info(f"ma_gap: {ma_gap}")
    logging.info(f"boll_up: {boll_up}, boll_down: {boll_down}")
    logging.info(f"williams_r: {williams_r}")
    logging.info(f"k: {k}, d: {d}")
    logging.info(f"obv: {obv}")
    logging.info(f"cci: {cci}")
    logging.info(f"adl: {adl}")

    return {
        "avg_price": avg_price,
        "rsi": rsi,
        "macd": macd,
        "ma_gap": ma_gap,
        "boll_up": boll_up,
        "boll_down": boll_down,
        "williams_r": williams_r,
        "k": k,
        "d": d,
        "obv": obv,
        "cci": cci,
        "adl": adl,
    }

def query_llama(prompt, model="meta-llama/llama-4-scout:free"):
    """Query the LLaMA model via OpenRouter and return the generated text."""
    token = os.environ.get("OPENROUTER_API_KEY")
    if not token:
        error_msg = "OPENROUTER_API_KEY environment variable not set"
        logging.error(error_msg)
        print(error_msg)  # 在終端機顯示錯誤
        return error_msg

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/frankchiboy",  # required by OpenRouter
        "X-Title": "FinSight",
    }

    api_url = "https://openrouter.ai/api/v1/chat/completions"
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        logging.info("Sending request to OpenRouter API...")
        print("Prompt:", prompt)  # 打印提示詞
        
        res = requests.post(api_url, headers=headers, json=payload, timeout=60)
        print(f"Status Code: {res.status_code}")  # 打印狀態碼
        
        if res.status_code != 200:
            error_msg = f"API Error: Status {res.status_code}, Response: {res.text}"
            print(error_msg)  # 打印錯誤訊息
            return error_msg

        data = res.json()
        print("\nAPI Response:", data)  # 打印完整回應
        
        if not data.get('choices'):
            error_msg = "No choices in response"
            print(error_msg)
            return error_msg
            
        content = data['choices'][0].get('message', {}).get('content', '')
        print("\nGenerated content:", content)  # 打印生成的內容
        
        if not content:
            error_msg = "Empty content in response"
            print(error_msg)
            return error_msg
            
        return content
        
    except Exception as e:
        error_msg = f"Error querying API: {str(e)}"
        print(error_msg)  # 打印例外錯誤
        return error_msg

if __name__ == "__main__":
    import streamlit as st
    import locale
    from datetime import timedelta
    import datetime
    from run_report import query_llama

    st.set_page_config(page_title="📈 FinSight", layout="centered")
    lang = st.sidebar.selectbox("🌐 Language 語言", ["English", "中文"])

    if lang == "中文":
        st.title("📈 FinSight 技術分析報告生成器")
        st.markdown("輸入股票代號與日期區間，系統將產生技術指標與投資建議")
        ticker_label = "輸入股票代號（例如: AAPL）"
        date_start_label = "開始日期"
        date_end_label = "結束日期"
        button_label = "產生分析報告"
        summary_label = "📊 技術指標摘要"
    else:
        st.title("📈 FinSight Technical Analysis Report Generator")
        st.markdown("Enter a stock ticker and date range to generate technical indicators and investment suggestions.")
        ticker_label = "Enter stock ticker (e.g., AAPL)"
        date_start_label = "Start Date"
        date_end_label = "End Date"
        button_label = "Generate Report"
        summary_label = "📊 Technical Indicator Summary"

    ticker = st.text_input(ticker_label, value="aapl")

    col1, col2 = st.columns(2)
    today = datetime.date.today()
    default_end_date = today - timedelta(days=1)
    default_start_date = today - timedelta(days=365)
    start_date_input = col1.date_input(date_start_label, value=default_start_date)
    end_date_input   = col2.date_input(date_end_label, value=default_end_date)
    start_date = start_date_input.strftime("%Y-%m-%d")
    end_date   = end_date_input.strftime("%Y-%m-%d")

    if st.button(button_label) and ticker:

        # Debug: show raw data
        raw_df = yf.download(ticker, start=start_date, end=end_date)
        st.subheader("🔍 Raw Data Preview")
        st.dataframe(raw_df)

        indicators = get_technical_indicators(ticker, start_date, end_date)

        # Label mapping based on language; move here after indicators is defined
        if lang == "中文":
            label_map = {
                "avg_price": "平均收盤價",
                "rsi": "相對強弱指數 RSI",
                "macd": "MACD",
                "ma_gap": "20 日均線乖離率",
                "boll_up": "布林通道上軌",
                "boll_down": "布林通道下軌",
                "williams_r": "威廉指標 %R",
                "k": "KD 指標 K",
                "d": "KD 指標 D",
                "obv": "能量潮指標 OBV",
                "cci": "商品通道指標 CCI",
                "adl": "累積/派發線 ADL"
            }
        else:
            label_map = {key: key for key in indicators.keys()}

        st.subheader(summary_label)
        for key, value in indicators.items():
            st.write(f"**{label_map[key]}**: {value:.2f}" if isinstance(value, (float, int)) and not pd.isna(value) else f"**{label_map[key]}**: 無法計算")

        # Generate AI report
        if lang == "中文":
            prompt = "請以繁體中文回答。\n" + f"你是一位資深技術分析師，根據以下指標提供 2~3 行投資建議：\n" + "\n".join([f"- {k}: {v:.2f}" for k,v in indicators.items()])
        else:
            prompt = "You are a senior technical analyst. Based on the following indicators, please provide a concise 2–3 line investment insight:\n" + "\n".join([f"- {k}: {v:.2f}" for k,v in indicators.items()])
        result = query_llama(prompt)
        st.markdown("### " + ("📊 投資建議" if lang=="中文" else "📊 Investment Suggestion"))
        st.markdown(result)
