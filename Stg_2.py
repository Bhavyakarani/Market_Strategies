import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
import streamlit as st
from datetime import date
from datetime import timedelta
def Stocks(company):

    date1 = date.today() 
    date2 = date1 - timedelta(days=1000)
    data = yf.download(company, date2 , date1)
    spt = ta.supertrend(data['High'], data['Low'], data['Close'],10 , 3)
    spt = spt.filter(['Date','Close', 'SUPERTd_10_3.0'])    
    spt['Indicator'] = spt['SUPERTd_10_3.0'].diff()
    df_pos = spt[(spt['Indicator'] == 2) | (spt['Indicator'] == -2)]
    df_pos['Indicator'] = df_pos['Indicator'].apply(lambda x: 'Buy' if x == 2 else  'Sell')
    df_pos = df_pos.filter(['Date','Indicator'])
    st.dataframe(df_pos)
Stocks("RELIANCE.NS")
