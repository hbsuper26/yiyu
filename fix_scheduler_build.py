import re

with open('app.py', 'r', encoding='utf-8') as f:
    app_py = f.read()

# Fix the import for freezer
app_py = app_py.replace('from build import freezer, app as build_app', 'from build_dist import freezer')

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(app_py)

print("Fixed scheduled_job build import in app.py")
