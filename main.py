import os
import requests
import csv
from dotenv import load_dotenv
from collections import defaultdict
from tabulate import tabulate
from datetime import datetime

# Load environment variables
load_dotenv()
API_KEY = os.getenv("DANELFIN_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")  # Replace with your Alpha Vantage API key

# Constants
API_URL = "https://apirest.danelfin.com/ranking"
SECTOR_LIMIT = 6  # Maximum number of sectors for diversification
PORTFOLIO_SIZE = 30  # Target portfolio size
MIN_AI_SCORE = 9
MIN_LOW_RISK_SCORE = 6
INPUT_CSV = "portfolio.csv"
OUTPUT_CSV = "portfolio_with_sectors.csv"

# Function to fetch the first 100 AI scored tickers from the API
def fetch_top_100_stocks(api_key):
    headers = {"x-api-key": api_key}
    current_date = datetime.now().strftime("%Y-%m-%d")
    params = {"date": current_date}  # Use current date
    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise ValueError(f"API request failed with status code {response.status_code}: {response.text}")

    print(f"Generated Link: {response.url}")
    return response.json()

# Function to filter stocks by risk and sector
def filter_and_group_stocks(stock_data, min_low_risk_score):
    filtered_stocks = []
    current_date = datetime.now().strftime("%Y-%m-%d")

    for ticker, details in stock_data.get(current_date, {}).items():
        if details.get("low_risk", 0) >= min_low_risk_score:
            filtered_stocks.append({"ticker": ticker, **details})

    return filtered_stocks

# Function to fetch sector information using Alpha Vantage
def fetch_sector_info_alpha_vantage(tickers):
    sector_info = {}
    for ticker in tickers:
        try:
            url = "https://www.alphavantage.co/query"
            params = {"function": "OVERVIEW", "symbol": ticker, "apikey": ALPHA_VANTAGE_API_KEY}
            response = requests.get(url, params=params)
            data = response.json()

            sector = data.get("Sector", "Unknown")
            sector_info[ticker] = sector
        except Exception as e:
            print(f"Error fetching sector data for {ticker}: {e}")
            sector_info[ticker] = "Unknown"
    return sector_info

# Function to save portfolio to CSV with sector information
def save_to_csv_with_sectors(portfolio, filename):
    tickers = [stock["ticker"] for stock in portfolio]
    sector_info = fetch_sector_info_alpha_vantage(tickers)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Ticker", "AI Score", "Low Risk Score", "Sector"])

        for stock in portfolio:
            sector = sector_info.get(stock["ticker"], "Unknown")
            writer.writerow([stock["ticker"], stock["aiscore"], stock["low_risk"], sector])

    print(f"Portfolio with sectors saved to {filename}")

# Main execution
def main():
    try:
        # Step 1: Fetch the first 100 stocks
        stock_data = fetch_top_100_stocks(API_KEY)

        # Step 2: Filter stocks by low_risk >= 6
        filtered_stocks = filter_and_group_stocks(stock_data, MIN_LOW_RISK_SCORE)

        # Debug: Print the number of filtered tickers
        print(f"Number of filtered tickers: {len(filtered_stocks)}")

        # Debug: Format and print filtered stocks as a table
        table = [[stock["ticker"], stock["aiscore"], stock["low_risk"]] for stock in filtered_stocks]
        print(tabulate(table, headers=["Ticker", "AI Score", "Low Risk Score"], tablefmt="grid"))

        # Step 3: Save filtered stocks with sector information to CSV
        save_to_csv_with_sectors(filtered_stocks, OUTPUT_CSV)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

