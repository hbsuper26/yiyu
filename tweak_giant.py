import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the giant text slightly more visible and responsive
html = html.replace('text-[20rem] md:text-[35rem] font-black text-blue-500/5', 'text-[15rem] md:text-[25rem] lg:text-[35rem] font-black text-blue-500/10')
html = html.replace('text-[20rem] md:text-[35rem] font-black text-white/5', 'text-[15rem] md:text-[25rem] lg:text-[35rem] font-black text-white/10')

# Also fix the GSAP animation so it moves nicely
gsap_update = """
                        // Giant Text Parallax Depth
                        const giantTextBack = document.getElementById('giantTextBack');
                        const giantTextFront = document.getElementById('giantTextFront');
                        if (giantTextBack) gsap.to(giantTextBack, { x: x * 80, y: y * 40, duration: 2, ease: 'power2.out' });
                        if (giantTextFront) gsap.to(giantTextFront, { x: x * 150, y: y * 80, duration: 2, ease: 'power2.out' });
"""

old_start = html.find('// Giant Text Parallax Depth')
if old_start != -1:
    old_end = html.find('if (textFront)', old_start)
    html = html[:old_start] + gsap_update[25:] + html[old_end:]

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
