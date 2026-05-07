import os
from flask import Flask
from flask_frozen import Freezer
from app import app, get_db

# Set freezer config
app.config['FREEZER_DESTINATION'] = os.path.join(os.path.dirname(__file__), 'dist')
app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
app.config['FREEZER_REMOVE_EXTRA_FILES'] = False

freezer = Freezer(app)

@freezer.register_generator
def article_detail():
    with app.app_context():
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT id FROM articles')
        articles = cur.fetchall()
        for article in articles:
            yield {'article_id': article['id']}

if __name__ == '__main__':
    print(f"Building static site to: {app.config['FREEZER_DESTINATION']}")
    freezer.freeze()
    print("Build complete!")
