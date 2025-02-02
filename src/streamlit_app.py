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
    """
    Fetch all available tickers that have buy records from Danelfin API.
    This assumes the endpoint returns a simple JSON array of ticker symbols.
    """
    try:
        with httpx.Client() as client:
            # Hypothetical endpoint filtering tickers by buy records
            response = client.get("http://localhost:8000/api/tickers?filter=with_buy_records")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        st.error(f"Failed to retrieve ticker list: {e}")
        return []


def main():
    st.title("Danelfin API Client")
    with st.sidebar:
        st.header("Query Parameters")
        date = st.date_input("Date")

        ticker_list = fetch_tickers()

        # Set the default index to the position of "spx500" if present
        default_index = ticker_list.index("spx500") if "spx500" in ticker_list else 0
        ticker = st.selectbox("Ticker Symbol", options=ticker_list, index=default_index)

    aiscore = st.slider("AI Score", 1, 10, 10)
    low_risk = st.slider("Low Risk Score", 1, 10, 6)  # ← New slider for "Low Risk Score"
    sentiment = st.slider("Sentiment Score", 1, 10, 5)  # ← Added slider for sentiment
    sector = st.selectbox("Sector", [None, "health-care", "technology", "energy", "finance"]) # it needs to be adjusted
    industry = st.text_input("Industry")
    buy_track_record = st.checkbox("Buy Track Record")
    sell_track_record = st.checkbox("Sell Track Record")
    fields = st.text_input("Fields")

    if st.button("Fetch Data"):
        request = DanelfinRequest(
            date=date,
            ticker=ticker,
            aiscore=aiscore,
            low_risk=low_risk,  # ← Include “low_risk”
            sentiment=sentiment,  # ← Existing “sentiment”
            sector=sector,
            industry=industry,
            buy_track_record=buy_track_record,
            sell_track_record=sell_track_record,
            fields=fields
        )
        if data := fetch_data(request):
            df = pd.DataFrame(data)
            st.dataframe(df)


if __name__ == "__main__":
    main()