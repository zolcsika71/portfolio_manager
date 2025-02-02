import os
import streamlit as st
import httpx
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env
DANELFIN_API_KEY = os.getenv("DANELFIN_API_KEY")

from src.models import DanelfinRequest


def main():
    st.title("Main Menu")
    st.subheader("Ticker Historical Data")

    # User input for ticker symbol
    ticker = st.text_input("Enter Ticker Symbol (e.g., TSLA, AMZN)")

    # Button to fetch data
    if st.button("Fetch Data"):
        try:
            url = f"https://apirest.danelfin.com/ranking?ticker={ticker}"
            headers = {
                "x-api-key": DANELFIN_API_KEY,  # Replace with your actual API key
            }

            # Fetch data
            with httpx.Client() as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()

            # If the data is a list of items
            if isinstance(data, list) and len(data) > 0:
                selected_item = st.selectbox("Select from available data", data)
                st.write("Selected item information:")
                st.json(selected_item)

            # If the data is a dictionary
            elif isinstance(data, dict):
                keys = list(data.keys())
                selected_key = st.selectbox("Select a key", keys)
                st.write("Selected key information:")
                st.json({selected_key: data[selected_key]})

            else:
                st.write("No data available or unknown format.")

        except httpx.HTTPError as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
