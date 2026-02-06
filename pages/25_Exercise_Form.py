from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from datetime import datetime
from data.db import exec_sql
from core.utils import stock_selector

st.header('Exercise Form (Rights Issue/HMETD)')
uid = st.session_state['user']['id']
sid = stock_selector('Saham (HMETD)')
rights_code = st.text_input('Kode Rights')
qty = st.number_input('Kuantitas', min_value=1, value=100)
if st.button('Ajukan (Pending Approval)') and sid and rights_code:
    exec_sql(
        'INSERT INTO exercises (user_id, stock_id, rights_code, quantity, status, created_at) VALUES (?,?,?,?,?,?)',
        [uid, sid, rights_code, int(qty), 'PendingApproval', datetime.utcnow().isoformat()]
    )
    st.success('Pengajuan exercise dikirim')
