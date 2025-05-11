from analysis_engine import (
    ticker, start_date, end_date,
    avg_price, rsi, macd, ma_gap,
    boll_up, boll_down, williams_r, k, d, obv, cci, adl
)
import requests
import math

def safe_format(value, suffix=""):
    return f"{value:.2f}{suffix}" if not math.isnan(value) else "無法計算"

# === Step 4: 組合 Prompt ===
prompt = f"""
你是一位資深技術分析師，請根據以下資料撰寫一段 2～3 行的中文技術分析建議：

股票代號：{ticker}
日期區間：{start_date} ~ {end_date}
技術指標摘要：
- 平均收盤價：{safe_format(avg_price)}
- RSI：{safe_format(rsi)}
- MACD：{safe_format(macd)}
- 20 日均線乖離率：{safe_format(ma_gap, '%')}
- 布林通道：上={safe_format(boll_up)} / 下={safe_format(boll_down)}
- Williams %R：{safe_format(williams_r)}
- KD值：K={safe_format(k)}, D={safe_format(d)}
- OBV：{safe_format(obv)}
- CCI：{safe_format(cci)}
- ADL：{safe_format(adl)}

請專業分析此股目前趨勢。
"""

print("\n📨 傳送給 LLaMA 模型的 Prompt：\n")
print(prompt)

# === Step 5: 呼叫 LLaMA 模型（透過 Ollama）===
def query_llama(prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3.3",
        "prompt": prompt,
        "stream": False
    }

    res = requests.post(url, json=data)
    res_json = res.json()
    print("🔍 LLaMA 回傳內容：", res_json)

    if "error" in res_json:
        raise RuntimeError(f"❌ LLaMA 模型錯誤：{res_json['error']}")
    if "response" in res_json:
        return res_json["response"]

    raise KeyError(f"❌ 回傳結果缺少 'response' 欄位：{res_json}")

# 呼叫 AI 模型並顯示結果
response = query_llama(prompt)

print("\n📈 LLaMA 模型回應：\n")
print(response)

# === Step 6: 儲存為分析報告 ===
filename = f"report_{ticker.replace('.', '')}.txt"
with open(filename, "w", encoding="utf-8") as f:
    f.write("📌 股票技術分析報告\n\n")
    f.write(prompt)
    f.write("\n\n📊 AI 回覆建議：\n")
    f.write(response)

print(f"\n✅ 報告已儲存為：{filename}")
