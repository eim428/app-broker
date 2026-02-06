import streamlit as st
from core.auth import verify_password, get_active_user

st.title('Login')
with st.form('login_form'):
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    submitted = st.form_submit_button('Login')

if submitted:
    row = get_active_user(username)
    if row is None:
        st.error('User tidak ditemukan atau tidak aktif')
    else:
        if verify_password(password, row['password_hash'], row['salt']):
            st.session_state['user'] = {'id': int(row['id']), 'username': row['username'], 'role': row['role']}
            st.success('Berhasil login')
            st.rerun()
        else:
            st.error('Password salah')
