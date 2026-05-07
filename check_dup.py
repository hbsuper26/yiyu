import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for duplicate or raw scripts
occurrences = html.count('Immersive 3D Data Particle Network Animation')
print(f"Found 'Immersive 3D Data Particle Network Animation' {occurrences} times.")

if occurrences > 1:
    # Remove the first occurrence which might be raw text
    idx = html.find('Immersive 3D Data Particle Network Animation')
    start_idx = html.rfind('//', 0, idx)
    end_idx = html.find('})();', idx) + 5
    print(f"Removing from {start_idx} to {end_idx}")
    html = html[:start_idx] + html[end_idx:]
    
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
