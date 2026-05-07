import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make sure z-indices are perfectly ordered so the text intertwines correctly
# giantTextBack -> canvas -> giantTextFront -> text content

# Update giantTextBack
html = html.replace('id="giantTextBack"', 'id="giantTextBack" style="z-index: 0;"')

# Update Canvas
html = html.replace('<canvas id="heroCanvas" class="absolute inset-0 z-0 w-full h-full pointer-events-auto mix-blend-screen"></canvas>', '<canvas id="heroCanvas" class="absolute inset-0 w-full h-full pointer-events-auto mix-blend-screen" style="z-index: 1;"></canvas>')

# Update giantTextFront
html = html.replace('id="giantTextFront"', 'id="giantTextFront" style="z-index: 2;"')

# Update Hero Content Container
html = html.replace('<div class="flex flex-col lg:flex-row items-center justify-center gap-16 relative z-10 w-full pointer-events-none">', '<div class="flex flex-col lg:flex-row items-center justify-center gap-16 relative w-full pointer-events-none" style="z-index: 10;">')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Z-index layering updated.")
