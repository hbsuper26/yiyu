import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Wait! Look at the screenshot again carefully. The text is white on a dark blue background.
# It is exactly the `hero-bg` section!
# If the text is showing up in the `hero-bg` section, it means the script was injected INSIDE a visible element instead of at the end of the body, OR it's not wrapped in a script tag at all where it was injected!
# Wait, the screenshot shows `// Immersive 3D Data Particle Network Animation` without a `<script>` tag.
# Oh! In my `add_3d_canvas.py`:
# old_script_start = html.find('// Enhanced Hero Background Particle & Data Flow Animation')
# old_script_end = html.find('</script>', old_script_start) + 9
# html = html[:old_script_start-15] + enhanced_particle_script + html[old_script_end:]
# If `old_script_start-15` didn't correctly remove the old `<script>` tag, maybe I have `<script><script>` or something?

print("Script block:")
idx = html.find('// Immersive 3D Data Particle Network Animation')
print(html[idx-50:idx+50])

