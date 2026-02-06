from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Stock Rank')
by = st.selectbox('Urutkan berdasarkan', ['Gain (Rp)','Gain (%)','Loss (Rp)','Loss (%)','Volume','Value','Frekuensi'])
base = query_df("""
    SELECT s.id, s.ticker, s.name, s.price_prev_close AS prev_close,
           (SELECT price FROM prices p WHERE p.stock_id=s.id ORDER BY ts DESC LIMIT 1) AS last_price,
           (SELECT SUM(t.volume) FROM trades t WHERE t.stock_id=s.id) AS volume,
           (SELECT SUM(t.value) FROM trades t WHERE t.stock_id=s.id) AS value,
           (SELECT COUNT(1) FROM trades t WHERE t.stock_id=s.id) AS freq
    FROM stocks s
""")
base['chg'] = (base['last_price'] - base['prev_close']).round(2)
base['chg_pct'] = (base['chg'] / base['prev_close'] * 100).round(2)
if by == 'Gain (Rp)':
    df = base.sort_values('chg', ascending=False)
elif by == 'Gain (%)':
    df = base.sort_values('chg_pct', ascending=False)
elif by == 'Loss (Rp)':
    df = base.sort_values('chg', ascending=True)
elif by == 'Loss (%)':
    df = base.sort_values('chg_pct', ascending=True)
elif by == 'Volume':
    df = base.sort_values('volume', ascending=False)
elif by == 'Value':
    df = base.sort_values('value', ascending=False)
else:
    df = base.sort_values('freq', ascending=False)

st.dataframe(df[['ticker','name','prev_close','last_price','chg','chg_pct','volume','value','freq']].head(50))
