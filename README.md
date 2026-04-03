# 📊 Stock Price & Revenue Dashboard (TSLA + GME)

<div align="center">

![GitHub Stars](https://img.shields.io/github/stars/NITHISH74/EquityRevenue-Dashboard?style=for-the-badge&color=blue)
![GitHub Forks](https://img.shields.io/github/forks/NITHISH74/EquityRevenue-Dashboard?style=for-the-badge&color=green)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)

**Interactive dashboards comparing stock price vs quarterly revenue for Tesla (TSLA) and GameStop (GME)**

[View Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage)

</div>

---

## 🎯 Overview

This repository contains a **production-ready dashboard application** that visualizes and compares **stock price trends** against **quarterly revenue data** for two major stocks: **Tesla (TSLA)** and **GameStop (GME)**.

Built as an enhanced version of the Coursera/IBM Skills Network lab **"Extracting and Visualizing Stock Data"**, this project demonstrates:
- 📈 Real-time data fetching from Yahoo Finance
- 🔍 Web scraping with BeautifulSoup
- 📊 Interactive visualization with Plotly
- 🎨 Professional dashboard generation

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📥 **Auto Download** | Fetches maximum available daily price history for any ticker |
| 🧹 **Data Cleaning** | Automatically scrapes & cleans quarterly revenue data (removes currency symbols) |
| 📈 **Dual Charts** | Two-panel interactive dashboards: Historical Share Price + Historical Revenue |
| 🌐 **Multi-Output** | Display charts in browser OR generate standalone `.html` files |
| ⚙️ **CLI Control** | Flexible command-line interface for customization |
| 🔄 **Timezone Safe** | Intelligent timestamp normalization for reliable filtering |

---

## 🚀 Quick Start

Get up and running in 30 seconds:

```bash
pip install -r requirements.txt
python stock_data_viz.py --no-show --output-dir ./output
```

This generates:
- 📄 `./output/tesla_dashboard.html` - Interactive Tesla dashboard
- 📄 `./output/gme_dashboard.html` - Interactive GameStop dashboard

---

## 📋 Requirements

- **Python** 3.10+ (3.11+ recommended)
- **Internet access** for Yahoo Finance & IBM-hosted lab pages
- See `requirements.txt` for Python dependencies

---

## 🔧 Installation

### Step 1: Create Virtual Environment

```bash
python -m venv .venv
```

### Step 2: Activate Environment

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

✅ You're ready to go!

---

## 💻 Usage

### Run Both Tickers
Opens interactive charts in your default browser:
```bash
python stock_data_viz.py
```

### Run Specific Ticker Only
```bash
# Tesla only
python stock_data_viz.py --tickers TSLA

# GameStop only
python stock_data_viz.py --tickers GME
```

### Save as HTML Files
```bash
python stock_data_viz.py --no-show
```

### Custom Output Directory
```bash
python stock_data_viz.py --no-show --output-dir ./output
```

### View All Options
```bash
python stock_data_viz.py -h
```

---

## 📁 Project Structure

```
EquityRevenue-Dashboard/
├── stock_data_viz.py          # Main CLI script (fetch, scrape, clean, plot)
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

---

## 📊 Data Sources

| Data | Source | Method |
|------|--------|--------|
| **Stock Prices** | Yahoo Finance | `yfinance` API |
| **Revenue Data** | IBM Skills Network | Web scraping with `BeautifulSoup` |

---

## 🛠️ Technology Stack

<div align="center">

![yfinance](https://img.shields.io/badge/yfinance-Real%20Time%20Data-brightgreen?style=flat-square)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-Web%20Scraping-blue?style=flat-square)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-purple?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.10+-orange?style=flat-square)

</div>

---

## 📝 Important Notes

⚠️ **Notebook Typo Fixed** - The original notebook used `2021--06-14` (double hyphen); this script correctly uses `2021-06-14`

🔒 **Timezone Safe** - Yahoo Finance data can be timezone-aware; this script normalizes timestamps for reliable filtering

---

## ⚖️ Disclaimer

This repository is for **educational purposes only**. Stock data and scraped content are subject to their respective providers' terms and conditions. Use responsibly.

---

## 📬 Support & Contribution

Found a bug? Have a suggestion? Feel free to:
- 🐛 Open an issue
- 🔀 Submit a pull request
- 💬 Start a discussion

---

<div align="center">

**Made with ❤️ by [NITHISH74](https://github.com/NITHISH74)**

![Views](https://komarev.com/ghpvc/?username=NITHISH74&repo=EquityRevenue-Dashboard&color=blue)

</div>
