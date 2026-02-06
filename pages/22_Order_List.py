from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Order List (Hari Ini)')
uid = st.session_state['user']['id']
role = st.session_state['user']['role']
where = 'WHERE date(o.created_at)=date("now")'; params = []
if role != 'admin':
    where += ' AND o.user_id=?'; params.append(uid)

df = query_df(f"""
    SELECT o.id, u.username, s.ticker, o.side, o.price, o.volume, o.status, o.created_at, o.approved_by, o.approved_at, o.notes
    FROM orders o JOIN users u ON u.id=o.user_id JOIN stocks s ON s.id=o.stock_id
    {where}
    ORDER BY o.created_at DESC
""", params)
st.dataframe(df)
