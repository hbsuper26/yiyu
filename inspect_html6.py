import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Ah, look at this:
# setTimeout(() => {
#                         document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => {
#                             observer.observe(el);
#                         });
#                     }, 100);
#                 }
#             }
#         }
#     </script>
# 
# Wait, this `observer.observe(el)` is from Alpine.js `init` or some global script.
# The issue might be that inside the `tweak_giant.py` or earlier, I messed up the curly braces!
# Wait, in `test_animation.py` I generated `screenshot_hero_animated.png`.
# I should look at `dist/index.html` to see if it's the same.
# Or better yet, maybe the `<script>` tag itself is rendered because it's inside a `<div>` that has `x-text` or something? No, it's at the end.
# If a script tag is rendered as text on the screen, it's usually because:
# 1. It is inside a `<pre>` or `<code>` tag.
# 2. A previous tag was not closed properly, e.g., `<div class="...` (missing `>`), causing the browser to parse the rest as text.
# 3. An attribute was not closed properly, e.g., `class="something` (missing `"`).

# Let's search for unclosed attributes or tags before the script.
idx = html.find('// Immersive 3D Data Particle Network Animation')
# Let's check the HTML around the end of the `features` section or `hero` section.
print(html[idx-1500:idx])
