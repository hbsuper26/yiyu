from flask import Flask, render_template, g
import os
import sqlite3

app = Flask(__name__)
# Disable template caching during development
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Add markdown rendering filter
import markdown
from threading import Thread
import schedule
import time
import sys
import os
sys.path.append(os.path.dirname(__file__))
from agent import generate_daily_articles

app.jinja_env.filters['markdown'] = lambda text: markdown.markdown(text, extensions=['extra', 'nl2br'])

# Database helper
DB_PATH = os.path.join(os.path.dirname(__file__), 'yiyu.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DB_PATH)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 0 seconds.
    """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response



@app.route('/tool_copywriting')
def tools_copywriting():
    return render_template('tools/copywriting.html')

@app.route('/tools')
def tools():
    return render_template('tools.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('login.html', is_register=True)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/articles')
def articles():
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM articles ORDER BY id DESC')
    db_articles = cur.fetchall()
    
    # Convert sqlite3.Row objects to dicts
    articles_list = [dict(row) for row in db_articles]
    
    return render_template('articles.html', articles=articles_list)

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM articles WHERE id = ?', (article_id,))
    article = cur.fetchone()
    
    if article is None:
        return "Article not found", 404
        
    return render_template('article_detail.html', article=dict(article))

@app.route('/api/articles.json')
def api_articles():
    """提供给外部拉取 Agent 每日生成文章数据的只读接口"""
    from flask import jsonify
    db = get_db()
    cur = db.cursor()
    # 默认返回最新生成的 10 篇文章
    cur.execute('SELECT id, category_id, title, title_en, summary, summary_en, content, content_en, date, views, seo_keywords FROM articles ORDER BY id DESC LIMIT 10')
    db_articles = cur.fetchall()
    
    articles_list = [dict(row) for row in db_articles]
    
    return jsonify({
        "status": "success",
        "count": len(articles_list),
        "data": articles_list
    })

def scheduled_job():
    print("Running scheduled daily article generation...")
    generate_daily_articles()
    
    print("Articles generated. Triggering static site build...")
    try:
        from build import freezer, app as build_app
        build_app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
        build_app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
        print(f"Building static site to: {build_app.config['FREEZER_DESTINATION']}")
        freezer.freeze()
        print("Build complete! Static site updated.")
    except Exception as e:
        print(f"Error during static site build: {e}")

def run_scheduler():
    """Background thread to run scheduled tasks"""
    # Run the agent and then build the static site every day at 08:00 AM
    schedule.every().day.at("08:00").do(scheduled_job)
    
    # You can also run it every few minutes for testing if needed
    # schedule.every(10).minutes.do(scheduled_job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    # Start the scheduler thread
    scheduler_thread = Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    print("Starting server...")
    try:
        app.run(debug=True, host='0.0.0.0', port=5001)
    except Exception as e:
        print(f"Error: {e}")
