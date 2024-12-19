import os
import requests
import csv
from dotenv import load_dotenv
from tabulate import tabulate
from datetime import datetime, timedelta

# Constants
DATE_FORMAT = "%Y-%m-%d"
DANELFIN_API_ENDPOINT = "https://apirest.danelfin.com/ranking"
PORTFOLIO_SIZE = 30  # Target portfolio size
RISK_THRESHOLD = 6  # Low risk score threshold
INPUT_FILE = "portfolio_input.csv"
OUTPUT_FILE = "portfolio_output.csv"

# Load environment variables
load_dotenv()
DANELFIN_API_KEY = os.getenv("DANELFIN_API_KEY")


def get_current_date_minus_days(days):
    """Returns the current date minus a specified number of days."""
    return (datetime.now() - timedelta(days=days)).strftime(DATE_FORMAT)


def fetch_stock_data(api_key, date):
    """Fetch tops 100 AI-ranked stocks for a given date."""
    headers = {"x-api-key": api_key}
    params = {"date": date}
    print(f"Requesting data for date: {date}")
    response = requests.get(DANELFIN_API_ENDPOINT, headers=headers, params=params)
    print(f"Request URL: {response.url}")
    print(f"Response Status Code: {response.status_code}")
    if response.status_code != 200:
        raise ValueError(f"API request failed with status {response.status_code}: {response.text}")
    return response.json()


def filter_stocks_by_risk(stock_data, date, risk_threshold):
    """Filter stocks by low risk score for the given date."""
    return [
        {"ticker": ticker, **details}
        for ticker, details in stock_data.get(date, {}).items()
        if details.get("low_risk", 0) >= risk_threshold
    ]

def display_filtered_stocks(filtered_stocks):
    """Display the filtered stocks in a table format with details."""
    print(f"Filtered {len(filtered_stocks)} stocks based on risk threshold.")
    print(tabulate(
        [
            [
                stock["ticker"], stock["aiscore"], stock["low_risk"],
                stock["fundamental"], stock["technical"], stock["sentiment"]
            ]
            for stock in filtered_stocks
        ],
        headers=["Ticker", "AI Score", "Low Risk Score", "Fundamental", "Technical", "Sentiment"],
        tablefmt="grid"
    ))

def save_portfolio_to_csv(portfolio, filename):
    """Save the filtered portfolio to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Ticker", "AI Score", "Low Risk Score", "Fundamentals", "Technical", "Sentiment"])
        for stock in portfolio:
            writer.writerow([stock["ticker"], stock["aiscore"], stock["low_risk"], stock["fundamental"], stock["technical"], stock["sentiment"]])
    print(f"Portfolio saved to {filename}")


def main():
    try:
        # Step 1: Calculate the target date (2 days ago)
        target_date = get_current_date_minus_days(2)

        # Step 2: Fetch the stock data
        stock_data = fetch_stock_data(DANELFIN_API_KEY, target_date)

        # Step 3: Filter stocks based on a risk threshold
        filtered_stocks = filter_stocks_by_risk(stock_data, target_date, RISK_THRESHOLD)

        # Debugging: Display filtered result and count
        display_filtered_stocks(filtered_stocks)

        # Step 4: Save filtered stocks to a CSV file
        save_portfolio_to_csv(filtered_stocks, OUTPUT_FILE)

    except Exception as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    main()
