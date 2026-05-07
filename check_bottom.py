import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The screenshot shows the text without ANY HTML formatting, which means the JS code
# was probably inserted outside of the `<script>` tag or the tags got escaped/stripped somewhere.
# Looking at the user's screenshot, it's the very bottom of the page or replacing everything.
# Wait, look closely at the user's screenshot. The text is JUST the JS code.
# The entire page is JUST the JS code.

# Ah! In my `add_3d_canvas.py` script:
# old_script_start = html.find('// Enhanced Hero Background Particle & Data Flow Animation')
# old_script_end = html.find('</script>', old_script_start) + 9
# html = html[:old_script_start-15] + enhanced_particle_script + html[old_script_end:]
# This might have accidentally deleted the closing `</body></html>` tags or messed up the structure.

print(html[-500:])
