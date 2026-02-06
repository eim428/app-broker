from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Broker Rank')

market = st.selectbox('Pasar', ['Semua', 'Reguler', 'Tunai', 'Negosiasi'])

where = "WHERE 1=1"
params = []
if market != 'Semua':
    where += " AND t.market=?"
    params.append(market)

sql_buy = f"""
SELECT b.code AS broker,
       COUNT(*) AS frekuensi,
       SUM(t.volume) AS volume,
       SUM(t.value)  AS value
FROM trades t
JOIN brokers b ON b.id = t.broker_buy_id
{where}
GROUP BY b.code
ORDER BY frekuensi DESC
"""
df_buy = query_df(sql_buy, params)
st.subheader('Broker Buy Rank')
st.dataframe(df_buy)

sql_sell = f"""
SELECT b.code AS broker,
       COUNT(*) AS frekuensi,
       SUM(t.volume) AS volume,
       SUM(t.value)  AS value
FROM trades t
JOIN brokers b ON b.id = t.broker_sell_id
{where}
GROUP BY b.code
ORDER BY frekuensi DESC
"""
df_sell = query_df(sql_sell, params)
st.subheader('Broker Sell Rank')
st.dataframe(df_sell)
