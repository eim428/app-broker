import numpy as np
import pandas as pd
from data.db import query_df

def compute_fin_metrics_df(year=None):
    base = query_df("""
        SELECT s.id AS stock_id, s.ticker, s.name,
               s.market_cap,
               s.price_prev_close,
               (SELECT price FROM prices p WHERE p.stock_id=s.id ORDER BY ts DESC LIMIT 1) AS last_price
        FROM stocks s
    """)
    if year is None:
        fdf = query_df("""
            SELECT f.* FROM fundamentals f
            JOIN (
                SELECT stock_id, MAX(year) AS maxy FROM fundamentals GROUP BY stock_id
            ) x ON x.stock_id=f.stock_id AND x.maxy=f.year
        """)
    else:
        fdf = query_df('SELECT * FROM fundamentals WHERE year=?', [int(year)])
    if fdf.empty:
        return None

    df = pd.merge(base, fdf, on='stock_id', how='inner')
    df['price'] = df['last_price']
    df['pe'] = np.where(df['eps']!=0, df['price']/df['eps'], np.nan)
    df['pb'] = np.where((df['eps']!=0) & (df['roe']>0), (df['price']*df['roe'])/df['eps'], np.nan)
    df['div_yield'] = np.where(df['price']>0, df['dividend']/df['price'], np.nan)
    df['net_margin'] = np.where(df['revenue']!=0, df['net_income']/df['revenue'], np.nan)
    cols = ['ticker','name','year','price','market_cap','eps','pe','pb','dividend','div_yield','roa','roe','debt_to_equity','net_margin']
    return df[cols].copy()
