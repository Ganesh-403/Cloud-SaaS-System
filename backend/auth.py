from flask_jwt_extended import create_access_token
import sqlite3
from config import DATABASE_PATH

def authenticate(username, password):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()

    if user and user[0] == password:
        return create_access_token(identity={"username": username, "role": user[1]})
    return None
