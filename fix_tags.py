import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix the broken script tags
html = html.replace('<s\n    <s\n    <s\n    <script>', '<script>')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
