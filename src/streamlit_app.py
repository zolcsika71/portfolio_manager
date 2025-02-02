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


def main():
    st.title("Danelfin API Client")
    with st.sidebar:
        st.header("Query Parameters")
        date = st.date_input("Date")
        ticker = st.text_input("Ticker Symbol", value="spx500")  # Default set to "spx500"
        aiscore = st.slider("AI Score", 1, 10, 10)
        low_risk = st.slider("Low Risk Score", 1, 10, 6)  # ← New slider for "Low Risk Score"
        sentiment = st.slider("Sentiment Score", 1, 10, 5)  # ← Added slider for sentiment
        sector = st.selectbox("Sector", [None, "health-care", "technology", "energy", "finance"])
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