import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Enhance the giant text to have multiple layers for a deep 3D effect
giant_text_html = """
        <!-- Giant Background Text Layers -->
        <div class="absolute inset-0 flex items-center justify-center pointer-events-none z-0 overflow-hidden" id="giantTextContainer">
            <div class="text-[20rem] md:text-[35rem] font-black text-blue-500/5 tracking-tighter whitespace-nowrap select-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 mix-blend-screen blur-sm" id="giantTextBack">
                GLOBAL
            </div>
            <div class="text-[20rem] md:text-[35rem] font-black text-white/5 tracking-tighter whitespace-nowrap select-none absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 mix-blend-overlay" id="giantTextFront">
                GLOBAL
            </div>
        </div>
"""

# Replace the old giant text container
old_giant_start = html.find('<!-- Giant Background Text -->')
if old_giant_start != -1:
    old_giant_end = html.find('</div>\n        </div>', old_giant_start) + 23
    html = html[:old_giant_start] + giant_text_html + html[old_giant_end:]

# Update the GSAP script to animate both layers differently for parallax depth
gsap_script_update = """
                        // Giant Text Parallax Depth
                        const giantTextBack = document.getElementById('giantTextBack');
                        const giantTextFront = document.getElementById('giantTextFront');
                        if (giantTextBack) gsap.to(giantTextBack, { x: x * 60, y: y * 30, duration: 2, ease: 'power2.out' });
                        if (giantTextFront) gsap.to(giantTextFront, { x: x * 120, y: y * 60, duration: 2, ease: 'power2.out' });
"""

old_gsap_giant_start = html.find('// Giant Text Parallax')
if old_gsap_giant_start != -1:
    old_gsap_giant_end = html.find('if (giantText)', old_gsap_giant_start)
    old_gsap_giant_end = html.find('\n', old_gsap_giant_end)
    html = html[:old_gsap_giant_start] + gsap_script_update + html[old_gsap_giant_end:]

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Giant text 3D depth added.")
