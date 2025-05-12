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
