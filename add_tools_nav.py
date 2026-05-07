import re
import glob

# Files to update
files = ['templates/articles.html', 'templates/article_detail.html', 'templates/index.html', 'templates/pricing.html']

nav_item = '                    <a href="/tools" class="text-sm font-medium text-slate-600 hover:text-blue-600 transition-colors" x-text="t[lang].nav.tools">实用工具</a>\n'

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 1. Add the nav link right before pricing
    pricing_link_start = html.find('<a href="/pricing"')
    if pricing_link_start != -1 and 'href="/tools"' not in html:
        html = html[:pricing_link_start] + nav_item + html[pricing_link_start:]
    
    # 2. Update the translations dictionary
    # Find zh nav object
    zh_nav_start = html.find('nav: {')
    if zh_nav_start != -1:
        zh_pricing_pos = html.find('pricing:', zh_nav_start)
        if zh_pricing_pos != -1 and 'tools: "实用工具"' not in html[zh_nav_start:zh_pricing_pos]:
            html = html[:zh_pricing_pos] + 'tools: "实用工具",\n                    ' + html[zh_pricing_pos:]
            
    # Find en nav object
    en_nav_start = html.find('nav: {', zh_nav_start + 50)
    if en_nav_start != -1:
        en_pricing_pos = html.find('pricing:', en_nav_start)
        if en_pricing_pos != -1 and 'tools: "Tools"' not in html[en_nav_start:en_pricing_pos]:
            html = html[:en_pricing_pos] + 'tools: "Tools",\n                    ' + html[en_pricing_pos:]
            
    with open(file, 'w', encoding='utf-8') as f:
        f.write(html)

print("Nav updated in all templates.")
