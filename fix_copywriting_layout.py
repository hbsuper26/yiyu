import re

with open('templates/tools/copywriting.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix body classes
html = html.replace('<body class="p-4 md:p-8 flex items-center justify-center">', '<body class="flex flex-col min-h-screen">')

# 2. Make the nav fixed at top or just normal block but without margin pushing things weirdly
nav_old = """    <!-- Navbar -->
    <nav class="w-full bg-white shadow-sm mb-6 border-b border-slate-100">"""
nav_new = """    <!-- Navbar -->
    <nav class="w-full bg-white/80 backdrop-blur-md shadow-sm border-b border-white/20 sticky top-0 z-50">"""
html = html.replace(nav_old, nav_new)

# 3. Wrap the main glass panel
glass_start = html.find('<div class="glass-panel rounded-3xl')
if glass_start != -1 and '<main class="flex-1 flex items-center justify-center p-4 md:p-8">' not in html:
    html = html[:glass_start] + '<main class="flex-1 flex items-center justify-center p-4 md:p-8 w-full">\n        ' + html[glass_start:]
    
    # Close main tag before scripts or body end
    script_start = html.find('<script>', glass_start)
    if script_start != -1:
        html = html[:script_start] + '    </main>\n\n    ' + html[script_start:]
    else:
        body_end = html.find('</body>')
        html = html[:body_end] + '    </main>\n' + html[body_end:]

with open('templates/tools/copywriting.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Fixed copywriting layout.")
