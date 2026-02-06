import hashlib
from data.db import query_df

def verify_password(password: str, stored_hash: str, salt_hex: str) -> bool:
    salt = bytes.fromhex(salt_hex)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return pwd_hash.hex() == stored_hash

def get_active_user(username: str):
    df = query_df('SELECT * FROM users WHERE username=? AND is_active=1', [username])
    return None if df.empty else df.iloc[0]
