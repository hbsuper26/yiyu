import re
with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Get all keys used in x-text
used_keys = re.findall(r'x-text=["\']t\[lang\]\.([^"\']+)["\']', html)
print('Used keys in HTML:', sorted(list(set(used_keys))))

# Get translations object
match = re.search(r'const translations = (.*?);\s*function appData\(\)', html, re.DOTALL)
if match:
    js_code = match.group(1)
    
    # We will just manually check if these keys exist in the JS code
    missing_zh = []
    missing_en = []
    
    # Split into zh and en parts
    zh_part = js_code[js_code.find('zh: {'):js_code.find('en: {')]
    en_part = js_code[js_code.find('en: {'):]
    
    for key in set(used_keys):
        parts = key.split('.')
        if len(parts) == 2:
            section, prop = parts
            if f'{section}:' not in zh_part or f'{prop}:' not in zh_part:
                missing_zh.append(key)
            if f'{section}:' not in en_part or f'{prop}:' not in en_part:
                missing_en.append(key)
                
    print('Missing in zh:', missing_zh)
    print('Missing in en:', missing_en)
