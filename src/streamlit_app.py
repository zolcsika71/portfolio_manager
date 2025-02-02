import streamlit as st
import pandas as pd
import httpx
from models import DanelfinRequest

st.set_page_config(page_title="Danelfin API Client", layout="wide")


def fetch_data(request: DanelfinRequest):
    try:
        with httpx.Client() as client:
            response = client.post("http://localhost:8000/api/data", json=request.dict(exclude_none=True))
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        st.error(f"Failed to retrieve data: {e}")
        return None


def fetch_tickers():
    try:
        with httpx.Client(timeout=30.0) as client:  # Increase timeout to 30s
            response = client.get("http://localhost:8000/api/tickers?filter=with_buy_records")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        # Handle the error case
        return []


def main():
    st.title("Danelfin API Client")

    with st.sidebar:
        st.header("Query Parameters")

        # Date and Ticker
        date = st.date_input("Date")
        days_offset = st.slider("Days Offset", 1, 7, 3)
        ticker_list = fetch_tickers()
        default_index = ticker_list.index("spx500") if "spx500" in ticker_list else 0
        ticker = st.selectbox("Ticker Symbol", options=ticker_list, index=default_index)

        # Sliders
        aiscore = st.slider("AI Score", 1, 10, 10)
        low_risk = st.slider("Low Risk Score", 1, 10, 6)
        sentiment = st.slider("Sentiment Score", 1, 10, 5)
        technical = st.slider("Technical Score", 1, 10, 5)
        fundamental = st.slider("Fundamental Score", 1, 10, 5)

        # Other Inputs
        sector = st.selectbox("Sector", [None, "health-care", "technology", "energy", "finance"])
        industry = st.text_input("Industry")
        buy_track_record = st.checkbox("Buy Track Record")
        sell_track_record = st.checkbox("Sell Track Record")

        # Fetch Data
        if st.button("Fetch Data"):
            request = DanelfinRequest(
                date=date,
                days_offset=days_offset,
                ticker=ticker,
                aiscore=aiscore,
                low_risk=low_risk,
                sentiment=sentiment,
                technical=technical,
                fundamental=fundamental,
                sector=sector,
                industry=industry,
                buy_track_record=buy_track_record,
                sell_track_record=sell_track_record
            )
            if data := fetch_data(request):
                df = pd.DataFrame(data)
                st.dataframe(df)


if __name__ == "__main__":
    main()