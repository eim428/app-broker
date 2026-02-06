from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df
from core.utils import stock_selector

st.header('Fundamental (5 tahun)')
sid = stock_selector('Pilih Saham', key='fund')
if sid:
    df = query_df('SELECT year, revenue, net_income, eps, roa, roe, debt_to_equity, dividend FROM fundamentals WHERE stock_id=? ORDER BY year DESC', [sid])
    st.dataframe(df)
