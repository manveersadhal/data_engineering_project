import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import date, timedelta, datetime
import plotly.express as px
# import matplotlib.pyplot as plt
# import seaborn as sns
# from re import A

engine = create_engine('sqlite:///stocks.db')

table = 'historical_prices'
symbol = 'AAPL'
end_date = date.today() - timedelta(days=1)
start_date = end_date - timedelta(days=30)
sql = f"""
SELECT DISTINCT Symbol
FROM {table}
"""

symbol_df = pd.read_sql(sql, engine)
symbol_list = symbol_df['Symbol'].tolist()

st.title('Stock Dashboard')

symbol = st.text_input("Symbol", "AAPL").upper().strip()

if symbol in symbol_list:
    period_months = st.slider('Number of Months', min_value=5/30, max_value=float(15*12), value=1.0)
    period_days = round(period_months*(365/12))

    start_date = end_date - timedelta(days=period_days)
    
    sql = f"""
    SELECT MIN(Date)
    FROM {table}
    WHERE Symbol='{symbol}';
    """
    earliest_trading_date = datetime.strptime(pd.read_sql(sql, engine).iloc[0, 0][:10], '%Y-%m-%d').date()

    sql = f"""
    SELECT Symbol, Adj_Close, Date
    FROM {table}
    WHERE Symbol='{symbol}' AND Date BETWEEN '{start_date}' AND '{end_date}';
    """

    data_to_plot = pd.read_sql(sql, engine)
    data_to_plot['Date'] = pd.to_datetime(data_to_plot['Date'], yearfirst=True)
    if start_date < earliest_trading_date:
        start_date = earliest_trading_date
        st.write(f"First date available is {start_date.strftime('%B %d, %Y')}")

    fig = px.line(x=data_to_plot['Date'], y=data_to_plot['Adj_Close'])
    fig.update_layout(
        title = f"{symbol} from {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}",
        xaxis_title = "Date",
        yaxis_title="Adjusted Close (USD)"
    )

    st.plotly_chart(fig)

    table = 'daily_metrics'
    sql = f"""
    SELECT sector, longBusinessSummary, city, state, country, website, address1, totalRevenue, totalCash, totalDebt, financialCurrency, longName,
    forwardPE, trailingPE, fiftyTwoWeekLow, fiftyTwoWeekHigh, ebitda, marketCap
    FROM {table}
    WHERE symbol='{symbol}';
    """

    attributes = pd.read_sql(sql, engine)

    #assign variables that require manipulation or are used multiple times
    financial_currency = attributes.loc[0, 'financialCurrency']
    revenue = "{:,}".format(attributes.loc[0, 'totalRevenue'])
    total_cash = "{:,}".format(attributes.loc[0, 'totalCash'])
    total_debt = "{:,}".format(attributes.loc[0, 'totalDebt'])
    market_cap = "{:,}".format(attributes.loc[0,'marketCap'])
    ebitda = "{:,}".format(attributes.loc[0,'ebitda'])

    try:
        forward_PE = round(float(attributes.loc[0, 'forwardPE']), 2)
    except TypeError:
        forward_PE = "Not available"
    
    try:
        trailing_PE = round(float(attributes.loc[0, 'trailingPE']), 2)
    except TypeError:
        trailing_PE = "Not available"

    cols = st.beta_columns(2)
    
    #left column of info under chart
    cols[0].header("Financials")
    cols[0].write(f"""
    Revenue: {revenue} {financial_currency}\n
    Total Cash: {total_cash} {financial_currency}\n
    Total Debt: {total_debt} {financial_currency}\n
    EBITDA: {ebitda} {financial_currency}
    """)

    #right column of info under chart
    cols[1].header("Metrics")
    cols[1].write(f"""
    Market Cap: {market_cap} {financial_currency}\n
    Forward P/E: {forward_PE}\n
    Trailing P/E: {trailing_PE}\n
    52-week range: {attributes.loc[0, 'fiftyTwoWeekLow']} - {attributes.loc[0, 'fiftyTwoWeekHigh']} USD
    """)
    
    #left sidebar
    st.sidebar.title(f"{attributes.loc[0, 'longName']} Overview")
    st.sidebar.markdown(f"""
    {attributes.loc[0, 'address1']}, {attributes.loc[0, 'city']}, {attributes.loc[0, 'state']}, {attributes.loc[0, 'country']}\n
    Sector: {attributes.loc[0, 'sector']}\n
    Website: {attributes.loc[0, 'website']}\n
    {attributes.loc[0, 'longBusinessSummary']}
    """)
else:
    st.write("Sorry! Symbol not available. Please enter another symbol.")
