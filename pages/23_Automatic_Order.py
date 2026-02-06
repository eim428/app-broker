from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from datetime import datetime
from data.db import exec_sql
from core.utils import stock_selector

st.header('Automatic Order (Trigger)')
uid = st.session_state['user']['id']
sid = stock_selector('Saham (Trigger)')
trig_type = st.selectbox('Tipe Trigger', ['price_above','price_below'])
trig_val = st.number_input('Nilai Trigger (Harga)')
side = st.selectbox('Side', ['Buy','Sell'])
limit_price = st.number_input('Limit Price', value=trig_val)
lot = st.number_input('Jumlah Lot', min_value=1, value=1)
if st.button('Simpan (Pending Approval)') and sid:
    exec_sql(
        'INSERT INTO automatic_orders (user_id, stock_id, side, trigger_type, trigger_value, limit_price, volume, is_active, status, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)',
        [uid, sid, side, trig_type, float(trig_val), float(limit_price), int(lot*100), 1, 'PendingApproval', datetime.utcnow().isoformat()]
    )
    st.success('Automatic order disimpan dan menunggu persetujuan')
