import os
import requests
import csv
from tabulate import tabulate
import yfinance as yf  # <-- NEW

# Constants
API_URL = "https://apirest.danelfin.com/ranking"


def ensure_directory(directory):
    """Ensure that the output directory exists."""
    os.makedirs(directory, exist_ok=True)


def fetch_top_100_stocks(api_key, date):
    """
    Fetches the top 100 stocks for a given date using the specified API key.

    Args:
        api_key (str): The API key for the API service.
        date (str): The date for which to fetch the stock data (yyyy-mm-dd).

    Returns:
        dict: A dictionary containing the API response.

    Raises:
        ValueError: If the API call fails.
    """
    headers = {"x-api-key": api_key}
    params = {"date": date}

    print(f"Requesting data for date: {date}")
    response = requests.get(API_URL, headers=headers, params=params)

    if response.status_code != 200:
        raise ValueError(
            f"API request failed with status {response.status_code}: {response.text}"
        )

    return response.json()


def filter_and_group_stocks(stock_data, min_low_risk_score, date):
    """
    Filter and group stocks by a minimum low-risk score.

    Args:
        stock_data (dict): The stock data fetched from the API.
        min_low_risk_score (int): The minimum low-risk score to filter stocks.
        date (str): The date data to filter stocks by.

    Returns:
        list: A list of filtered stock dictionaries.
    """
    return [
        {"ticker": ticker, **details}
        for ticker, details in stock_data.get(date, {}).items()
        if details.get("low_risk", 0) >= min_low_risk_score
    ]


def display_filtered_stocks(filtered_stocks):
    """
    Display the filtered stocks in a tabular format.

    Args:
        filtered_stocks (list): A list of filtered stock dictionaries.

    Returns:
        None
    """
    print(f"Filtered {len(filtered_stocks)} stocks based on risk threshold.")
    print(
        tabulate(
            [
                [
                    stock["ticker"],
                    stock["aiscore"],
                    stock["low_risk"],
                    stock["fundamental"],
                    stock["technical"],
                    stock["sentiment"],
                ]
                for stock in filtered_stocks
            ],
            headers=[
                "Ticker",
                "AI Score",
                "Low Risk Score",
                "Fundamental",
                "Technical",
                "Sentiment",
            ],
            tablefmt="grid",
        )
    )


def save_portfolio_to_csv(portfolio, directory, filename):
    """
    Save the filtered portfolio to a CSV file.

    Args:
        portfolio (list): A list of stock dictionaries.
        directory (str): Directory to save the CSV file.
        filename (str): Name of the CSV file.

    Returns:
        None
    """
    ensure_directory(directory)
    file_path = os.path.join(directory, filename)

    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["Ticker", "AI Score", "Low Risk Score", "Fundamental", "Technical", "Sentiment"])
        for stock in portfolio:
            writer.writerow(
                [
                    stock["ticker"],
                    stock["aiscore"],
                    stock["low_risk"],
                    stock["fundamental"],
                    stock["technical"],
                    stock["sentiment"],
                ]
            )

    print(f"Portfolio saved to {file_path}")


def save_tickers_to_txt(filtered_stocks, directory, filename):
    """
    Save the tickers to a text file, separated by a ".".

    Args:
        filtered_stocks (list): A list of filtered stock dictionaries.
        directory (str): Directory to save the TXT file.
        filename (str): Name of the TXT file.

    Returns:
        None
    """
    ensure_directory(directory)
    file_path = os.path.join(directory, filename)

    with open(file_path, mode="w") as file:
        file.write(",".join(stock["ticker"] for stock in filtered_stocks) + "\n")

    print(f"Tickers saved to {file_path}")
