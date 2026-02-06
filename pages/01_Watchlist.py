from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from datetime import datetime
from data.db import query_df, exec_sql
from core.utils import stock_selector

st.header('Watchlist')
uid = st.session_state['user']['id']
sid = stock_selector('Tambah ke Watchlist', key='wl_add')
if sid and st.button('Tambah'):
    exec_sql('INSERT OR IGNORE INTO watchlists (user_id, stock_id, created_at) VALUES (?,?,?)', [uid, sid, datetime.utcnow().isoformat()])
    st.success('Ditambahkan ke watchlist')

df = query_df("""
    SELECT s.ticker, s.name, s.price_prev_close AS prev_close,
           (SELECT price FROM prices p WHERE p.stock_id=s.id ORDER BY ts DESC LIMIT 1) AS last_price
    FROM watchlists w JOIN stocks s ON s.id=w.stock_id
    WHERE w.user_id=? ORDER BY s.ticker
""", [uid])

if df.empty:
    st.info('Watchlist kosong')
else:
    df['Delta (Rp)'] = (df['last_price'] - df['prev_close']).round(2)
    df['Delta (%)'] = ((df['last_price'] - df['prev_close'])/df['prev_close']*100).round(2)
    st.dataframe(df)
    remove = st.multiselect('Hapus dari watchlist', df['ticker'].tolist())
    if remove and st.button('Hapus terpilih'):
        placeholders = ','.join('?'*len(remove))
        exec_sql(f'DELETE FROM watchlists WHERE user_id=? AND stock_id IN (SELECT id FROM stocks WHERE ticker IN ({placeholders}))', [uid, *remove])
        st.success('Dihapus')
        st.rerun()
