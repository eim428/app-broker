# --- seed_db.py with triple-double quoted SQL blocks ---

import os, sqlite3, hashlib
from datetime import datetime, timedelta
from config.settings import DB_PATH

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Drop tables if exist
for t in [
    'users','brokers','sectors','subsectors','stocks','indices','stock_index_membership',
    'prices','trades','orderbook_levels','fundamentals','market_summary','sector_trade_summary',
    'currencies','news','research','announcements','corporate_actions','watchlists','orders',
    'automatic_orders','exercises']:
    cur.execute(f"DROP TABLE IF EXISTS {t}")

# Schema (use triple-double quotes to avoid nesting issues)
cur.execute("""
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE,
  password_hash TEXT,
  salt TEXT,
  role TEXT,
  is_active INTEGER DEFAULT 1,
  created_at TEXT
)
""")

cur.execute("""
CREATE TABLE brokers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT UNIQUE,
  name TEXT
)
""")

cur.execute("""
CREATE TABLE sectors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT UNIQUE
)
""")

cur.execute("""
CREATE TABLE subsectors (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  sector_id INTEGER,
  name TEXT,
  FOREIGN KEY(sector_id) REFERENCES sectors(id)
)
""")

cur.execute("""
CREATE TABLE stocks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ticker TEXT UNIQUE,
  name TEXT,
  sector_id INTEGER,
  subsector_id INTEGER,
  lot_size INTEGER,
  price_prev_close REAL,
  market_cap REAL,
  free_float REAL,
  security_type TEXT DEFAULT 'Stock',
  pre_opening INTEGER DEFAULT 0,
  notation TEXT DEFAULT '',
  FOREIGN KEY(sector_id) REFERENCES sectors(id),
  FOREIGN KEY(subsector_id) REFERENCES subsectors(id)
)
""")

cur.execute("""
CREATE TABLE indices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT UNIQUE,
  name TEXT
)
""")

cur.execute("""
CREATE TABLE stock_index_membership (
  index_id INTEGER,
  stock_id INTEGER,
  PRIMARY KEY(index_id, stock_id)
)
""")

cur.execute("""
CREATE TABLE prices (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  stock_id INTEGER,
  ts TEXT,
  price REAL,
  volume INTEGER
)
""")

cur.execute("""
CREATE TABLE trades (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT,
  stock_id INTEGER,
  price REAL,
  volume INTEGER,
  value REAL,
  broker_buy_id INTEGER,
  broker_sell_id INTEGER,
  market TEXT,
  status TEXT,
  investor_type TEXT
)
""")

cur.execute("""
CREATE TABLE orderbook_levels (
  stock_id INTEGER,
  side TEXT,
  level INTEGER,
  price REAL,
  lot INTEGER,
  orders_count INTEGER,
  PRIMARY KEY(stock_id, side, level)
)
""")

cur.execute("""
CREATE TABLE fundamentals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  stock_id INTEGER,
  year INTEGER,
  revenue REAL,
  net_income REAL,
  eps REAL,
  roa REAL,
  roe REAL,
  debt_to_equity REAL,
  dividend REAL
)
""")

cur.execute("""
CREATE TABLE market_summary (
  ts TEXT,
  market TEXT,
  instrument_type TEXT,
  volume INTEGER,
  value REAL,
  frequency INTEGER
)
""")

cur.execute("""
CREATE TABLE sector_trade_summary (
  ts TEXT,
  sector_id INTEGER,
  volume INTEGER,
  value REAL,
  frequency INTEGER
)
""")

cur.execute("""
CREATE TABLE currencies (
  code TEXT PRIMARY KEY,
  name TEXT,
  rate_to_idr REAL,
  ts TEXT
)
""")

cur.execute("""
CREATE TABLE news (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT,
  source TEXT,
  title TEXT,
  url TEXT
)
""")

cur.execute("""
CREATE TABLE research (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT,
  title TEXT,
  summary TEXT
)
""")

cur.execute("""
CREATE TABLE announcements (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT,
  category TEXT,
  title TEXT,
  content TEXT
)
""")

cur.execute("""
CREATE TABLE corporate_actions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts TEXT,
  stock_id INTEGER,
  action_type TEXT,
  details TEXT
)
""")

cur.execute("""
CREATE TABLE watchlists (
  user_id INTEGER,
  stock_id INTEGER,
  created_at TEXT,
  PRIMARY KEY(user_id, stock_id)
)
""")

cur.execute("""
CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  side TEXT,
  stock_id INTEGER,
  price REAL,
  volume INTEGER,
  status TEXT,
  created_at TEXT,
  approved_by INTEGER,
  approved_at TEXT,
  notes TEXT
)
""")

cur.execute("""
CREATE TABLE automatic_orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  stock_id INTEGER,
  side TEXT,
  trigger_type TEXT,
  trigger_value REAL,
  limit_price REAL,
  volume INTEGER,
  is_active INTEGER,
  status TEXT,
  created_at TEXT,
  approved_by INTEGER,
  approved_at TEXT,
  notes TEXT
)
""")

cur.execute("""
CREATE TABLE exercises (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER,
  stock_id INTEGER,
  rights_code TEXT,
  quantity INTEGER,
  status TEXT,
  created_at TEXT,
  approved_by INTEGER,
  approved_at TEXT
)
""")

# Seed users
import os

def add_user(username, password, role='user', is_active=1):
    salt = os.urandom(16).hex()
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000).hex()
    cur.execute('INSERT INTO users (username, password_hash, salt, role, is_active, created_at) VALUES (?,?,?,?,?,?)',
                (username, pwd_hash, salt, role, is_active, datetime.utcnow().isoformat()))

add_user('admin','admin123','admin')
add_user('user1','user123','user')

# Brokers
cur.executemany('INSERT INTO brokers (code, name) VALUES (?,?)', [
    ('AJA','Andalan Jaya'), ('BNI','Bina Niaga Indah'), ('MND','Mandiri Sekuritas')
])

# Sectors & Subsectors
for s in ['Finance','Consumer','Energy']:
    cur.execute('INSERT INTO sectors (name) VALUES (?)', (s,))
cur.execute('SELECT id, name FROM sectors')
sec_map = {name: sid for sid, name in cur.fetchall()}
for s, subs in {'Finance':['Banking','Insurance'], 'Consumer':['Staples','Discretionary'], 'Energy':['Oil & Gas','Coal']}.items():
    for sub in subs:
        cur.execute('INSERT INTO subsectors (sector_id, name) VALUES (?,?)', (sec_map[s], sub))
cur.execute('SELECT id, name FROM subsectors')
sub_map = {name: sid for sid, name in cur.fetchall()}

# Stocks
cur.executemany("""
INSERT INTO stocks (ticker, name, sector_id, subsector_id, lot_size, price_prev_close, market_cap, free_float)
VALUES (?,?,?,?,?,?,?,?)
""", [
    ('BBRI','Bank Rakyat', sec_map['Finance'], sub_map['Banking'], 100, 5200.0, 600e12, 0.47),
    ('BBCA','Bank Central', sec_map['Finance'], sub_map['Banking'], 100, 9700.0, 900e12, 0.45),
    ('ASII','Astra Int', sec_map['Consumer'], sub_map['Discretionary'], 100, 6000.0, 250e12, 0.50),
    ('PGAS','Perusahaan Gas', sec_map['Energy'], sub_map['Oil & Gas'], 100, 1600.0, 38e12, 0.55)
])

# Indices & membership
cur.executemany('INSERT INTO indices (code, name) VALUES (?,?)', [('LQ45','Liquid 45'),('IDX30','IDX 30')])
cur.execute('SELECT id, code FROM indices')
idx_map = {code: iid for iid, code in cur.fetchall()}
cur.execute('SELECT id, ticker FROM stocks')
stk_map = {t: i for i, t in cur.fetchall()}
cur.executemany('INSERT INTO stock_index_membership (index_id, stock_id) VALUES (?,?)', [
    (idx_map['LQ45'], stk_map['BBRI']), (idx_map['LQ45'], stk_map['BBCA']),
    (idx_map['IDX30'], stk_map['ASII']), (idx_map['IDX30'], stk_map['PGAS'])
])

# Prices (30 hari)
base = datetime.utcnow()
for t in ['BBRI','BBCA','ASII','PGAS']:
    sid = stk_map[t]
    price = {'BBRI':5200,'BBCA':9700,'ASII':6000,'PGAS':1600}[t]
    for d in range(30):
        ts = (base - timedelta(days=30-d)).isoformat()
        price = round(price * (1 + (0.002 if d%4==0 else -0.001)), 2)
        vol = 100000 + d*200
        cur.execute('INSERT INTO prices (stock_id, ts, price, volume) VALUES (?,?,?,?)', (sid, ts, price, vol))

# Orderbook
for t in ['BBRI','BBCA']:
    sid = stk_map[t]
    for lvl in range(1,6):
        cur.execute('INSERT OR REPLACE INTO orderbook_levels (stock_id, side, level, price, lot, orders_count) VALUES (?,?,?,?,?,?)', (sid,'bid',lvl, 5000-lvl*10, 50+lvl*5, 10+lvl))
        cur.execute('INSERT OR REPLACE INTO orderbook_levels (stock_id, side, level, price, lot, orders_count) VALUES (?,?,?,?,?,?)', (sid,'ask',lvl, 5000+lvl*10, 45+lvl*5, 8+lvl))

# Trades
cur.execute('SELECT id FROM brokers WHERE code=?', ('AJA',))
b1 = cur.fetchone()[0]
cur.execute('SELECT id FROM brokers WHERE code=?', ('MND',))
b2 = cur.fetchone()[0]
for i, t in enumerate(['BBRI','BBCA','ASII','PGAS']):
    sid = stk_map[t]
    for k in range(60):
        ts = (base - timedelta(minutes=k+i*5)).isoformat()
        price = 1000 + i*1000 + (k%12)*7
        volume = 1000 + (k*10)
        value = price*volume
        cur.execute("""
            INSERT INTO trades (ts, stock_id, price, volume, value, broker_buy_id, broker_sell_id, market, status, investor_type)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (ts, sid, price, volume, value, b1, b2, 'Reguler', 'Done', 'Asing' if k%2==0 else 'Domestik'))

# Fundamentals 2022-2024
for t in ['BBRI','BBCA','ASII','PGAS']:
    sid = stk_map[t]
    for year in [2022, 2023, 2024]:
        revenue = 100e12 + (hash(t+str(year))%10)*1e12
        net_income = 20e12 + (hash('n'+t+str(year))%5)*1e12
        eps = round(200 + (hash('e'+t+str(year))%50), 2)
        roa = round(0.02 + (hash('a'+t+str(year))%5)/100, 4)
        roe = round(0.08 + (hash('r'+t+str(year))%7)/100, 4)
        de = round(0.2 + (hash('d'+t+str(year))%30)/100, 2)
        div = round(80 + (hash('v'+t+str(year))%40), 2)
        cur.execute("""
            INSERT INTO fundamentals (stock_id, year, revenue, net_income, eps, roa, roe, debt_to_equity, dividend)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (sid, year, revenue, net_income, eps, roa, roe, de, div))

# Market summary & sector summary
for mkt in ['Reguler','Tunai','Negosiasi']:
    cur.execute('INSERT INTO market_summary (ts, market, instrument_type, volume, value, frequency) VALUES (?,?,?,?,?,?)', (base.isoformat(), mkt, 'Equity', 10_000_000, 5_000_000_000, 200_000))
cur.execute('SELECT id,name FROM sectors')
for sid, nm in cur.fetchall():
    cur.execute('INSERT INTO sector_trade_summary (ts, sector_id, volume, value, frequency) VALUES (?,?,?,?,?)', (base.isoformat(), sid, 1_000_000, 500_000_000, 20_000))

# Currencies
cur.executemany('INSERT INTO currencies (code, name, rate_to_idr, ts) VALUES (?,?,?,?)', [
    ('USD','US Dollar', 15600.0, base.isoformat()),
    ('SGD','Singapore Dollar', 11600.0, base.isoformat()),
    ('JPY','Japanese Yen', 105.0, base.isoformat())
])

# Misc
cur.execute('INSERT INTO news (ts, source, title, url) VALUES (?,?,?,?)', (base.isoformat(),'IDX','Perubahan Aturan Perdagangan','https://www.idx.co.id'))
cur.execute('INSERT INTO research (ts, title, summary) VALUES (?,?,?)', (base.isoformat(),'Outlook 2026','Ringkasan outlook pasar 2026'))
cur.execute('INSERT INTO announcements (ts, category, title, content) VALUES (?,?,?,?)', (base.isoformat(),'Listing','Pencatatan Efek Baru','Rincian pengumuman...'))
cur.execute('INSERT INTO corporate_actions (ts, stock_id, action_type, details) VALUES (?,?,?,?)', (base.isoformat(), stk_map['BBRI'], 'Dividend', 'Dividen tunai Rp100'))

conn.commit()
conn.close()

print('Database created at:', DB_PATH)
