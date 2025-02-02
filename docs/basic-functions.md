* Danelfin API Guide
  - Ticker Historical Data

        ticker:
            cURL Example:
            curl -H 'x-api-key: THE_API_KEY_CREATED' "https://apirest.danelfin.com/ranking?ticker=PYPL"

  - All Data in a Day (Top 100 Tickers)

        date:
            cURL Example:
            curl -H 'x-api-key: THE_API_KEY_CREATED' "https://apirest.danelfin.com/ranking?date=2024-01-02"

  - Ticker Data in a Day

        date:
        ticker:
            cURL Example:
            curl -H 'x-api-key: THE_API_KEY_CREATED' "https://apirest.danelfin.com/ranking?date=2024-01-02&ticker=PYPL"

  - Value by Score Type in a Day

        date:
        value_type (choose one: aiscore, technical, low_risk, sentiment, fundamental)
        value (optional, from 1-10):
            cURL Example:
            curl -H 'x-api-key: THE_API_KEY_CREATED' "https://apirest.danelfin.com/ranking?date=2024-01-02&value_type=aiscore&value=7"

  - BUY Track Record in a Date

        date:
        buy_track_record (set to on to enable):
            cURL Example:
            curl -H 'x-api-key: THE_API_KEY_CREATED' "https://apirest.danelfin.com/ranking?date=2024-01-02&buy_track_record=on"

  - SELL Track Record in a Date

        date:
        sell_track_record (set to on to enable):
            cURL Example:
            curl -H 'x-api-key: THE_API_KEY_CREATED' "https://apirest.danelfin.com/ranking?date=2024-01-02&sell_track_record=on"

  - Tickers of Sector in a Date

        date:
        sector:
            cURL Example:
            curl -H 'x-api-key: THE_API_KEY_CREATED' "https://apirest.danelfin.com/ranking?date=2024-01-02&sector=Utilities"

  - Tickers of Industry in a Date

        date:
        industry:
            cURL Example:
            curl -H 'x-api-key: THE_API_KEY_CREATED' "https://apirest.danelfin.com/ranking?date=2024-01-02&industry=banks"

  - Custom Fields in Response

        Description: You can specify custom fields to be included in the response.
            cURL Example:
            curl -H 'x-api-key: THE_API_KEY_CREATED' "https://apirest.danelfin.com/ranking?custom_fields=field1,field2"


