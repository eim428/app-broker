import streamlit as st
from data.db import query_df
from core.triggers import process_triggers

def require_login():
    if 'user' not in st.session_state:
        st.warning('Silakan login terlebih dahulu di halaman Login (paling atas di sidebar).')
        st.stop()

def stock_selector(label='Pilih Saham', key=None):
    df = query_df('SELECT id, ticker, name FROM stocks ORDER BY ticker')
    if df.empty:
        st.warning('Belum ada data saham')
        return None
    options = {f"{r['ticker']} - {r['name']}": int(r['id']) for _, r in df.iterrows()}
    choice = st.selectbox(label, list(options.keys()), key=key)
    return options.get(choice)

def run_triggers_once_per_page():
    key = 'triggers_ran'
    if not st.session_state.get(key):
        process_triggers()
        st.session_state[key] = True
