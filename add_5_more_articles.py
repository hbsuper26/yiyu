import sqlite3
import random
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'yiyu.db')

def add_5_articles():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    articles = [
        {
            "category": "news",
            "title": "2026年Meta官方代理商政策调整解读",
            "title_en": "Interpretation of Meta's 2026 Official Agency Policy Adjustments",
            "summary": "Meta近期更新了亚太区代理商开户与信用额度政策，本文为您详细解读新规变化及应对策略。",
            "summary_en": "Meta recently updated its agency account opening and credit line policies in the APAC region. Here is a detailed interpretation.",
            "keywords": "Meta政策, 代理商, 广告开户, 信用额度",
            "zh_content": "## 1. 政策背景\n\n随着全球数字广告市场的合规化进程加快，Meta 在2026年第一季度对亚太区代理商政策进行了新一轮的调整。\n\n## 2. 核心变化\n\n- **开户审核加严**：对电商和游戏客户的资质要求提升。\n- **信用额度动态调整**：引入AI信用评估模型。\n\n## 3. 出海企业如何应对\n\n建议企业提前准备好完整的营业执照、业务模式说明，并保持良好的账户消耗记录。",
            "en_content": "## 1. Policy Background\n\nAs global digital advertising compliance accelerates, Meta has adjusted its APAC agency policies for Q1 2026.\n\n## 2. Core Changes\n\n- **Stricter Account Audits**: Higher requirements for e-commerce and gaming clients.\n- **Dynamic Credit Lines**: Introduction of an AI credit evaluation model.\n\n## 3. How to Respond\n\nPrepare complete business licenses and maintain a good ad spend history."
        },
        {
            "category": "insight",
            "title": "东南亚电商市场：TikTok Shop 与 Shopee 流量对比",
            "title_en": "SEA E-commerce: TikTok Shop vs. Shopee Traffic Comparison",
            "summary": "深入对比两大平台的流量分发逻辑与ROI表现，帮助出海商家选择最适合的带货渠道。",
            "summary_en": "A deep comparison of traffic distribution logic and ROI between the two major platforms.",
            "keywords": "东南亚电商, TikTok Shop, Shopee, 流量分发",
            "zh_content": "## 1. 流量逻辑的本质差异\n\n- **TikTok Shop**：兴趣电商，货找人。依赖短视频和直播的瞬间爆发力。\n- **Shopee**：货架电商，人找货。依赖关键词搜索和店铺权重。\n\n## 2. 获客成本对比\n\n目前 TikTok Shop 的早期红利仍在，CPA 相对较低，但退货率略高。Shopee 流量精准，但站内广告竞争激烈。\n\n## 3. 破局建议\n\n采用“TikTok引流 + Shopee承接”的双栖作战模式，最大化流量价值。",
            "en_content": "## 1. Essential Differences in Traffic Logic\n\n- **TikTok Shop**: Interest-based e-commerce (product finds user). Relies on short videos and live streams.\n- **Shopee**: Shelf-based e-commerce (user finds product). Relies on keyword search.\n\n## 2. CAC Comparison\n\nTikTok Shop still has early demographic dividends with lower CPAs. Shopee offers precise traffic but fierce ad competition.\n\n## 3. Strategic Advice\n\nAdopt a dual-channel strategy: drive traffic via TikTok and fulfill via Shopee."
        },
        {
            "category": "guide",
            "title": "Google Performance Max (PMax) 广告爆量投放指南",
            "title_en": "Google Performance Max (PMax) Ad Scaling Guide",
            "summary": "全面解析PMax广告系列的搭建技巧、素材要求与数据优化方法，实现全渠道覆盖。",
            "summary_en": "A comprehensive guide on setting up PMax campaigns, asset requirements, and optimization.",
            "keywords": "Google Ads, PMax, 效果最大化, 广告优化",
            "zh_content": "## 1. 什么是 PMax？\n\n效果最大化广告系列 (Performance Max) 允许广告主通过单个广告系列访问所有 Google Ads 渠道库。\n\n## 2. 素材资产的最佳实践\n\n- **图片**：至少提供 5 张高质量横图和方图。\n- **视频**：强烈建议上传时长超过 10 秒的 YouTube 视频，否则系统会自动生成低质量视频。\n- **文字**：提供涵盖不同卖点的长短标题。\n\n## 3. 避坑指南\n\n不要在 PMax 刚上线的前两周频繁修改预算，给机器学习足够的探索时间。",
            "en_content": "## 1. What is PMax?\n\nPerformance Max allows advertisers to access all Google Ads inventory from a single campaign.\n\n## 2. Asset Best Practices\n\n- **Images**: Provide at least 5 high-quality landscape and square images.\n- **Videos**: Highly recommend uploading YouTube videos longer than 10 seconds.\n- **Text**: Provide short and long headlines covering different selling points.\n\n## 3. Pitfalls to Avoid\n\nDo not frequently change the budget during the first two weeks of a PMax campaign."
        },
        {
            "category": "update",
            "title": "以渔数媒虚拟卡系统新增批量发卡功能",
            "title_en": "Yiyu Virtual Card System Adds Batch Issuance Feature",
            "summary": "为满足大型投放团队需求，以渔资金管理后台现已支持一键生成并绑定数百张虚拟卡。",
            "summary_en": "To meet the needs of large media buying teams, the backend now supports batch issuance of virtual cards.",
            "keywords": "虚拟卡, 批量发卡, 资金管理, 产品更新",
            "zh_content": "## 1. 批量发卡功能上线\n\n为了解决大型团队手动开卡效率低下的问题，以渔数媒正式推出**批量发卡**功能。\n\n## 2. 操作指南\n\n在“卡片管理”模块点击“批量操作”，上传包含卡片别名、限额等信息的 Excel 模板，即可在 10 秒内完成多达 500 张卡片的创建与分配。\n\n## 3. 安全性保障\n\n批量发卡同样受制于风控系统，所有卡片默认开启 3D Secure 验证，保障资金安全。",
            "en_content": "## 1. Batch Issuance Feature Launched\n\nTo solve the inefficiency of manual card creation, Yiyu officially launched the **Batch Issuance** feature.\n\n## 2. User Guide\n\nClick 'Batch Operations' in the Card Management module, upload an Excel template, and create up to 500 cards in 10 seconds.\n\n## 3. Security Guarantee\n\nAll cards default to 3D Secure verification to ensure fund safety."
        },
        {
            "category": "insight",
            "title": "AI赋能出海：如何利用大模型批量生成多语种广告文案",
            "title_en": "AI in Global Expansion: Generating Multilingual Ad Copy with LLMs",
            "summary": "探讨如何使用大语言模型（如ChatGPT/MiniMax）降低本地化翻译成本，提升广告A/B测试效率。",
            "summary_en": "Explore how to use LLMs to reduce localization costs and boost ad A/B testing efficiency.",
            "keywords": "AI出海, 广告文案, 大模型, 本地化",
            "zh_content": "## 1. 本地化翻译的痛点\n\n出海企业在进入中东、拉美等小语种市场时，高昂的翻译成本和漫长的交付周期往往拖慢了投放节奏。\n\n## 2. AI 带来的变革\n\n现代大语言模型不仅能提供准确的语法翻译，还能理解当地的**俚语和流行文化**。\n\n## 3. Prompt (提示词) 技巧\n\n> “你是一个巴西当地的资深营销专家，请将以下产品卖点翻译成葡萄牙语，要求语言极具煽动性，适合 TikTok 短视频的口播风格。”\n\n通过设定角色和场景，AI 生成的文案转化率甚至能超过初级本土优化师。",
            "en_content": "## 1. Pain Points of Localization\n\nHigh translation costs and long delivery cycles often slow down media buying in non-English markets.\n\n## 2. The AI Revolution\n\nModern LLMs not only provide accurate grammar but also understand local **slang and pop culture**.\n\n## 3. Prompting Tips\n\n> \"You are a senior marketing expert in Brazil. Translate these selling points into Portuguese with a highly persuasive tone suitable for TikTok.\"\n\nBy setting roles and contexts, AI-generated copy can outperform junior local optimizers."
        }
    ]
    
    for data in articles:
        seed = random.randint(100, 9999)
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        c.execute('''
            INSERT INTO articles (category_id, title, summary, content, date, views, image, seo_keywords, title_en, summary_en, content_en)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data["category"],
            data["title"],
            data["summary"],
            data["zh_content"],
            date_str,
            random.randint(500, 2000),
            f'https://picsum.photos/seed/yiyu{seed}/800/500',
            data["keywords"],
            data["title_en"],
            data["summary_en"],
            data["en_content"],
        ))
        
    conn.commit()
    conn.close()
    print('成功追加了剩余的 5 篇今日文章，凑齐 6 篇！')

if __name__ == '__main__':
    add_5_articles()