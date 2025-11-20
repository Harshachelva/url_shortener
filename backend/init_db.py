import sqlite3
import os

DB_DIR = 'data'
DB_PATH = os.path.join(DB_DIR, 'shortener.db')

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print(f"Checking/Creating database structure at {DB_PATH}...")

cursor.execute(
   """
   CREATE TABLE IF NOT EXISTS urls (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       original_url TEXT NOT NULL,
       short_code TEXT UNIQUE NOT NULL
   )
"""
)
conn.commit()
conn.close()
print("Database structure initialized successfully.")