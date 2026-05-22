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
        html_content = html_content.replace('href="/pricing"', 'href="pricing.html"')
        html_content = html_content.replace('href="/tools"', 'href="tools.html"')
        html_content = html_content.replace('href="/tool_copywriting"', 'href="tool_copywriting.html"')
        html_content = html_content.replace('href="/tool_douyin_video"', 'href="tool_douyin_video.html"')
        
        # Special case for logo redirect
        html_content = html_content.replace("window.location.href='/'", "window.location.href='index.html'")
        
        return html_content

    def generate_page(route, template_name, output_name, **context):
        with app.test_request_context(route):
            output = render_template(template_name, **context)
            output = fix_links(output)
            with open(os.path.join(dist_dir, output_name), 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Generated {output_name}")

    # 3. Generate Pages
    generate_page('/', 'index.html', 'index.html')
    generate_page('/login', 'login.html', 'login.html')
    generate_page('/dashboard', 'dashboard.html', 'dashboard.html')
    generate_page('/pricing', 'pricing.html', 'pricing.html')
    generate_page('/tools', 'tools.html', 'tools.html')
    generate_page('/tool_copywriting', 'tools/copywriting.html', 'tool_copywriting.html')
    generate_page('/tool_douyin_video', 'tools/douyin_video.html', 'tool_douyin_video.html')

    # 4. Create ZIP archive
    zip_path = os.path.join(base_dir, 'dist')
    print(f"\nCreating ZIP archive: {zip_path}.zip")
    shutil.make_archive(zip_path, 'zip', dist_dir)

    print("\nBuild completed successfully!")
    print(f"1. Static site directory: {dist_dir}")
    print(f"2. Deployable ZIP file:   {zip_path}.zip")

if __name__ == '__main__':
    build()
