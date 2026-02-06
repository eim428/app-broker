from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Screener')
min_price, max_price = st.slider('Last Price (Rp)', 0, 20000, (0, 20000), step=50)
min_mcap = st.number_input('Min Market Cap', value=0)
min_gain = st.number_input('Min Gain (%)', value=-100)
max_gain = st.number_input('Max Gain (%)', value=100)

df = query_df("""
    SELECT s.ticker, s.name, s.market_cap, s.price_prev_close AS prev_close,
           (SELECT price FROM prices p WHERE p.stock_id=s.id ORDER BY ts DESC LIMIT 1) AS last_price
    FROM stocks s
""")

df['gain_pct'] = ((df['last_price']-df['prev_close'])/df['prev_close']*100).round(2)
mask = (
    (df['last_price']>=min_price) & (df['last_price']<=max_price) &
    (df['market_cap']>=min_mcap) &
    (df['gain_pct']>=min_gain) & (df['gain_pct']<=max_gain)
)

st.dataframe(df[mask])
