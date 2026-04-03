#!/usr/bin/env python3
"""
Extracting and Visualizing Stock Data
=====================================

Fetches historical stock prices via yfinance, scrapes quarterly revenue from
IBM Skills Network lab HTML pages, and produces interactive Plotly dashboards
comparing share price and revenue (Tesla and/or GameStop workflows from the
original Coursera lab).

Usage:
    python stock_data_viz.py
    python stock_data_viz.py --tickers TSLA GME
    python stock_data_viz.py --tickers TSLA --no-show  # save HTML instead
"""

from __future__ import annotations

import argparse
import logging
import os
import warnings

import pandas as pd
import plotly.graph_objects as go
import requests
import yfinance as yf
from bs4 import BeautifulSoup
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------
# Configuration (IBM Skills Network lab URLs — course assignment sources)
# -----------------------------------------------------------------------------

TESLA_REVENUE_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
)
GME_REVENUE_URL = (
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/"
    "IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
)

DEFAULT_STOCK_END = "2021-06-14"
DEFAULT_REVENUE_END = "2021-04-30"
GME_EXTRA_FILTER_END = "2021-06-30"

warnings.filterwarnings("ignore", category=FutureWarning)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
)
logger = logging.getLogger(__name__)


def _to_naive_datetime(series: pd.Series) -> pd.Series:
    """Convert to datetime64[ns], dropping timezone for consistent comparisons."""
    out = pd.to_datetime(series)
    if getattr(out.dt, "tz", None) is not None:
        out = out.dt.tz_convert("UTC").dt.tz_localize(None)
    return out


def fetch_stock_history(ticker: str) -> pd.DataFrame:
    """
    Download maximum available daily history for ``ticker`` and return a
    DataFrame with a ``Date`` column (index reset).
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period="max")
    if hist.empty:
        raise ValueError(f"No price history returned for {ticker!r}")
    out = hist.reset_index()
    # yfinance may name the column Date or Datetime depending on version
    date_col = "Date" if "Date" in out.columns else out.columns[0]
    if date_col != "Date":
        out = out.rename(columns={date_col: "Date"})
    return out


def _table_rows_for_title(soup: BeautifulSoup, title_substring: str) -> list[list[str]]:
    """Parse HTML tables and return rows ``[date, revenue]`` for the matching table."""
    for table in soup.find_all("table"):
        if title_substring not in str(table):
            continue
        tbody = table.find("tbody")
        if tbody is None:
            continue
        rows_out: list[list[str]] = []
        for row in tbody.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) >= 2:
                rows_out.append([cols[0].get_text(strip=True), cols[1].get_text(strip=True)])
        return rows_out
    raise ValueError(f"No table containing {title_substring!r} was found.")


def scrape_quarterly_revenue(url: str, table_title: str) -> pd.DataFrame:
    """
    Fetch HTML from ``url`` and build a DataFrame with ``Date`` and ``Revenue``
    columns from the quarterly revenue table identified by ``table_title``.
    """
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.content, "html.parser")
    rows = _table_rows_for_title(soup, table_title)
    if not rows:
        return pd.DataFrame(columns=["Date", "Revenue"])
    df = pd.DataFrame(rows, columns=["Date", "Revenue"])
    df["Revenue"] = df["Revenue"].str.replace(r",|\$", "", regex=True)
    df = df.dropna()
    df = df[df["Revenue"] != ""]
    return df.reset_index(drop=True)


def make_graph(
    stock_data: pd.DataFrame,
    revenue_data: pd.DataFrame,
    stock_name: str,
    *,
    stock_cutoff: str = DEFAULT_STOCK_END,
    revenue_cutoff: str = DEFAULT_REVENUE_END,
    show: bool = True,
    output_html: str | None = None,
) -> go.Figure:
    """
    Build a two-row Plotly figure: historical close price vs. quarterly revenue.

    Parameters mirror the original assignment filters (dates as strings comparable
    to the ``Date`` columns after parsing).
    """
    stock_df = stock_data.copy()
    rev_df = revenue_data.copy()

    stock_df["Date"] = _to_naive_datetime(stock_df["Date"])
    rev_df["Date"] = _to_naive_datetime(rev_df["Date"])

    stock_specific = stock_df[stock_df["Date"] <= pd.Timestamp(stock_cutoff)]
    revenue_specific = rev_df[rev_df["Date"] <= pd.Timestamp(revenue_cutoff)]

    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        subplot_titles=("Historical Share Price", "Historical Revenue"),
        vertical_spacing=0.3,
    )
    fig.add_trace(
        go.Scatter(
            x=stock_specific["Date"],
            y=stock_specific["Close"].astype(float),
            name="Share Price",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=revenue_specific["Date"],
            y=revenue_specific["Revenue"].astype(float),
            name="Revenue",
        ),
        row=2,
        col=1,
    )
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(
        showlegend=False,
        height=900,
        title=stock_name,
        xaxis_rangeslider_visible=True,
    )

    if output_html:
        fig.write_html(output_html)
        logger.info("Wrote chart to %s", output_html)
    if show:
        fig.show()
    return fig


def run_tesla_pipeline(
    *,
    show: bool,
    html_path: str | None,
) -> tuple[pd.DataFrame, pd.DataFrame, go.Figure]:
    """Tesla (TSLA) price + revenue scrape and chart."""
    logger.info("Fetching TSLA history and Tesla quarterly revenue…")
    tesla_data = fetch_stock_history("TSLA")
    tesla_revenue = scrape_quarterly_revenue(TESLA_REVENUE_URL, "Tesla Quarterly Revenue")
    path = html_path or (None if show else "tesla_dashboard.html")
    fig = make_graph(
        tesla_data,
        tesla_revenue,
        "Tesla",
        show=show,
        output_html=path,
    )
    return tesla_data, tesla_revenue, fig


def run_gme_pipeline(
    *,
    show: bool,
    html_path: str | None,
) -> tuple[pd.DataFrame, pd.DataFrame, go.Figure]:
    """GameStop (GME) price + revenue scrape and chart (assignment date filters)."""
    logger.info("Fetching GME history and GameStop quarterly revenue…")
    gme_data = fetch_stock_history("GME")
    gme_revenue = scrape_quarterly_revenue(GME_REVENUE_URL, "GameStop Quarterly Revenue")

    cutoff = pd.Timestamp(GME_EXTRA_FILTER_END)
    gme_data["Date"] = _to_naive_datetime(gme_data["Date"])
    gme_revenue["Date"] = _to_naive_datetime(gme_revenue["Date"])
    gme_data = gme_data[gme_data["Date"] <= cutoff].copy()
    gme_revenue = gme_revenue[gme_revenue["Date"] <= cutoff].copy()

    path = html_path or (None if show else "gme_dashboard.html")
    fig = make_graph(
        gme_data,
        gme_revenue,
        "GameStop",
        show=show,
        output_html=path,
    )
    return gme_data, gme_revenue, fig


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Extract stock and revenue data and plot interactive dashboards.",
    )
    p.add_argument(
        "--tickers",
        nargs="+",
        default=["TSLA", "GME"],
        choices=["TSLA", "GME"],
        help="Which pipelines to run (default: both).",
    )
    p.add_argument(
        "--no-show",
        action="store_true",
        help="Do not open a browser; write HTML files instead.",
    )
    p.add_argument(
        "--output-dir",
        type=str,
        default=".",
        help="Directory for HTML output when --no-show is set (default: current).",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    show = not args.no_show
    out_dir = args.output_dir
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir, exist_ok=True)

    if "TSLA" in args.tickers:
        tesla_html = os.path.join(out_dir, "tesla_dashboard.html") if args.no_show else None
        _, _, _ = run_tesla_pipeline(show=show, html_path=tesla_html)

    if "GME" in args.tickers:
        gme_html = os.path.join(out_dir, "gme_dashboard.html") if args.no_show else None
        _, _, _ = run_gme_pipeline(show=show, html_path=gme_html)


if __name__ == "__main__":
    main()
