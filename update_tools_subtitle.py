import re

with open('templates/tools.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update the Chinese translation
old_zh_subtitle = 'subtitle: "我们正在为您准备一系列提升投放和素材处理效率的实用工具，敬请期待。"'
new_zh_subtitle = 'subtitle: "聚合多维度核心能力，提供全面、高效的业务辅助方案，为您的每一次决策与执行赋能。"'
html = html.replace(old_zh_subtitle, new_zh_subtitle)

# Update the English translation
old_en_subtitle = 'subtitle: "We are preparing a suite of practical tools to boost your ad operations and asset management efficiency. Stay tuned."'
new_en_subtitle = 'subtitle: "Aggregating multi-dimensional core capabilities to provide comprehensive and efficient business assistance solutions, empowering every decision and execution."'
html = html.replace(old_en_subtitle, new_en_subtitle)

with open('templates/tools.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated subtitle to be more general and abstract.")
