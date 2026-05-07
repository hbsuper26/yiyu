import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for ANY text that matches "// Immersive 3D Data Particle Network Animation"
count = html.count('// Immersive 3D Data Particle Network Animation')
print(f"Count: {count}")

# Are there any other occurrences of "Particle Network"?
print("Other occurrences of Particle Network:")
for m in re.finditer(r'.{0,30}Particle Network.{0,30}', html):
    print(m.group(0))

