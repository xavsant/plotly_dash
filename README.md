# Plotly Dash
This repo creates a dummy dashboard using 1Y ticker data from NASDAQ.

## Instructions
This dash is pythonic in that its components can be quite easily modified to fit time series analysis. Currently, it produces a Plotly Dash which contains selectable tickers across 2 different tabs (stocks and precious metals).

### Input
Input data accepts a `.xlsx` file with sheets, where each sheet represents historical data of a specific product. **Technical indicators** from `technicals.py` are calculated and added to each sheet.

### CSS
Style and colours of dashboard can be customised in `assets/styles.css`.

### Dashboard
Modify `helper.py` and `app.py` to get the type of charts desired.
