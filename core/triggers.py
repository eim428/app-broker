from datetime import datetime
from data.db import query_df, exec_sql

def process_triggers():
    aodf = query_df("""
        SELECT ao.*, s.ticker,
               (SELECT price FROM prices p WHERE p.stock_id=ao.stock_id ORDER BY ts DESC LIMIT 1) AS last_price
        FROM automatic_orders ao JOIN stocks s ON s.id=ao.stock_id
        WHERE ao.is_active=1 AND ao.status='Approved'
    """)
    for _, row in aodf.iterrows():
        cond = False
        lp = row['last_price']
        if row['trigger_type'] == 'price_above':
            cond = lp is not None and lp >= row['trigger_value']
        elif row['trigger_type'] == 'price_below':
            cond = lp is not None and lp <= row['trigger_value']
        elif row['trigger_type'] == 'time':
            try:
                cond = datetime.utcnow() >= datetime.fromisoformat(str(row['trigger_value']))
            except Exception:
                cond = False
        if cond:
            note_ref = f"AO#{row['id']} triggered at {datetime.utcnow().isoformat()}"
            exec_sql(
                'INSERT INTO orders (user_id, side, stock_id, price, volume, status, created_at, notes) VALUES (?,?,?,?,?,?,?,?)',
                [int(row['user_id']), row['side'], int(row['stock_id']), float(row['limit_price']), int(row['volume']), 'PendingApproval', datetime.utcnow().isoformat(), note_ref]
            )
            exec_sql('UPDATE automatic_orders SET is_active=0, notes=? WHERE id=?', [note_ref, int(row['id'])])
