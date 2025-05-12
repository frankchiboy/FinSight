# 📈 FinSight v0.0.1 – AI-Powered Technical Analysis MVP (LLaMA + CLI)

This is the first MVP release of **FinSight**, a local-first technical analysis engine that combines financial indicators with natural-language insights via LLaMA.

🔍 Overview:
FinSight computes commonly-used technical indicators (RSI, MACD, MA, OBV, etc.) for any stock ticker, and generates investment suggestions using a locally hosted LLaMA model. The entire flow runs offline with no API keys or cloud dependencies.

In this MVP version, the stock ticker symbol is hardcoded (e.g., `2330.TW`) for demonstration purposes. Future versions will support dynamic symbol detection based on user input.

✨ Features:
- Parses historical stock data via yFinance
- Calculates 12 technical indicators, including RSI, MACD, MA Gap, Bollinger Bands, KD, OBV, CCI, ADL, and Williams %R
- Formats into natural language prompts
- Calls Ollama (`localhost:11434`) for LLaMA inference
- Saves the result into `.txt` reports
- CLI-based only (no proxy API, no tunneling)

🔧 Tech Stack:
- Python 3.9+
- yFinance, Pandas
- Ollama + LLaMA3 / LLaMA4 (local inference)
- GitHub CLI automation

📂 Included:
- `run_report.py` – command-line script to run end-to-end analysis
- `analysis_engine.py` – computes indicators and exports variables
- `report_2330TW.txt` – sample LLaMA-generated investment suggestion

🚧 Next Steps:
- Web frontend (e.g., Streamlit or Svelte)
- Backtest + multi-ticker comparison

🛠 Version: `v0.0.1`  
🔒 License: MIT  
👤 Author: [Frank Hsu](https://github.com/frankchiboy)
