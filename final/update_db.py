import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine

#get list of tickers/symbols
def get_symbol_list(quantity):
#   nasdaq_download_url = 'http://www.nasdaq.com/screening/companies-by-name.aspx?letter=0&exchange=all&render=download'
    tickers_df = pd.read_csv('nasdaq_screener_Nasdaq_NYSE_AMEX_2021-10-13.csv')
    tickers_df.sort_values(['Market Cap'], ascending=False, inplace=True)
    symbol_list = tickers_df['Symbol'][:quantity].tolist()
    return symbol_list


#connect to yfinance to download data for update
def get_historical_data(symbol_list, start_date, end_date):
    return yf.download(symbol_list, start=start_date, end=end_date)


#transform dataframe from yfinance to long form, remove multi-index
def hist_data_to_long_form(df):
    df_long = df.reset_index().melt('Date', var_name=['var', 'Symbol'])
    df_long = df_long.pivot_table(index=['Date', 'Symbol'], columns='var', values='value').reset_index()
    df_long = df_long.rename(columns={'Adj Close' : 'Adj_Close'})
    return df_long


#get metrics about each company, some of which are updated daily
def get_daily_metrics(symbol_list):
    metrics_df = pd.DataFrame()
    for symbol in symbol_list:
        ticker = yf.Ticker(symbol)
        #reducing the fields that need to be retrieved
        fields_to_retrieve = ['zip', 'sector', 'longBusinessSummary', 'city', 'phone', 'state', 'country', 'website', 'address1', 'industry',
        'ebitdaMargins', 'profitMargins', 'grossMargins', 'operatingCashflow', 'revenueGrowth', 'operatingMargins',
        'ebitda', 'targetLowPrice', 'recommendationKey', 'grossProfits', 'freeCashflow', 'targetMedianPrice',
        'currentPrice', 'earningsGrowth', 'currentRatio', 'returnOnAssets', 'targetMeanPrice', 'debtToEquity',
        'returnOnEquity', 'targetHighPrice', 'totalCash', 'totalDebt', 'totalRevenue', 'financialCurrency', 
        'revenuePerShare', 'exchange', 'shortName', 'longName', 'exchangeTimezoneName', 'exchangeTimeZoneShortName',
        'symbol', 'market', 'enterpriseEbitda', 'forwardEPS', 'sharesOutstanding', 'trailingEps', 'SandP52WeekChange',
        'beta', 'forwardPE', 'previousClose', 'regularMarketOpen', 'twoHundredDayAverage', 'fiftyDayAverage',
        'regularMarketDayLow', 'currency', 'trailingPE', 'regularMarketVolume', 'marketCap', 'averageVolume', 'dayLow', 'ask',
        'askSize', 'volume', 'fiftyTwoWeekHigh', 'fiftyTwoWeekLow', 'bid', 'dayHigh', 'regularMarketPrice', 'logo_url']
        
        daily_metrics = {key:ticker.info[key] for key in ticker.info if key in fields_to_retrieve}
        metrics_df = metrics_df.append([daily_metrics], ignore_index=True)
    return metrics_df


symbol_list = get_symbol_list(2000) #grab top 2000 symbols by market cap from NYSE, NASDAQ, AMEX

#connect to the database
engine = create_engine('sqlite:///stocks.db')

#check the latest date in the current historical_prices table
sql = "SELECT MAX(Date) FROM historical_prices;"


if datetime.strptime(pd.read_sql(sql, con=engine).iloc[0, 0][:10], '%Y-%m-%d').date() < (date.today() - timedelta(days=1)): #only run if there's something to update
    start_date = (datetime.strptime(pd.read_sql(sql, con=engine).iloc[0, 0][:10], '%Y-%m-%d').date() + timedelta(days=1)).strftime('%Y-%m-%d') #set the start date to the day after the latest date
    end_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')

    price_append_df = get_historical_data(symbol_list, start_date, end_date) #grab data since last update from yfinance
    if len(price_append_df.index) > 0: #make sure there is something in the dataframe to transform/append
        price_append_df_long = hist_data_to_long_form(price_append_df) #transform dataframe to long form
        price_append_df_long.to_sql('historical_prices', con=engine, if_exists='append', index=False) #append to table in sql database

    metrics_df = get_daily_metrics(symbol_list) #retrieve daily metrics and assign to df
    metrics_df.to_sql('daily_metrics', con=engine, if_exists='replace', index=False) #replace existing
