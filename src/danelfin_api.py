# danelfin_api.py

import os
import requests
import csv
from datetime import datetime, timedelta
from tabulate import tabulate
import yfinance as yf

API_URL = "https://apirest.danelfin.com/ranking"

def ensure_directory(directory):
    """Ensure that the output directory exists."""
    os.makedirs(directory, exist_ok=True)

def fetch_top_100_stocks(api_key, date):
    """
    Fetches the top 100 stocks for a given date using the specified API key.
    ...
    """
    headers = {"x-api-key": api_key}
    params = {"date": date}

    print(f"Requesting data for date: {date}")
    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise ValueError(f"API request failed with status {response.status_code}: {response.text}")

    return response.json()

def combine_data_for_date_range(api_key, end_date_str, days):
    """
    Fetch data for a range of consecutive days (including end_date),
    going backwards in time.
    ...
    """
    results = {}
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    for i in range(days):
        date_to_fetch = (end_date - timedelta(days=i)).strftime("%Y-%m-%d")
        try:
            data = fetch_top_100_stocks(api_key, date_to_fetch)
            results[date_to_fetch] = data.get(date_to_fetch, {})
        except ValueError as e:
            print(f"Skipping {date_to_fetch} due to error: {e}")
    return results

def filter_and_group_stocks(stock_data, min_low_risk_score, date):
    """
    Filter and group stocks by a minimum low-risk score.
    ...
    """
    return [
        {"ticker": ticker, **details}
        for ticker, details in stock_data.get(date, {}).items()
        if details.get("low_risk", 0) >= min_low_risk_score
    ]

def enrich_with_sector_and_industry(filtered_stocks):
    """
    Use yfinance to fetch sector and industry info for each stock.
    """
    for stock in filtered_stocks:
        ticker_symbol = stock["ticker"]
        try:
            yf_ticker = yf.Ticker(ticker_symbol)
            sector = yf_ticker.info.get("sector", "N/A")
            industry = yf_ticker.info.get("industry", "N/A")
        except Exception as e:
            print(f"Warning: Could not fetch yfinance data for {ticker_symbol} - {e}")
            sector, industry = "N/A", "N/A"

        stock["sector"] = sector
        stock["industry"] = industry

    return filtered_stocks

def display_filtered_stocks(filtered_stocks):
    """
    Display the filtered stocks in a tabular format with aligned columns.
    """
    # Create a list of lists for tabulate
    table_data = [
        [
            stock["ticker"],
            stock["aiscore"],
            stock["low_risk"],
            stock["fundamental"],
            stock["technical"],
            stock["sentiment"],
            stock.get("sector", "N/A"),
            stock.get("industry", "N/A"),
        ]
        for stock in filtered_stocks
    ]

    # Headers for each column
    headers = [
        "Ticker",
        "AI Score",
        "Low Risk Score",
        "Fundamental",
        "Technical",
        "Sentiment",
        "Sector",
        "Industry"
    ]

    print(
        tabulate(
            table_data,
            headers=headers,
            tablefmt="tsv"
        )
    )


def save_portfolio_to_csv(portfolio, directory, filename):
    """
    Save the filtered portfolio to a CSV file.
    ...
    """
    ensure_directory(directory)
    file_path = os.path.join(directory, filename)

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Ticker", "AI Score", "Low Risk Score",
            "Fundamental", "Technical", "Sentiment",
            "Sector", "Industry"
        ])
        for stock in portfolio:
            writer.writerow([
                stock["ticker"],
                stock["aiscore"],
                stock["low_risk"],
                stock["fundamental"],
                stock["technical"],
                stock["sentiment"],
                stock.get("sector", "N/A"),
                stock.get("industry", "N/A"),
            ])
    print(f"Portfolio saved to {file_path}")

def save_tickers_to_txt(filtered_stocks, directory, filename):
    """
    Save the tickers to a text file, separated by ",".
    ...
    """
    ensure_directory(directory)
    file_path = os.path.join(directory, filename)

    with open(file_path, mode="w") as file:
        file.write(",".join(stock["ticker"] for stock in filtered_stocks) + "\n")

    print(f"Tickers saved to {file_path}")
