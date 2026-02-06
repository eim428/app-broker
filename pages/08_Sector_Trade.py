from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Sector Trade')
df = query_df("""
    SELECT st.ts, s.name AS sector, st.volume, st.value, st.frequency
    FROM sector_trade_summary st JOIN sectors s ON s.id=st.sector_id
    ORDER BY st.value DESC
""")
st.dataframe(df)
