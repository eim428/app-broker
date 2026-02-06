from core.utils import require_login, run_triggers_once_per_page
require_login()
run_triggers_once_per_page()

import streamlit as st
import pandas as pd
from core.metrics import compute_fin_metrics_df
from core.utils import stock_selector
from data.db import query_df

st.header('Financial Metrics')

st.subheader('Per Saham (Detail)')
sid = stock_selector('Pilih Saham', key='fm_stock')
year_mode = st.radio('Pilih Tahun', ['Latest','Pilih Tahun'])
chosen_year = None
if year_mode == 'Pilih Tahun':
    years_df = query_df('SELECT DISTINCT year FROM fundamentals ORDER BY year DESC')
    if not years_df.empty:
        chosen_year = st.selectbox('Tahun', years_df['year'].tolist())

df_all = compute_fin_metrics_df(year=chosen_year)
if df_all is None:
    st.info('Belum ada data fundamentals untuk menghitung metrics.')
else:
    if sid:
        tkr = query_df('SELECT ticker FROM stocks WHERE id=?', [sid]).iloc[0]['ticker']
        row = df_all[df_all['ticker']==tkr]
        if row.empty:
            st.warning('Data fundamentals untuk saham ini tidak tersedia.')
        else:
            r = row.iloc[0]
            c1,c2,c3,c4 = st.columns(4)
            c1.metric('Harga (Rp)', f"{r['price']:.2f}")
            c2.metric('P/E', f"{r['pe']:.2f}" if pd.notna(r['pe']) else '-')
            c3.metric('P/B', f"{r['pb']:.2f}" if pd.notna(r['pb']) else '-')
            c4.metric('Dividend Yield', f"{r['div_yield']*100:.2f}%" if pd.notna(r['div_yield']) else '-')
            d1,d2,d3,d4 = st.columns(4)
            d1.metric('ROA', f"{r['roa']*100:.2f}%" if pd.notna(r['roa']) else '-')
            d2.metric('ROE', f"{r['roe']*100:.2f}%" if pd.notna(r['roe']) else '-')
            d3.metric('Debt/Equity', f"{r['debt_to_equity']:.2f}" if pd.notna(r['debt_to_equity']) else '-')
            d4.metric('Net Margin', f"{r['net_margin']*100:.2f}%" if pd.notna(r['net_margin']) else '-')
            st.caption('Catatan: P/B dihitung dengan pendekatan BVPS ≈ EPS/ROE (estimasi).')

    st.divider()
    st.subheader('Screener Metrics (Seluruh Saham)')
    colf1, colf2, colf3, colf4 = st.columns(4)
    with colf1:
        pe_max = st.number_input('Maks P/E', min_value=0.0, value=50.0)
        pb_max = st.number_input('Maks P/B', min_value=0.0, value=10.0)
    with colf2:
        roe_min = st.number_input('Min ROE (%)', min_value=0.0, value=10.0)
        roa_min = st.number_input('Min ROA (%)', min_value=0.0, value=5.0)
    with colf3:
        dy_min = st.number_input('Min Div Yield (%)', min_value=0.0, value=0.0)
        nm_min = st.number_input('Min Net Margin (%)', min_value=-100.0, value=0.0)
    with colf4:
        de_max = st.number_input('Maks Debt/Equity', min_value=0.0, value=2.0)

    df_screen = df_all.copy()
    df_screen = df_screen[
        (df_screen['pe'].isna() | (df_screen['pe'] <= pe_max)) &
        (df_screen['pb'].isna() | (df_screen['pb'] <= pb_max)) &
        (df_screen['roe'].isna() | (df_screen['roe']*100 >= roe_min)) &
        (df_screen['roa'].isna() | (df_screen['roa']*100 >= roa_min)) &
        (df_screen['div_yield'].isna() | (df_screen['div_yield']*100 >= dy_min)) &
        (df_screen['net_margin'].isna() | (df_screen['net_margin']*100 >= nm_min)) &
        (df_screen['debt_to_equity'].isna() | (df_screen['debt_to_equity'] <= de_max))
    ]
    df_screen = df_screen.sort_values(['roe','div_yield'], ascending=[False, False])
    show = df_screen.copy()
    show['ROE (%)'] = (show['roe']*100).round(2)
    show['ROA (%)'] = (show['roa']*100).round(2)
    show['DY (%)'] = (show['div_yield']*100).round(2)
    show['Net Margin (%)'] = (show['net_margin']*100).round(2)
    st.dataframe(show[
        ['ticker','name','year','price','eps','pe','pb','DY (%)','ROE (%)','ROA (%)','debt_to_equity','Net Margin (%)']
    ].reset_index(drop=True))
