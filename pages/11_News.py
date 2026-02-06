from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('News')
st.dataframe(query_df('SELECT ts, source, title, url FROM news ORDER BY ts DESC'))
