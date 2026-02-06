from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
import numpy as np
import pandas as pd
from data.db import query_df

st.header('Indices')
idx = query_df('SELECT id, code, name FROM indices')
out = []
for _, r in idx.iterrows():
    members = query_df("""
        SELECT s.id, s.price_prev_close AS prev_close,
               (SELECT price FROM prices p WHERE p.stock_id=s.id ORDER BY ts DESC LIMIT 1) AS last_price
        FROM stock_index_membership m JOIN stocks s ON s.id=m.stock_id
        WHERE m.index_id=?
    """, [int(r['id'])])
    if members.empty:
        level = np.nan; chg = np.nan; chg_pct = np.nan
    else:
        prev_sum = members['prev_close'].sum()
        last_sum = members['last_price'].sum()
        level = (last_sum/prev_sum)*100 if prev_sum>0 else np.nan
        chg = last_sum - prev_sum
        chg_pct = (chg/prev_sum*100) if prev_sum>0 else np.nan
    out.append({'code': r['code'], 'name': r['name'], 'level': round(level,2) if level==level else None, 'Delta (Rp)': round(chg,2) if chg==chg else None, 'Delta (%)': round(chg_pct,2) if chg_pct==chg_pct else None})

st.dataframe(pd.DataFrame(out))
