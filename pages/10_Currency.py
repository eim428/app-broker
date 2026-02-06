from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Currency')
st.dataframe(query_df('SELECT code, name, rate_to_idr, ts FROM currencies ORDER BY code'))
