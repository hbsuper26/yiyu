import os
import sys
import shutil
from flask import Flask, render_template

# Add current directory to path to import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app

def build():
    # Base directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dist_dir = os.path.join(base_dir, 'dist')
    static_dir = os.path.join(base_dir, 'static')

    print(f"Building static site to: {dist_dir}")

    # 1. Clean and Create dist directory
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)

    # 2. Copy Static Files
    if os.path.exists(static_dir):
        shutil.copytree(static_dir, os.path.join(dist_dir, 'static'))
        print("Copied static files.")
    else:
        print("Warning: No static directory found.")

    # Helper to fix links for static deployment
    def fix_links(html_content):
        # Fix static asset links to be relative
        html_content = html_content.replace('"/static/', '"static/')
        html_content = html_content.replace("'/static/", "'static/")
        
        # Fix navigation links
        html_content = html_content.replace('href="/"', 'href="index.html"')
        html_content = html_content.replace('href="/login"', 'href="login.html"')
        html_content = html_content.replace('href="/register"', 'href="login.html"')
        html_content = html_content.replace('href="/dashboard"', 'href="dashboard.html"')
        
        # Special case for logo redirect
        html_content = html_content.replace("window.location.href='/'", "window.location.href='index.html'")
        
        return html_content

    # 3. Generate Pages
    
    # 3.1 Index -> index.html
    with app.test_request_context('/'):
        output = render_template('index.html')
        output = fix_links(output)
        with open(os.path.join(dist_dir, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(output)
        print("Generated index.html")

    # 3.2 Login -> login.html
    with app.test_request_context('/login'):
        output = render_template('login.html')
        output = fix_links(output)
        with open(os.path.join(dist_dir, 'login.html'), 'w', encoding='utf-8') as f:
            f.write(output)
        print("Generated login.html")

    # 3.3 Dashboard -> dashboard.html
    with app.test_request_context('/dashboard'):
        output = render_template('dashboard.html')
        output = fix_links(output)
        with open(os.path.join(dist_dir, 'dashboard.html'), 'w', encoding='utf-8') as f:
            f.write(output)
        print("Generated dashboard.html")

    # 4. Create ZIP archive
    zip_path = os.path.join(base_dir, 'dist')
    print(f"\nCreating ZIP archive: {zip_path}.zip")
    shutil.make_archive(zip_path, 'zip', dist_dir)

    print("\nBuild completed successfully!")
    print(f"1. Static site directory: {dist_dir}")
    print(f"2. Deployable ZIP file:   {zip_path}.zip")

if __name__ == '__main__':
    build()