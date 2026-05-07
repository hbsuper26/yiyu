import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace GLOBAL with FUNDS or something more relevant to the current brand
html = html.replace('id="giantTextBack">\n                GLOBAL\n            </div>', 'id="giantTextBack">\n                FUNDS\n            </div>')
html = html.replace('id="giantTextFront">\n                GLOBAL\n            </div>', 'id="giantTextFront">\n                FUNDS\n            </div>')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
