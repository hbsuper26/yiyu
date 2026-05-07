import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('title_full: "鍏ㄧ悆骞垮憡璐︽埛 寮€鎴仿峰厖鍊悸峰噺娆?",', 'title1: "鍏ㄧ悆骞垮憡璐︽埛",\n                    title_full: "鍏ㄧ悆骞垮憡璐︽埛 寮€鎴仿峰厖鍊悸峰噺娆?",')
content = content.replace('title_full: "Global Ad Accounts Open · Recharge · Deduct",', 'title1: "Global Ad Accounts",\n                    title_full: "Global Ad Accounts Open · Recharge · Deduct",')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
