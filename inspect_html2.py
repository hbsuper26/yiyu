import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# I see it. It is actually inside a `<script>` tag.
# But wait, if it's inside a `<script>` tag, why is it rendering as text?
# Oh! The user might be viewing it in an editor where word wrap makes it look like text,
# OR the screenshot shows the code minified or raw? 
# Wait, look at the screenshot. It says `// Immersive 3D Data Particle Network Animation (function() { const canvas = ...`
# It's all on ONE line in the screenshot!
# If it's rendering as text on the webpage, it's because there's a missing closing bracket somewhere earlier that broke the HTML parser, or something.
# Let's check the very end of the file again.

# Let's search for "Immersive 3D Data Particle Network Animation"
parts = html.split('// Immersive 3D Data Particle Network Animation')
print(f"There are {len(parts)-1} instances.")
print("Before first instance:")
print(parts[0][-200:])

