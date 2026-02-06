from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df
from core.utils import stock_selector

st.header('Order Book (5-level)')
sid = stock_selector('Pilih Saham', key='ob')
if sid:
    df_bid = query_df('SELECT level, price, lot, orders_count FROM orderbook_levels WHERE stock_id=? AND side="bid" ORDER BY level', [sid])
    df_ask = query_df('SELECT level, price, lot, orders_count FROM orderbook_levels WHERE stock_id=? AND side="ask" ORDER BY level', [sid])
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Bid'); st.dataframe(df_bid)
    with col2:
        st.subheader('Ask'); st.dataframe(df_ask)
