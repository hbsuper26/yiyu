import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make the title text massive and behind/in-front style to match the GIF
# We can add a large, semi-transparent background text that reacts to mouse
large_text_html = """
        <!-- Giant Background Text -->
        <div class="absolute inset-0 flex items-center justify-center pointer-events-none z-0 overflow-hidden" id="giantTextContainer">
            <div class="text-[15rem] md:text-[25rem] font-black text-white/5 tracking-tighter whitespace-nowrap select-none" id="giantText">
                GLOBAL
            </div>
        </div>
"""

# Insert right before the canvas
canvas_tag = '<canvas id="heroCanvas"'
if 'id="giantTextContainer"' not in html:
    html = html.replace(canvas_tag, large_text_html + '\n        ' + canvas_tag)

# Update the GSAP script to animate the giant text
gsap_script_update = """
                        // Giant Text Parallax
                        const giantText = document.getElementById('giantText');
                        if (giantText) gsap.to(giantText, { x: x * 100, y: y * 50, duration: 2, ease: 'power2.out' });
"""

old_gsap_end = html.find('// Mockup rotates and moves with mouse')
if old_gsap_end != -1 and 'Giant Text Parallax' not in html:
    html = html[:old_gsap_end] + gsap_script_update + html[old_gsap_end:]

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Giant text added.")
