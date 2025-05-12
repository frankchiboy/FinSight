

# 🛣 FinSight Development Roadmap

This document outlines the planned development directions and milestones of the FinSight project.

## ✅ Completed (v0.0.1)
- CLI-based report generator
- LLaMA integration via local Ollama instance
- Generates investment suggestions from 12 technical indicators
- No internet connection or proxy required

## 🟡 In Development
### 🧠 Intent Detection
- Enable system to understand natural-language questions
- Automatically infer:
  - Related financial instrument codes (e.g., 2330.TW)
  - Time ranges (e.g., past month, 2023 Q1)
  - Resolution granularity (daily, weekly, etc.)

## 🔜 Next Features
### 📊 Multi-Ticker Analysis
- Load and analyze multiple stock symbols together
- Compare indicators and LLM-generated summaries side-by-side

### 📈 Backtesting
- Simulate performance using past data
- Integrate with rule-based indicator logic

### 🖼 Report Output
- Export to CSV, PDF
- Include charts with annotated indicators

### 🖥 (Optional) Web Dashboard
- Build basic frontend (e.g., Streamlit) for interactive usage