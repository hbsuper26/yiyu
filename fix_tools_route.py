import re

with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

app_py = app_py.replace("@app.route('/tools/copywriting')", "@app.route('/tool_copywriting')")

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

with open('templates/tools.html', 'r', encoding='utf-8') as f:
    tools_html = f.read()

tools_html = tools_html.replace('href="/tools/copywriting"', 'href="/tool_copywriting"')

with open('templates/tools.html', 'w', encoding='utf-8') as f:
    f.write(tools_html)

print("Fixed route clash.")
