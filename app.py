import streamlit as st
from pathlib import Path

st.set_page_config(page_title='Broker Saham Demo', layout='wide')

# Sidebar brand/logo
logo_path = Path('assets/logo.png')
if logo_path.exists():
    st.sidebar.image(str(logo_path), width='stretch')

st.sidebar.title('Broker System')
if 'user' in st.session_state:
    u = st.session_state['user']
    st.sidebar.markdown(f"Halo **{u['username']}** (role: {u['role']})")
    if st.sidebar.button('Logout'):
        st.session_state.pop('user', None)
        st.rerun()

st.title('Beranda')
st.markdown('Gunakan halaman **00_Login** di sidebar untuk masuk.')
