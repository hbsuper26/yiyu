import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the giant text blend better and look more like the GIF (massive, overlapping, deep space)
html = html.replace('text-[15rem] md:text-[25rem] font-black text-white/5', 'text-[15rem] md:text-[30rem] font-black text-white/5 mix-blend-overlay')

# The hero section needs to be truly full screen to look like the GIF
html = html.replace('<section class="relative pt-32 pb-20 lg:pt-40 lg:pb-32 overflow-hidden hero-bg">', '<section class="relative pt-32 pb-20 lg:pt-40 lg:pb-32 min-h-screen flex items-center overflow-hidden hero-bg">')

# Add 3D rotation properties to the container to give it depth
html = html.replace('<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">', '<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 w-full" style="perspective: 1000px;">')

# Ensure canvas is properly placed and sized
html = html.replace('class="absolute inset-0 z-0 w-full h-full pointer-events-auto"', 'class="absolute inset-0 z-0 w-full h-full pointer-events-auto mix-blend-screen"')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Hero layout improved for full-screen immersive effect.")
