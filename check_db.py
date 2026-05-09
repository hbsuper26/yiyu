import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'yiyu.db')
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute('SELECT id, title, category_id FROM articles')
for row in cur.fetchall():
    print(row)
conn.close()
