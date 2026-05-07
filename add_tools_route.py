import re

with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

route = """
@app.route('/tools')
def tools():
    return render_template('tools.html')
"""

if "@app.route('/tools')" not in app_py:
    # Insert before the first route
    idx = app_py.find("@app.route('/')")
    if idx != -1:
        app_py = app_py[:idx] + route + "\n" + app_py[idx:]
        with open('app.py', 'w', encoding='utf-8') as f:
            f.write(app_py)
        print("Added /tools route to app.py")
