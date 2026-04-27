import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'yiyu.db')

def migrate_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Check if seo_keywords exists
    c.execute("PRAGMA table_info(articles)")
    columns = [col[1] for col in c.fetchall()]
    
    if 'seo_keywords' not in columns:
        print("Adding seo_keywords column...")
        c.execute("ALTER TABLE articles ADD COLUMN seo_keywords TEXT DEFAULT ''")
        
    if 'seo_score' not in columns:
        print("Adding seo_score column...")
        c.execute("ALTER TABLE articles ADD COLUMN seo_score INTEGER DEFAULT 0")
        
    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == '__main__':
    migrate_db()