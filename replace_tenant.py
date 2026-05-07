import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Chinese replacements
content = content.replace('全链路租户与客户管理系统', '全链路客户管理系统')
content = content.replace('租户与客户', '客户')
content = content.replace('租户', '客户')

# English replacements
content = content.replace('Tenant & Client Management', 'Client Management')
content = content.replace('Tenant & Client', 'Client')
content = content.replace('Multi-tenant', 'Multi-client')
content = content.replace('multi-tenant', 'multi-client')
content = content.replace('tenant balance', 'client balance')
content = content.replace('Tenant Spend', 'Client Spend')
content = content.replace('Tenant A', 'Client A')
content = content.replace('Tenant B', 'Client B')
content = content.replace('Tenant C', 'Client C')
content = content.replace('tenant verification', 'client verification')
content = content.replace('Tenant', 'Client')
content = content.replace('tenant', 'client')

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced '租户' with '客户' successfully.")
