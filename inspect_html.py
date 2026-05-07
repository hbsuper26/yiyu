import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's find the start of the raw JS text. Looking at the output, the 6th script tag is at 80460.
# The 5th script tag is at 58366.
# Let's inspect the text around 80445 (the 5th </script>)

print("Text around 80445:")
print(html[80400:80600])

