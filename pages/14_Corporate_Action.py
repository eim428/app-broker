from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Corporate Action')
df = query_df("""
    SELECT c.ts, s.ticker, c.action_type, c.details
    FROM corporate_actions c LEFT JOIN stocks s ON s.id=c.stock_id
    ORDER BY c.ts DESC
""")
st.dataframe(df)
