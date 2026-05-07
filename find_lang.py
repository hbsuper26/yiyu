import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'x-text="lang' in line:
        print(f"Line {i+1}: {line.strip()}")
