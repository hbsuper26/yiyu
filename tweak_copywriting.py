import re

with open('templates/tools/copywriting.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure Tailwind CSS is loaded, since the original file uses cdn.tailwindcss.com. It is.
# Add a back button to return to the tools page, or a basic navbar.
nav = """
    <!-- Navbar -->
    <nav class="w-full bg-white shadow-sm mb-6 border-b border-slate-100">
        <div class="max-w-6xl mx-auto px-4">
            <div class="flex justify-between h-16 items-center">
                <div class="flex items-center gap-4">
                    <a href="/tools" class="text-slate-500 hover:text-primary transition-colors flex items-center gap-2">
                        <i class="fas fa-arrow-left"></i> 返回工具库
                    </a>
                    <div class="h-6 w-px bg-slate-200"></div>
                    <span class="font-bold text-slate-800 text-lg">文案裂变神器</span>
                </div>
            </div>
        </div>
    </nav>
"""

# Insert the nav after the body tag
body_start = html.find('<body')
if body_start != -1:
    body_end = html.find('>', body_start) + 1
    # Check if there's already a nav
    if "返回工具库" not in html:
        html = html[:body_end] + nav + html[body_end:]
        with open('templates/tools/copywriting.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("Added navbar to copywriting.html")
    else:
        print("Navbar already exists.")
