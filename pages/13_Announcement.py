from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Announcement')
st.dataframe(query_df('SELECT ts, category, title, content FROM announcements ORDER BY ts DESC'))
