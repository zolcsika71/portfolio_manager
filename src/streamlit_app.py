import streamlit as st
import pandas as pd
from datetime import datetime
import httpx
from .models import DanelfinRequest

st.set_page_config(page_title="Danelfin API Client", layout="wide")


def main():
    st.title("Danelfin API Client")

    # Create sidebar for inputs
    with st.sidebar:
        st.header("Parameters")
        date = st.date_input("Date", value=datetime.now().date())
        ticker = st.text_input("Ticker Symbol")
        aiscore = st.slider("AI Score", min_value=1, max_value=10, value=5)
        sector = st.selectbox("Sector", [
            None, "communication-services", "consumer-discretionary",
            "consumer-staples", "energy", "financials", "health-care",
            "industrials", "information-technology", "materials",
            "real-estate", "utilities"
        ])
        industry = st.text_input("Industry")
        buy_track_record = st.checkbox("Buy Track Record")
        sell_track_record = st.checkbox("Sell Track Record")
        fields = st.multiselect(
            "Fields",
            ["aiscore", "technical", "low_risk", "sentiment", "fundamental",
             "buy_track_record", "sell_track_record"]
        )

        submit = st.button("Get Data")

    if submit:
        # Create request parameters
        params = DanelfinRequest(
            date=date,
            ticker=ticker or None,
            aiscore=aiscore,
            sector=sector,
            industry=industry or None,
            buy_track_record=buy_track_record or None,
            sell_track_record=sell_track_record or None,
            fields=",".join(fields) if fields else None
        )

        # Make request to FastAPI backend
        try:
            _extracted_from_main_42(params)
        except Exception as e:
            st.error(f"Error fetching data: {str(e)}")


# TODO Rename this here and in `main`
def _extracted_from_main_42(params):
    response = httpx.post(
        "http://localhost:8000/api/data",
        json=params.dict(exclude_none=True)
    )
    data = response.json()

    # Display results
    st.header("Results")
    df = pd.DataFrame(data)
    st.dataframe(df)

    # Add download button
    csv = df.to_csv(index=False)
    st.download_button(
        "Download CSV",
        csv,
        "danelfin_data.csv",
        "text/csv",
        key='download-csv'
    )


if __name__ == "__main__":
    main()