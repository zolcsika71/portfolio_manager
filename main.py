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
    """Returns the current date minus a specified number of days.

    Args:
        days (int): The number of days to subtract from the current date.

    Returns:
        str: The resulting date formatted as a string according to DATE_FORMAT.
    """
    return (datetime.now() - timedelta(days=days)).strftime(DATE_FORMAT)


def fetch_stock_data(api_key, date):
    """Fetch tops 100 AI-ranked stocks for a given date.

    Args:
        api_key (str): The API key for authentication with the Danelfin API.
        Date (str): The date for which to fetch the stock data, formatted as 'YYYY-MM-DD'.

    Returns:
        dict: A dictionary containing the stock data for the specified date.

    Raises:
        ValueError: If the API request fails or returns a status code other than 200.
    """
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
    """Filter stocks by low risk score for the given date.

    Args:
        stock_data (dict): A dictionary containing stock data, where keys are dates
                           and values are dictionaries of stock details.
        date (str): The date for which to filter stocks, formatted as 'YYYY-MM-DD'.
        risk_threshold (int): The minimum low risk score a stock must have to be included.

    Returns:
        list: A list of dictionaries, each containing the ticker and details of stocks
              that meet or exceed the low risk score threshold for the specified date.
    """
    return [
        {"ticker": ticker, **details}
        for ticker, details in stock_data.get(date, {}).items()
        if details.get("low_risk", 0) >= risk_threshold
    ]

def display_filtered_stocks(filtered_stocks):
    """Display the filtered stocks in a table format with details.

    Args:
        filtered_stocks (list): A list of dictionaries, each containing details of a stock
                                that has passed the filtering criteria. Each dictionary
                                should include keys such as 'ticker', 'aiscore', 'low_risk',
                                'fundamental', 'technical', and 'sentiment'.

    Returns:
        None: This function prints the filtered stocks to the console in a formatted table.
    """
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
    """Save the filtered portfolio to a CSV file.

    Args:
        portfolio (list): A list of dictionaries, each representing a stock with keys such as
                          'ticker', 'aiscore', 'low_risk', 'fundamental', 'technical', and 'sentiment'.
        Filename (str): The name of the file where the portfolio will be saved, including the file extension.

    Returns:
        None: This function doesn't return a value. It writes the portfolio data to a CSV file
              and prints a confirmation message upon successful saving.
    """
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
