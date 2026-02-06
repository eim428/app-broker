from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df

st.header('Stock List')
sec = query_df('SELECT id, name FROM sectors ORDER BY name')
sec_map = {r['name']: int(r['id']) for _, r in sec.iterrows()}
sub = query_df('SELECT id, name FROM subsectors ORDER BY name')
sub_map = {r['name']: int(r['id']) for _, r in sub.iterrows()}
idx = query_df('SELECT id, code FROM indices ORDER BY code')
idx_map = {r['code']: int(r['id']) for _, r in idx.iterrows()}

chosen_sec = st.multiselect('Sektor', list(sec_map.keys()))
chosen_sub = st.multiselect('Subsektor', list(sub_map.keys()))
chosen_idx = st.multiselect('Index Constituents', list(idx_map.keys()))

where = 'WHERE 1=1'; params = []
if chosen_sec:
    placeholders = ','.join('?'*len(chosen_sec))
    ids = [sec_map[x] for x in chosen_sec]
    where += f' AND sector_id IN ({placeholders})'
    params += ids
if chosen_sub:
    placeholders = ','.join('?'*len(chosen_sub))
    ids = [sub_map[x] for x in chosen_sub]
    where += f' AND subsector_id IN ({placeholders})'
    params += ids

base = query_df(f"""
    SELECT s.id, s.ticker, s.name, s.security_type, s.pre_opening, s.notation,
           s.price_prev_close,
           (SELECT price FROM prices p WHERE p.stock_id=s.id ORDER BY ts DESC LIMIT 1) AS last_price
    FROM stocks s {where} ORDER BY s.ticker
""", params)

if chosen_idx:
    placeholders = ','.join('?'*len(chosen_idx))
    ids = [idx_map[x] for x in chosen_idx]
    idx_df = query_df(f"""
        SELECT stock_id FROM stock_index_membership WHERE index_id IN ({placeholders})
    """, ids)
    base = base[base['id'].isin(idx_df['stock_id'])]

st.dataframe(base.drop(columns=['id']))
