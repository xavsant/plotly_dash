from dash import Dash, html, dcc, Output, Input
from helper import load_sheets, make_ticker_subplots
import plotly.graph_objects as go

# Tickers
STOCK_SYMBOLS = ["AAPL", "MSFT", "NVDA"]
PRECIOUS_METALS_SYMBOLS = ["GLD", "SLV"]

file_path = "data/dataset.xlsx"
dfs = load_sheets(file_path)


app = Dash(__name__)
app.layout = html.Div(className='main-wrapper', children=[
    
    # Header
    html.Div(className='header-container', children=[
        html.H1("Technical Indicators Dashboard"),
    ]),

    # Tabs
    dcc.Tabs(
        id='main-tabs',
        value='tab-1',
        className='dashboard-tabs',
        children=[
            # Stocks Tab
            dcc.Tab(
                label="Stocks",
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected',
                
                children=[
                    # Dropdown
                    html.Div(className='dropdown-container', children=[
                        html.Label("Select Ticker:"),
                        dcc.Dropdown(
                            id='stock-dropdown',
                            options=[{'label': s, 'value': s} for s in STOCK_SYMBOLS],
                            value=STOCK_SYMBOLS[0],
                            clearable=False,
                            style={'width': '250px'}
                        )
                    ]),
                    dcc.Graph(
                        id='stock-graph',
                        style={'height': '900px', 'width': '100%', 'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.5)'}, 
                        config={'responsive': True, 'displayModeBar': True}
                    )
                ]
            ),

            # Precious Metals Tab
            dcc.Tab(
                label="Precious Metals",
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected',
                children=[
                    # Dropdown
                    html.Div(className='dropdown-container', children=[
                        html.Label("Select Ticker:"),
                        dcc.Dropdown(
                            id='precious-metals-dropdown',
                            options=[{'label': s, 'value': s} for s in PRECIOUS_METALS_SYMBOLS],
                            value=PRECIOUS_METALS_SYMBOLS[0],
                            clearable=False,
                            style={'width': '250px'}
                        )
                    ]),
                    dcc.Graph(
                        id='precious-metals-graph',
                        style={'height': '900px', 'width': '100%', 'boxShadow': '0 4px 10px rgba(0, 0, 0, 0.5)'},
                        config={'responsive': True, 'displayModeBar': True}
                    )
                ]
            )
        ]
    )
])

# Callback
@app.callback(
    Output('stock-graph', 'figure'),
    Input('stock-dropdown', 'value')
)
def update_equity_graph(selected_ticker):
    if selected_ticker and selected_ticker in dfs:
        return make_ticker_subplots(dfs[selected_ticker])
    return go.Figure().update_layout(title="Select a valid Stock Ticker to view the analysis.", height=900, template='plotly_dark')

@app.callback(
    Output('precious-metals-graph', 'figure'),
    Input('precious-metals-dropdown', 'value')
)
def update_commodity_graph(selected_ticker):
    if selected_ticker and selected_ticker in dfs:
        return make_ticker_subplots(dfs[selected_ticker])
    return go.Figure().update_layout(title="Select a valid Precious Metals Ticker to view the analysis.", height=900, template='plotly_dark')

if __name__ == "__main__":
    app.run(debug=True)