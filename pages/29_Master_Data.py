from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
from data.db import query_df, exec_sql

st.header('Master Data (Admin)')
if st.session_state['user']['role'] != 'admin':
    st.warning('Hanya untuk Admin')
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(['Brokers','Sectors','Subsectors','Stocks'])
with tab1:
    st.subheader('Brokers')
    code = st.text_input('Kode Broker')
    name = st.text_input('Nama Broker')
    if st.button('Tambah Broker') and code and name:
        exec_sql('INSERT INTO brokers (code, name) VALUES (?,?)', [code, name])
        st.success('Broker ditambah')
    st.dataframe(query_df('SELECT id, code, name FROM brokers ORDER BY code'))
with tab2:
    st.subheader('Sectors')
    sname = st.text_input('Nama Sektor')
    if st.button('Tambah Sektor') and sname:
        exec_sql('INSERT INTO sectors (name) VALUES (?)', [sname])
        st.success('Sektor ditambah')
    st.dataframe(query_df('SELECT id, name FROM sectors ORDER BY name'))
with tab3:
    st.subheader('Subsectors')
    sectors = query_df('SELECT id, name FROM sectors ORDER BY name')
    sec_map = {r['name']: int(r['id']) for _, r in sectors.iterrows()}
    subname = st.text_input('Nama Subsektor')
    par = st.selectbox('Sektor', list(sec_map.keys())) if len(sec_map)>0 else None
    if st.button('Tambah Subsektor') and par and subname:
        exec_sql('INSERT INTO subsectors (sector_id, name) VALUES (?,?)', [sec_map[par], subname])
        st.success('Subsektor ditambah')
    st.dataframe(query_df('SELECT sub.id, sec.name AS sector, sub.name FROM subsectors sub JOIN sectors sec ON sec.id=sub.sector_id ORDER BY sec.name, sub.name'))
with tab4:
    st.subheader('Stocks')
    ticker = st.text_input('Ticker')
    nm = st.text_input('Nama')
    sectors = query_df('SELECT id, name FROM sectors ORDER BY name')
    subs = query_df('SELECT id, name FROM subsectors ORDER BY name')
    sec_map = {r['name']: int(r['id']) for _, r in sectors.iterrows()}
    sub_map = {r['name']: int(r['id']) for _, r in subs.iterrows()}
    sec_sel = st.selectbox('Sektor_Utama', list(sec_map.keys())) if len(sec_map)>0 else None
    sub_sel = st.selectbox('Subsektor', list(sub_map.keys())) if len(sub_map)>0 else None
    prev = st.number_input('Prev Close', value=1000.0)
    lot = st.number_input('Lot Size', value=100)
    if st.button('Tambah Saham') and ticker and nm and sec_sel and sub_sel:
        exec_sql(
            'INSERT INTO stocks (ticker, name, sector_id, subsector_id, lot_size, price_prev_close, market_cap, free_float) VALUES (?,?,?,?,?,?,?,?)',
            [ticker, nm, sec_map[sec_sel], sub_map[sub_sel], int(lot), float(prev), float(prev*1_000_000), 0.5]
        )
        st.success('Saham ditambah')
    st.dataframe(query_df('SELECT s.id, s.ticker, s.name, sec.name AS sector, sub.name AS subsector, s.price_prev_close FROM stocks s LEFT JOIN sectors sec ON sec.id=s.sector_id LEFT JOIN subsectors sub ON sub.id=s.subsector_id ORDER BY s.ticker'))
