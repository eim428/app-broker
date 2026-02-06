from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st

st.header('e-IPO')
st.info('Untuk pemesanan saham IPO, silakan gunakan kanal e-IPO resmi.')
st.markdown('[Kunjungi e-IPO](https://e-ipo.co.id)', unsafe_allow_html=True)
