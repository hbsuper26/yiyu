import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'yiyu.db')

def migrate_db_en():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if english fields exist
    c.execute("PRAGMA table_info(articles)")
    columns = [col[1] for col in c.fetchall()]
    
    if 'title_en' not in columns:
        print("Adding title_en column...")
        c.execute("ALTER TABLE articles ADD COLUMN title_en TEXT DEFAULT ''")
        
    if 'summary_en' not in columns:
        print("Adding summary_en column...")
        c.execute("ALTER TABLE articles ADD COLUMN summary_en TEXT DEFAULT ''")
        
    if 'content_en' not in columns:
        print("Adding content_en column...")
        c.execute("ALTER TABLE articles ADD COLUMN content_en TEXT DEFAULT ''")
        
    conn.commit()
    conn.close()
    print("Migration for English fields complete.")

if __name__ == '__main__':
    migrate_db_en()