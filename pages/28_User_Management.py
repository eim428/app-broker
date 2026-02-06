from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from datetime import datetime
import hashlib, os
from data.db import query_df, exec_sql

st.header('User Management (Admin)')
if st.session_state['user']['role'] != 'admin':
    st.warning('Hanya untuk Admin')
    st.stop()

st.subheader('Tambah User')
with st.form('add_user_form'):
    uname = st.text_input('Username Baru')
    pwd = st.text_input('Password', type='password')
    role = st.selectbox('Role', ['user','admin'])
    submitted = st.form_submit_button('Tambah')
if submitted and uname and pwd:
    salt = os.urandom(16).hex()
    pwd_hash = hashlib.pbkdf2_hmac('sha256', pwd.encode('utf-8'), bytes.fromhex(salt), 100000).hex()
    try:
        exec_sql('INSERT INTO users (username, password_hash, salt, role, is_active, created_at) VALUES (?,?,?,?,?,datetime("now"))', [uname, pwd_hash, salt, role, 1])
        st.success('User dibuat')
    except Exception as e:
        st.error(f'Gagal: {e}')

st.subheader('Daftar User')
st.dataframe(query_df('SELECT id, username, role, is_active, created_at FROM users ORDER BY id'))
