import re

with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

route = """
@app.route('/tools/copywriting')
def tools_copywriting():
    return render_template('tools/copywriting.html')
"""

if "@app.route('/tools/copywriting')" not in app_py:
    # Insert before the first route
    idx = app_py.find("@app.route('/tools')")
    if idx != -1:
        app_py = app_py[:idx] + route + "\n" + app_py[idx:]
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(app_py)
        print("Added /tools/copywriting route to app.py")
