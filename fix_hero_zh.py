import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('title_full: "全球广告账户 开户·充值·减款",', 'title1: "全球广告账户",\n                    title_full: "全球广告账户 开户·充值·减款",')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
