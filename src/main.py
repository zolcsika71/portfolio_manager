import os
from dotenv import load_dotenv
from src.danelfin_api import (
    fetch_top_100_stocks,
    filter_and_group_stocks,
    save_portfolio_to_csv,
    display_filtered_stocks,
    save_tickers_to_txt,
)
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()
DANELFIN_API_KEY = os.getenv("DANELFIN_API_KEY")

# Constants
OUTPUT_DIR = "output"
TIME_DELTA = 2
MIN_LOW_RISK_SCORE = 6
DATE = (datetime.now() - timedelta(days=TIME_DELTA)).strftime("%Y-%m-%d")
TIME_STAMP = datetime.now().strftime("%Y%m%d%H%M%S")


def create_output_filenames(base_name):
    """Generate CSV and TXT filenames with a timestamp."""
    return {
        "csv": f"{base_name}_portfolio_{TIME_STAMP}.csv",
        "txt": f"{base_name}_portfolio_{TIME_STAMP}.txt",
    }


def main():
    try:
        # Build filenames
        filenames = create_output_filenames(OUTPUT_DIR)

        # Fetch AI-ranked stocks
        stock_data = fetch_top_100_stocks(DANELFIN_API_KEY, DATE)

        # Filter stocks based on risk threshold
        filtered_stocks = filter_and_group_stocks(stock_data, MIN_LOW_RISK_SCORE, DATE)

        # Debug/log the number of filtered stocks
        print(f"Number of filtered tickers: {len(filtered_stocks)}")

        # Display filtered stocks in a table format
        display_filtered_stocks(filtered_stocks)

        # Save the filtered portfolio to both CSV and TXT outputs
        save_portfolio_to_csv(filtered_stocks, OUTPUT_DIR, filenames["csv"])
        save_tickers_to_txt(filtered_stocks, OUTPUT_DIR, filenames["txt"])

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
