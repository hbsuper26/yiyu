import re

with open('build_dist.py', 'r', encoding='utf-8') as f:
    build_py = f.read()

# Make sure it freezes the tools page too
# Actually, Flask-Frozen automatically finds all routes without parameters, so /tools will be frozen automatically!
print("Flask-Frozen handles parameter-less routes automatically.")
