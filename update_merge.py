import re
with open('d:/AI生成原型/yiyu_digital_media/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Make the title full for translations
content = content.replace('title1: "全球广告账户",', 'title_full: "全球广告账户 开户·充值·减款",\n                    stat1: "极速开户与资金下发",\n                    stat2: "全球主流媒体渠道支持",')
content = content.replace('title1: "Global Ad Accounts",', 'title_full: "Global Ad Accounts Open · Recharge · Deduct",\n                    stat1: "Fast Opening & Dispatch",\n                    stat2: "Global Media Channels",')

with open('d:/AI生成原型/yiyu_digital_media/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
