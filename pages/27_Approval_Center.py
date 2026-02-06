from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from datetime import datetime
from data.db import query_df, exec_sql

st.header('Approval Center (Admin)')
if st.session_state['user']['role'] != 'admin':
    st.warning('Hanya untuk Admin')
    st.stop()

tab1, tab2, tab3 = st.tabs(['Orders','Automatic Orders','Exercises'])
with tab1:
    df = query_df("""
        SELECT o.id, u.username, s.ticker, o.side, o.price, o.volume, o.status, o.created_at
        FROM orders o JOIN users u ON u.id=o.user_id JOIN stocks s ON s.id=o.stock_id
        WHERE o.status='PendingApproval' ORDER BY o.created_at ASC
    """)
    st.dataframe(df)
    oid = st.number_input('Order ID untuk approve/reject', min_value=0, value=0, step=1)
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Approve Order') and oid>0:
            exec_sql('UPDATE orders SET status="Approved", approved_by=?, approved_at=? WHERE id=?', [st.session_state['user']['id'], datetime.utcnow().isoformat(), int(oid)])
            st.success('Order di-approve')
    with col2:
        if st.button('Reject Order') and oid>0:
            exec_sql('UPDATE orders SET status="Rejected", approved_by=?, approved_at=? WHERE id=?', [st.session_state['user']['id'], datetime.utcnow().isoformat(), int(oid)])
            st.warning('Order di-reject')
with tab2:
    df = query_df("""
        SELECT ao.id, u.username, s.ticker, ao.side, ao.trigger_type, ao.trigger_value, ao.limit_price, ao.volume, ao.status, ao.created_at
        FROM automatic_orders ao JOIN users u ON u.id=ao.user_id JOIN stocks s ON s.id=ao.stock_id
        WHERE ao.status='PendingApproval' ORDER BY ao.created_at ASC
    """)
    st.dataframe(df)
    aoid = st.number_input('Automatic Order ID', min_value=0, value=0, step=1)
    c1, c2 = st.columns(2)
    with c1:
        if st.button('Approve AO') and aoid>0:
            exec_sql('UPDATE automatic_orders SET status="Approved", approved_by=?, approved_at=? WHERE id=?', [st.session_state['user']['id'], datetime.utcnow().isoformat(), int(aoid)])
            st.success('Automatic order di-approve')
    with c2:
        if st.button('Reject AO') and aoid>0:
            exec_sql('UPDATE automatic_orders SET status="Rejected", approved_by=?, approved_at=? WHERE id=?', [st.session_state['user']['id'], datetime.utcnow().isoformat(), int(aoid)])
            st.warning('Automatic order di-reject')
with tab3:
    df = query_df("""
        SELECT e.id, u.username, s.ticker, e.rights_code, e.quantity, e.status, e.created_at
        FROM exercises e JOIN users u ON u.id=e.user_id JOIN stocks s ON s.id=e.stock_id
        WHERE e.status='PendingApproval' ORDER BY e.created_at ASC
    """)
    st.dataframe(df)
    eid = st.number_input('Exercise ID', min_value=0, value=0, step=1)
    d1, d2 = st.columns(2)
    with d1:
        if st.button('Approve Exercise') and eid>0:
            exec_sql('UPDATE exercises SET status="Approved", approved_by=?, approved_at=? WHERE id=?', [st.session_state['user']['id'], datetime.utcnow().isoformat(), int(eid)])
            st.success('Exercise di-approve')
    with d2:
        if st.button('Reject Exercise') and eid>0:
            exec_sql('UPDATE exercises SET status="Rejected", approved_by=?, approved_at=? WHERE id=?', [st.session_state['user']['id'], datetime.utcnow().isoformat(), int(eid)])
            st.warning('Exercise di-reject')
