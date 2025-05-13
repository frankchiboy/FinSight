# 📈 FinSight – AI-Powered Technical Analysis MVP (LLaMA + CLI)

## 🚀 Overview
FinSight is a local-first MVP tool that computes technical indicators for any stock and produces concise investment summaries using a self-hosted LLaMA model.

## 📦 Features
- Parses historical data using yFinance
- Calculates 12 technical indicators, including RSI, MACD, MA Gap, Bollinger Bands, KD, OBV, CCI, ADL, and Williams %R
- Converts metrics into natural language prompts
- CLI-only interface
- Saves results into `.txt` reports

## 🧰 Tech Stack
- Python 3.9+
- yFinance, Pandas
- Ollama with LLaMA3/LLaMA4
- GitHub CLI (release automation)

> 💡 You must install [Ollama](https://ollama.com/) locally and ensure the `llama3` or `llama4` model is downloaded (e.g. `ollama run llama3`) before running.

## 🧪 Usage

### CLI mode
```bash
python3 run_report.py
```

- Generates prompt
- Calls LLaMA via API
- Saves report to `report_2330TW.txt`

> 🧪 In this MVP version, the stock symbol is hardcoded for demonstration (e.g., `2330.TW`). Future versions will support dynamic symbol extraction from user input.

## 📁 Files
- `run_report.py`: CLI orchestrator
- `analysis_engine.py`: computes indicators
- `report_2330TW.txt`: sample output

## 🔒 License
MIT

## 👤 Author
[Frank Hsu](https://github.com/frankchiboy)

## 📟 Demo: Finsight v0.0.1 Terminal Log

Below is a sample terminal session showing how Finsight generates a technical analysis report and uses a language model to provide insights.

```
$ python3 run_report.py

✅ Stock price data preview:
Price            Close        High         Low        Open     Volume
Date                                                                 
2024-02-01  619.91      619.91      611.03      616.95   44946369
2024-02-02  626.82      626.82      619.91      624.85   26334815
2024-02-05  637.68      638.67      629.78      636.69   44017740
2024-02-15  688.02      699.87      684.07      699.87   112945296
2024-02-16  674.20      690.00      674.20      688.02   44232811

📊 Technical analysis indicators:
Average price (Close): 743.11  
RSI: 44.17  
MACD: 5.11  
20MA deviation rate: 0.98%  
Bollinger Bands: Upper=826.94, Lower=734.53  
Williams %R: -36.05  
K: 54.34, D: 43.10  
OBV: 1301636658.00  
CCI: 16.59  
ADL: -63983909.57

📨 Prompt sent to LLaMA model:

You are a senior technical analyst. Based on the following technical data, please provide a concise 2–3 line investment insight...

📈 LLaMA model response:

The stock's RSI (44.17) and KD (54.34, 43.10) suggest a neutral to slightly bullish trend. The MACD (5.11) and CCI (16.59) indicate a potential for upward movement. However, the Bollinger Bands and 20-day MA Deviation (0.98%) imply a relatively stable and narrow trading range, suggesting a cautious approach.

✅ Report saved as: report_2330TW.txt
```