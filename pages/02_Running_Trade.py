from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Running Trade (Done)')
limit = st.slider('Jumlah baris', 20, 300, 50)
df = query_df("""
    SELECT t.ts, s.ticker, t.price, t.volume, t.value,
           b1.code AS broker_buy, b2.code AS broker_sell, t.market
    FROM trades t
    JOIN stocks s ON s.id=t.stock_id
    JOIN brokers b1 ON b1.id=t.broker_buy_id
    JOIN brokers b2 ON b2.id=t.broker_sell_id
    WHERE t.status='Done'
    ORDER BY t.ts DESC
    LIMIT ?
""", [limit])
st.dataframe(df)
