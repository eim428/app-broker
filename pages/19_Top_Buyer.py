from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Top Buyer / Seller')
inv = st.selectbox('Investor', ['Asing','Domestik'])
df = query_df("""
    SELECT s.ticker,
           SUM(CASE WHEN t.investor_type=? THEN t.value ELSE 0 END) AS value_by_inv
    FROM trades t JOIN stocks s ON s.id=t.stock_id
    GROUP BY s.ticker
    ORDER BY value_by_inv DESC
    LIMIT 50
""", [inv])
st.dataframe(df)
