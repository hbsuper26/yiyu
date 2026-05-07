import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'x-text=([^\s>]+)', html)
for m in matches:
    if not (m.startswith('"') and m.endswith('"')) and not (m.startswith("'") and m.endswith("'")):
        print('Bad x-text:', m)
