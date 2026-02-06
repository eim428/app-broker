from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
import pandas as pd
from data.db import query_df
from core.utils import stock_selector

st.header('Chart')
sid = stock_selector('Pilih Saham', key='chart')
if sid:
    period = st.selectbox('Periode', ['1M','3M','6M','All'])
    ind_sma5 = st.checkbox('SMA 5', value=True)
    ind_sma20 = st.checkbox('SMA 20', value=True)
    ind_sma60 = st.checkbox('SMA 60', value=False)
    df = query_df('SELECT ts, price, volume FROM prices WHERE stock_id=? ORDER BY ts', [sid])
    df['ts'] = pd.to_datetime(df['ts'])
    if not df.empty:
        if period == '1M':
            df = df[df['ts'] >= (df['ts'].max() - pd.DateOffset(months=1))]
        elif period == '3M':
            df = df[df['ts'] >= (df['ts'].max() - pd.DateOffset(months=3))]
        elif period == '6M':
            df = df[df['ts'] >= (df['ts'].max() - pd.DateOffset(months=6))]
    chart_df = df[['ts','price']].set_index('ts')
    if ind_sma5:
        chart_df['SMA5'] = chart_df['price'].rolling(5).mean()
    if ind_sma20:
        chart_df['SMA20'] = chart_df['price'].rolling(20).mean()
    if ind_sma60:
        chart_df['SMA60'] = chart_df['price'].rolling(60).mean()
    st.line_chart(chart_df)
