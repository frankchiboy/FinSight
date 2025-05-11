from analysis_engine import (
    ticker, start_date, end_date,
    avg_price, rsi, macd, ma_gap,
    boll_up, boll_down, williams_r, k, d, obv, cci, adl
)
import requests
import math

def safe_format(value, suffix=""):
    return f"{value:.2f}{suffix}" if not math.isnan(value) else "無法計算"

# === Step 4: Compose Prompt ===
prompt = f"""
You are a senior technical analyst. Based on the following technical data, please provide a concise 2–3 line investment insight:

Stock Ticker: {ticker}
Date Range: {start_date} ~ {end_date}
Technical Indicator Summary:
- Average Closing Price: {safe_format(avg_price)}
- RSI: {safe_format(rsi)}
- MACD: {safe_format(macd)}
- 20-day MA Deviation: {safe_format(ma_gap, '%')}
- Bollinger Bands: Upper={safe_format(boll_up)} / Lower={safe_format(boll_down)}
- Williams %R: {safe_format(williams_r)}
- KD: K={safe_format(k)}, D={safe_format(d)}
- OBV: {safe_format(obv)}
- CCI: {safe_format(cci)}
- ADL: {safe_format(adl)}

Please analyze the current trend of this stock.
"""

print("\n📨 Prompt sent to LLaMA model:\n")
print(prompt)

# === Step 5: Call LLaMA model (via Ollama) ===
def query_llama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.3",
        "prompt": prompt,
        "stream": False
    }

    res = requests.post(url, json=data)
    res_json = res.json()
    print("🔍 LLaMA response content:", res_json)

    if "error" in res_json:
        raise RuntimeError(f"❌ LLaMA model error: {res_json['error']}")
    if "response" in res_json:
        return res_json["response"]

    raise KeyError(f"❌ Missing 'response' field in result: {res_json}")

# Call AI model and display result
response = query_llama(prompt)

print("\n📈 LLaMA model response:\n")
print(response)

# === Step 6: Save as analysis report ===
filename = f"report_{ticker.replace('.', '')}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write("📌 Stock Technical Analysis Report\n\n")
    f.write(prompt)
    f.write("\n\n📊 AI Response Suggestion:\n")
    f.write(response)

print(f"\n✅ Report saved as: {filename}")
