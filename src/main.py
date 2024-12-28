# main.py

import os
from dotenv import load_dotenv
import argparse
from datetime import datetime, timedelta

from src.danelfin_api import (
    fetch_top_100_stocks,
    filter_and_group_stocks,
    save_portfolio_to_csv,
    display_filtered_stocks,
    save_tickers_to_txt,
    combine_data_for_date_range,
    enrich_with_sector_and_industry  # <-- NEW
)

# Load environment variables
load_dotenv()
DANELFIN_API_KEY = os.getenv("DANELFIN_API_KEY")

OUTPUT_DIR = "output"

def create_output_filenames(base_name):
    """Generate CSV and TXT filenames with a timestamp."""
    time_stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return {
        "csv": f"{base_name}_portfolio_{time_stamp}.csv",
        "txt": f"{base_name}_portfolio_{time_stamp}.txt",
    }

def main():
    parser = argparse.ArgumentParser(description="Fetch and filter stocks via Danelfin API.")
    parser.add_argument(
        "--date",
        type=str,
        default=(datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
        help="Specify the date (yyyy-mm-dd) to fetch the data. Defaults to 2 days ago."
    )
    parser.add_argument(
        "--min_low_risk_score",
        type=int,
        default=6,
        help="Minimum low-risk score to filter on. Default is 6."
    )
    parser.add_argument(
        "--days",
        type=int,
        default=1,
        help="Number of days of data to fetch. Default is 1 (only the specified date)."
    )
    args = parser.parse_args()

    try:
        _extracted_from_main_24(args)
    except Exception as e:
        print(f"Error: {e}")


# TODO Rename this here and in `main`
def _extracted_from_main_24(args):
    filenames = create_output_filenames(OUTPUT_DIR)

    # Either fetch data for a single date or a range of dates
    if args.days == 1:
        stock_data = fetch_top_100_stocks(DANELFIN_API_KEY, args.date)
        filtered_stocks = filter_and_group_stocks(stock_data, args.min_low_risk_score, args.date)
    else:
        stock_data = combine_data_for_date_range(DANELFIN_API_KEY, args.date, args.days)
        filtered_stocks = []
        for date_key, data_for_day in stock_data.items():
            filtered = filter_and_group_stocks({date_key: data_for_day}, args.min_low_risk_score, date_key)
            filtered_stocks.extend(filtered)

    # NEW: Enrich with sector and industry using yfinance
    filtered_stocks = enrich_with_sector_and_industry(filtered_stocks)

    print(f"Number of filtered tickers: {len(filtered_stocks)}")

    # Display them in tabular form, including sector & industry
    display_filtered_stocks(filtered_stocks)

    # Save to CSV and TXT
    save_portfolio_to_csv(filtered_stocks, OUTPUT_DIR, filenames["csv"])
    save_tickers_to_txt(filtered_stocks, OUTPUT_DIR, filenames["txt"])

if __name__ == "__main__":
    main()
