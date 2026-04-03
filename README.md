# Stock Price & Revenue Dashboard (TSLA + GME)

Interactive dashboards that compare **stock price** vs **quarterly revenue** for **Tesla (TSLA)** and **GameStop (GME)**.

This is a cleaned, production-style script version of the Coursera / IBM Skills Network lab **“Extracting and Visualizing Stock Data”**:
- **Prices** come from Yahoo Finance via [`yfinance`](https://github.com/ranaroussi/yfinance)
- **Revenue tables** are scraped from the official IBM-hosted lab HTML using [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/)
- **Charts** are built with [`plotly`](https://plotly.com/python/)

## What it does

- **Downloads** maximum available daily price history for a ticker
- **Scrapes & cleans** quarterly revenue (removes commas and `$`)
- **Plots** a two-panel dashboard: *Historical Share Price* + *Historical Revenue*
- **Outputs** interactive charts (browser) or standalone `.html` files

## Quickstart

```bash
pip install -r requirements.txt
python stock_data_viz.py --no-show --output-dir ./output
```

This will generate:
- `./output/tesla_dashboard.html`
- `./output/gme_dashboard.html`

## Requirements

- Python **3.10+** (3.11+ recommended)
- Internet access (Yahoo Finance + IBM-hosted lab pages)

## Installation (recommended: virtual environment)

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run both tickers (opens charts in your browser):

```bash
python stock_data_viz.py
```

Run only one ticker:

```bash
python stock_data_viz.py --tickers TSLA
python stock_data_viz.py --tickers GME
```

Save HTML files instead of opening a browser:

```bash
python stock_data_viz.py --no-show
```

Save HTML files to a specific folder:

```bash
python stock_data_viz.py --no-show --output-dir ./output
```

See all CLI options:

```bash
python stock_data_viz.py -h
```

## Notes

- **Notebook typo fixed**: the original notebook used `2021--06-14` (double hyphen) in the stock cutoff filter; this script uses `2021-06-14`.
- **Timezone-safe filtering**: Yahoo Finance data can be timezone-aware; the script normalizes timestamps so the cutoff filters work reliably.

## Project structure

| Path | Description |
|------|-------------|
| `stock_data_viz.py` | Main CLI script (fetch, scrape, clean, plot). |
| `requirements.txt` | Python dependencies. |
| `readme.md` | Project documentation (this file). |

## Data sources

- **Prices**: Yahoo Finance via `yfinance`
- **Revenue**: IBM Skills Network lab HTML pages (URLs are constants in `stock_data_viz.py`)

## Disclaimer

This repository is for educational use. Stock data and scraped content are subject to their providers’ terms.
