import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
from technicals import add_all_indicators

# Load + Process Data
def load_sheets(path):
    xls = pd.ExcelFile(path)
    dfs = {}

    for sheet in xls.sheet_names:
        df = pd.read_excel(path, sheet_name=sheet)

        # ensure datetime index
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"])
            df = df.set_index("Date")

        # Apply all indicators from technicals.py
        df = add_all_indicators(df)

        dfs[sheet] = df

    return dfs

# Backgrounds
DARK_BG_PRIMARY = '#17191d'
DARK_BG_SECONDARY = '#222426'

# Text & Lines
BRIGHT_TEXT = '#f3f4f6'
GRID_COLOR = '#4b5563'

# Charts
COLOR_OVER = '#2E3133'
COLOR_OVER_DASH = "#3F4345"

# Chart Colors
GRID_COLOR = '#4b5563'
COLOR_PRICE = '#f3f4f6'
COLOR_SMA20 = "#15d8fa"
COLOR_SMA50 = "#168bf9"
COLOR_BB_FILL = 'rgba(75, 85, 99, 0.3)'
COLOR_RSI = '#a78bfa'
COLOR_STOCH_K = '#facc15'
COLOR_STOCH_D = '#f97316'

# Charts
def price_with_technicals(df):
    """Creates a Price plot (Line) with SMA20, SMA50, and Bollinger Bands (Dark Mode)."""
    fig = go.Figure()

    # Upper Band
    fig.add_trace(go.Scatter(
        x=df.index, y=df['BB_Upper'], line=dict(color=GRID_COLOR, width=1), mode='lines', 
        name='BB Upper', showlegend=False
    ))

    # Lower Band
    fig.add_trace(go.Scatter(
        x=df.index, y=df['BB_Lower'], line=dict(color=GRID_COLOR, width=1), 
        mode='lines', fill='tonexty', fillcolor=COLOR_BB_FILL, 
        name='BB Lower'
    ))

    # SMA50
    fig.add_trace(go.Scatter(
        x=df.index, y=df['SMA_50'], line=dict(color=COLOR_SMA50, width=1.5), 
        name='MA50', opacity=0.9
    ))

    # SMA20
    fig.add_trace(go.Scatter(
        x=df.index, y=df['SMA_20'], line=dict(color=COLOR_SMA20, width=1.5), 
        name='MA20', opacity=0.9
    ))
    
    # Price
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Close'], mode='lines', name='Close Price',
        line=dict(color=COLOR_PRICE, width=2)
    ))

    fig.update_layout(xaxis_rangeslider_visible=False)
    return fig

# RSI Chart
def rsi_chart(df):
    """Creates the Relative Strength Index (RSI) chart (Traces only)."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['RSI'], line=dict(color=COLOR_RSI, width=2), name='RSI'
    ))
    return fig

# Stochastic Chart
def stoch_chart(df):
    """Creates the Stochastic Oscillator chart (%K and %D) (Traces only)."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Stoch_%K'], line=dict(color=COLOR_STOCH_K, width=2), name='%K'
    ))
    fig.add_trace(go.Scatter(
        x=df.index, y=df['Stoch_%D'], line=dict(color=COLOR_STOCH_D, width=1.5), name='%D'
    ))
    return fig

# Dash Subplots
def make_ticker_subplots(df, last_n=90):
    full_index = df.index
    row_heights = [0.6, 0.2, 0.2]

    # Create subplot figure
    fig = sp.make_subplots(
        rows=3, cols=1,
        # Set title
        # subplot_titles=(f"<span style='color:{BRIGHT_TEXT}'>Price</span>", 
        #                 f"<span style='color:{BRIGHT_TEXT}'>RSI</span>", 
        #                 f"<span style='color:{BRIGHT_TEXT}'>Stochastic Oscillator</span>"),
        vertical_spacing=0.02,
        row_heights=row_heights
    )

    # Price Chart
    try:
        price_fig = price_with_technicals(df)
        for trace in price_fig.data:
            fig.add_trace(trace, row=1, col=1)

        fig.update_yaxes(title_text="Price", row=1, col=1)

    except Exception:
        pass

    # RSI Chart
    try:
        rsi_fig = rsi_chart(df)
        for trace in rsi_fig.data:
            fig.add_trace(trace, row=2, col=1)

        # Overbought/Oversold shaded regions and lines
        fig.add_hrect(y0=70, y1=100, fillcolor=COLOR_OVER, layer="below", line_width=0, row=2, col=1)
        fig.add_hrect(y0=0, y1=30, fillcolor=COLOR_OVER, layer="below", line_width=0, row=2, col=1)
        fig.add_hline(y=70, line_dash="dash", line_color=COLOR_OVER_DASH, row=2, col=1)
        fig.add_hline(y=30, line_dash="dash", line_color=COLOR_OVER_DASH, row=2, col=1)

        fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)
    
    except Exception:
        pass

    # Stochastic Chart
    try:
        stoch_fig = stoch_chart(df)
        for trace in stoch_fig.data:
            fig.add_trace(trace, row=3, col=1)

        # Overbought/Oversold shaded regions and lines
        fig.add_hrect(y0=80, y1=100, fillcolor=COLOR_OVER, layer="below", line_width=0, row=3, col=1)
        fig.add_hrect(y0=0, y1=20, fillcolor=COLOR_OVER, layer="below", line_width=0, row=3, col=1)
        fig.add_hline(y=80, line_dash="dash", line_color=COLOR_OVER_DASH, row=3, col=1)
        fig.add_hline(y=20, line_dash="dash", line_color=COLOR_OVER_DASH, row=3, col=1)

        fig.update_yaxes(title_text="Stochastics", range=[0, 100], row=3, col=1)
    except Exception:
        pass

    # Modify x-axis range
    if len(df) > last_n:
        x_start = full_index[-last_n]
        x_end = full_index[-1]
        for row in [1, 2, 3]:
            # Setting the default view range
            fig.update_xaxes(range=[x_start, x_end], row=row, col=1)

    # Style
    for row in [1, 2, 3]:
        fig.update_xaxes(matches='x', row=row, col=1, showgrid=False) 
        fig.update_yaxes(gridcolor=GRID_COLOR, mirror=True) 

    fig.update_layout(
        height=1000,
        autosize=True,
        showlegend=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=80, b=50, l=50, r=50),
        
        title_font_size=18,
        font=dict(family="Tahoma, sans-serif", size=12, color=BRIGHT_TEXT),
        
        # Plot and Paper Backgrounds
        plot_bgcolor=DARK_BG_SECONDARY,
        paper_bgcolor=DARK_BG_PRIMARY, 
        hovermode="x unified",
        
        xaxis1_rangeslider_visible=False,
        xaxis_showgrid=False,
    )
    
    # Hide axis labels for middle and top charts
    fig.update_xaxes(showticklabels=False, row=1, col=1)
    fig.update_xaxes(showticklabels=False, row=2, col=1)


    return fig