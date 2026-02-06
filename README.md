# Broker Saham Demo – Multipage (Streamlit + SQLite)

## Cara Menjalankan
```bash
python seed_db.py   # membuat database + sample data
pip install -r requirements.txt
streamlit run app.py
```

Login contoh:
- admin / admin123 (role: admin)
- user1 / user123 (role: user)

DB Path default: `data/broker_app.db` (override via env `DB_PATH`).
