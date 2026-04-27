import os
import sys
from flask_frozen import Freezer

# Add the project directory to sys.path so we can import app
sys.path.append(os.path.dirname(__file__))

# Import the Flask app
from app import app
from db import get_db_connection

# Configure the freezer to output to 'yiyu_digital_media/dist' folder
app.config['FREEZER_DESTINATION'] = os.path.join(os.path.dirname(__file__), 'dist')
app.config['FREEZER_RELATIVE_URLS'] = True

freezer = Freezer(app)

@freezer.register_generator
def article_detail():
    """Generator for dynamic article detail pages."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute('SELECT id FROM articles')
        articles = c.fetchall()
        conn.close()
        
        for article in articles:
            yield {'article_id': article['id']}
    except Exception as e:
        print(f"Warning: Could not fetch articles for generator: {e}")
        # Yield empty so it doesn't crash if db is empty or missing
        return

if __name__ == '__main__':
    # Add .html extension to generated pages instead of directory index
    app.config['FREEZER_DEFAULT_MIMETYPE'] = 'text/html'
    # Ensure the freezer completely overwrites/cleans the destination folder
    app.config['FREEZER_REMOVE_EXTRA_FILES'] = False
    
    print(f"Building static site to: {app.config['FREEZER_DESTINATION']}")
    freezer.freeze()
    print("Build complete! Check the 'dist' folder.")