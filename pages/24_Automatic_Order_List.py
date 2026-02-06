from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Automatic Order List')
uid = st.session_state['user']['id']
role = st.session_state['user']['role']
where = 'WHERE 1=1'; params = []
if role != 'admin':
    where += ' AND ao.user_id=?'; params.append(uid)

df = query_df(f"""
    SELECT ao.id, u.username, s.ticker, ao.side, ao.trigger_type, ao.trigger_value, ao.limit_price, ao.volume, ao.is_active, ao.status, ao.created_at, ao.approved_by, ao.approved_at, ao.notes
    FROM automatic_orders ao JOIN users u ON u.id=ao.user_id JOIN stocks s ON s.id=ao.stock_id
    {where}
    ORDER BY ao.created_at DESC
""", params)
st.dataframe(df)
