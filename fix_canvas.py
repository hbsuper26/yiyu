import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix CSS for the hero section to ensure canvas fills it properly and interactions work
html = html.replace('.hero-bg {', '.hero-bg { position: relative; ')

# Insert <canvas id="heroCanvas" class="absolute inset-0 z-0"></canvas> if not already right after <section class="... hero-bg">
hero_section_tag = r'<section class="relative pt-32 pb-20 lg:pt-40 lg:pb-32 overflow-hidden hero-bg">'
if '<canvas id="heroCanvas"' not in html.split(hero_section_tag)[1][:200]:
    html = html.replace(hero_section_tag, hero_section_tag + '\n        <canvas id="heroCanvas" class="absolute inset-0 z-0 w-full h-full pointer-events-auto"></canvas>')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Canvas structure fixed.")
