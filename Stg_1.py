import yfinance as yf
import pandas as pd
import talib as ta
import numpy as np 
from datetime import date, timedelta
import streamlit as st


def Stocks(company):

    date1 = date.today()
    date2 = date1 - timedelta(days=1000)        
    data = yf.download(company, date2 , date1)
    data = data.filter(['Date', 'Close'])
    data['EMA9'] = ta.EMA(data['Close'], timeperiod = 9)
    data['EMA26'] = ta.EMA(data['Close'], timeperiod = 26)
    data['Closecum'] = data['Close'].cummax()
    data['Stop'] = (data['Closecum'] - (0.05 * data['Closecum']))
    data['Signal'] = 0.0
    data['Signal1'] = 0.0
    data['Signal'] = np.where(data['EMA9'] > data['EMA26'], 1.0, 0.0) 
    data['Signal1'] = np.where(data['Close'] < data['Stop'], 1.0, 0.0)
    data['Indicator'] = data['Signal'].diff()
    data['SLindicator'] = data['Signal1'].diff()
    call = data[((data['Indicator'] == 1) | (data['Indicator'] == -1))]
    call['Indicator'] = call['Indicator'].apply(lambda x: 'Buy' if x == 1 else 'Sell')
    call = call.filter(['Date','Indicator'])
    call1= data[(data['SLindicator'] == 1)]
    call1['SLindicator'] = call1['SLindicator'].apply(lambda x: 'Sell' if x == 1 else 'Not')
    call1 = call1.filter(['Date', 'SLindicator'])
    call2 = pd.concat([call, call1], axis=1)
    call2.fillna(value = ".",inplace = True)
    st.dataframe(call2)
       
Stocks("RELIANCE.NS")
