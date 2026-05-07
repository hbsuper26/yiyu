import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's see where exactly this <script> tag is located in the HTML tree.
# It should be right before </body>.
idx = html.find('// Immersive 3D Data Particle Network Animation')
print("Context around script:")
print(html[idx-500:idx+200])

