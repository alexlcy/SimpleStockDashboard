import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

CURRENT_PROFILE = ['AMD', 'BABA', 'VOO']

def get_stock(stock_name):
    stock_ticker = yf.Ticker(stock_name)
    # get historical market data
    hist = stock_ticker.history(period="max")
    price = pd.DataFrame(hist['Close'])
    return stock_ticker, price

def get_moving_average(price_series):
    price_series['100 Day Rolling'] = price_series['Close'].rolling(100).mean()
    price_series['30 Day Rolling'] = price_series['Close'].rolling(30).mean()
    return price_series

def get_native_decision(price_series, cur_value):
    rolling_200 = price_series['Close'].rolling(200).mean()[-1]
    if cur_value > rolling_200 * 1.05:
        return 'Buy'
    elif cur_value < rolling_200 * 0.95:
        return 'Sell'
    else:
        return "Hold"

st.title('Alex Stock Dashboard')

for stock in CURRENT_PROFILE:
    stock_ticker, price = get_stock(stock)
    cur_value = stock_ticker.info["previousClose"]
    st.subheader(f"Stock Name: {stock_ticker.info['longName']}")
    action = get_native_decision(price, cur_value)
    rolling_df = get_moving_average(price)
    st.line_chart(rolling_df[-365:])
    st.write(f"Current Value:", cur_value)
    st.write(f"P/E Value:", stock_ticker.info['trailingPE'])
    st.text(f"Suggested Action based on Moving Average: {action}")
    #st.write("Information", stock_ticker.info)
    if stock_ticker.recommendations is not None:
        st.write("Recommendations", stock_ticker.recommendations.iloc[-10:])