from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Market Summary')
st.dataframe(query_df('SELECT ts, market, instrument_type, volume, value, frequency FROM market_summary ORDER BY market, instrument_type'))
