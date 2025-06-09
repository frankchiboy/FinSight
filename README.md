# 📈 FinSight – AI-Powered Technical Analysis MVP (LLaMA via Hugging Face)

## 🚀 Overview

FinSight is a tool that calculates technical indicators for stocks and generates concise investment summaries using a LLaMA model hosted on Hugging Face. It supports both command-line and web-based interfaces.

## 📦 Features

- Supports both CLI and Streamlit UI interfaces
- Calculates 10+ technical indicators:
  - RSI, MACD, Bollinger Bands, OBV, CCI, KD, Williams %R, MA deviation, ADL
- Uses LLaMA to generate 2–3 line investment insights
- Saves reports to `.txt` files
- Uses the Hugging Face Inference API for text generation

## 🧰 Tech Stack

- Python 3.9+
- yfinance, pandas, numpy
- Streamlit (for UI)
- Hugging Face Inference API (LLaMA model)

## 🧪 Usage

### CLI mode

```bash
python3 run_report.py --ticker AAPL --start 2024-05-01 --end 2024-05-20
```

- Downloads stock data via yfinance
- Computes technical indicators
- Generates prompt for LLaMA and appends LLM response
- Saves `.txt` report (e.g., `report_aapl.txt`)

### UI mode (Streamlit)

```bash
streamlit run run_report.py
```

> Requires: `pip install streamlit`

- Opens a web-based interface at `http://localhost:8501`
- Allows manual ticker/date input and displays results
- Report is viewable and downloadable

## 📁 Files

- `run_report.py` – Entry point for CLI and UI
- `analysis_engine.py` – Core logic for indicator calculation
- `report_*.txt` – Output reports with LLM analysis
- `README.md`, `ROADMAP.md`, `release_notes.md` – Documentation

## 🧠 Notes

- Set the `HUGGING_FACE_HUB_TOKEN` environment variable to access the Hugging Face API
- CLI and UI share the same analysis backend

## 👤 Author

[Frank Hsu](https://github.com/frankchiboy)
