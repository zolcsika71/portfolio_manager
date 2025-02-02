# src/streamlit_app.py
import streamlit as st
import httpx
from datetime import datetime
import os
from models import ScoreType, SectorList, DanelfinRequest


def init_session_state():
    if 'api_key' not in st.session_state:
        st.session_state.api_key = os.getenv("DANELFIN_API_KEY")


def make_api_request(params: dict):
    headers = {"x-api-key": st.session_state.api_key}
    url = "https://apirest.danelfin.com/ranking"
    try:
        with httpx.Client() as client:
            response = client.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        st.error(f"API Error: {str(e)}")
        return None


def main():
    st.title("Danelfin API Explorer")
    init_session_state()

    # Query Type Selection
    query_type = st.selectbox(
        "Select Query Type",
        [
            "Ticker Historical Data",
            "All Data in a Day (Top 100)",
            "Ticker Data in a Day",
            "Value by Score Type",
            "BUY Track Record",
            "SELL Track Record",
            "Tickers by Sector",
            "Tickers by Industry",
            "Custom Fields"
        ]
    )

    # Parameter inputs based on query type
    params = {}

    if query_type == "Ticker Historical Data":
        ticker = st.text_input("Enter Ticker Symbol")
        if ticker:
            params["ticker"] = ticker.upper()

    elif query_type in ["All Data in a Day (Top 100)", "BUY Track Record", "SELL Track Record"]:
        date = st.date_input("Select Date")
        params["date"] = date.strftime("%Y-%m-%d")
        if query_type == "BUY Track Record":
            params["buy_track_record"] = ""
        elif query_type == "SELL Track Record":
            params["sell_track_record"] = ""

    elif query_type == "Ticker Data in a Day":
        date = st.date_input("Select Date")
        ticker = st.text_input("Enter Ticker Symbol")
        if date and ticker:
            params["date"] = date.strftime("%Y-%m-%d")
            params["ticker"] = ticker.upper()

    elif query_type == "Value by Score Type":
        date = st.date_input("Select Date")
        score_type = st.selectbox("Select Score Type", list(ScoreType))
        score_value = st.slider("Select Score Value", 1, 10, 5)
        if date:
            params["date"] = date.strftime("%Y-%m-%d")
            params[score_type] = score_value

    elif query_type == "Tickers by Sector":
        date = st.date_input("Select Date")
        sector = st.selectbox("Select Sector", list(SectorList))
        if date and sector:
            params["date"] = date.strftime("%Y-%m-%d")
            params["sector"] = sector

    elif query_type == "Tickers by Industry":
        date = st.date_input("Select Date")
        industry = st.text_input("Enter Industry")
        if date and industry:
            params["date"] = date.strftime("%Y-%m-%d")
            params["industry"] = industry.lower()

    elif query_type == "Custom Fields":
        date = st.date_input("Select Date")
        fields = st.multiselect(
            "Select Fields",
            ["date", "ticker", "aiscore", "technical", "low_risk", "sentiment", "fundamental"]
        )
        if date and fields:
            params["date"] = date.strftime("%Y-%m-%d")
            params["fields"] = ",".join(fields)

    # Execute API request
    if st.button("Fetch Data") and params:
        with st.spinner("Fetching data..."):
            data = make_api_request(params)
            if data:
                st.json(data)

    # Display current query parameters
    if params:
        st.sidebar.subheader("Current Query Parameters")
        st.sidebar.json(params)


if __name__ == "__main__":
    main()

