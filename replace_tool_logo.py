import re

with open('templates/tools/copywriting.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the magic wand icon with the logo image
old_logo = """<div class="w-10 h-10 rounded-full bg-gradient-to-tr from-primary to-secondary flex items-center justify-center text-white shadow-lg">
                    <i class="fa-solid fa-wand-magic-sparkles"></i>
                </div>"""
                
new_logo = """<div class="w-10 h-10 rounded-lg flex items-center justify-center shadow-md overflow-hidden bg-white">
                    <img src="{{ url_for('static', filename='images/logo.png') }}" alt="Logo" class="w-full h-full object-cover" onerror="this.src='https://ui-avatars.com/api/?name=YY&background=0D8ABC&color=fff'">
                </div>"""

html = html.replace(old_logo, new_logo)

with open('templates/tools/copywriting.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Replaced magic wand with Yiyu logo.")
