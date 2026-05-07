import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all <script> and </script> tags
script_starts = [m.start() for m in re.finditer(r'<script.*?>', html)]
script_ends = [m.start() for m in re.finditer(r'</script>', html)]

print("Starts:", script_starts)
print("Ends:", script_ends)

# Wait, there are 2 starts and 6 ends. This means I accidentally injected extra </script> tags or replaced <script> with something else.
# Let's fix this by finding the raw JS block at the end and wrapping it properly.

# Let's just rewrite the bottom part of the HTML to be safe
body_close = html.rfind('</body>')
if body_close != -1:
    bottom_html = html[body_close-5000:body_close+20]
    print(bottom_html)

