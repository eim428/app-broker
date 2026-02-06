from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from datetime import datetime
from data.db import query_df, exec_sql
from core.utils import stock_selector

st.header('Buy')
uid = st.session_state['user']['id']
sid = stock_selector('Saham')
if sid:
    last = query_df('SELECT price FROM prices WHERE stock_id=? ORDER BY ts DESC LIMIT 1', [sid])
    last_price = float(last.iloc[0]['price']) if not last.empty else 0
    price = st.number_input('Harga (Rp)', value=float(last_price))
    lot = st.number_input('Jumlah Lot', min_value=1, value=1)
    volume = int(lot)*100
    st.caption(f'Volume saham = {volume} saham')
    if st.button('Kirim Order (Pending Approval)'):
        exec_sql(
            'INSERT INTO orders (user_id, side, stock_id, price, volume, status, created_at) VALUES (?,?,?,?,?,?,?)',
            [uid, 'Buy', sid, float(price), int(volume), 'PendingApproval', datetime.utcnow().isoformat()]
        )
        st.success('Order dikirim untuk persetujuan')
