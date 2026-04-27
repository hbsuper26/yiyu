import sqlite3
import random
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'yiyu.db')

def generate_mock_articles():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Clear old data so we only see bilingual mock data
    c.execute('DELETE FROM articles')
    
    topics = [
        'TikTok 短视频广告出海投放策略与ROI提升', 
        'Google Ads 搜索广告账户防封技巧与申诉', 
        'Meta (Facebook) 广告高转化素材设计指南', 
        '海外游戏发行的买量成本(CAC)深度分析', 
        '出海电商独立站引流最新玩法与转化优化', 
        '企业级海外资金管理系统如何解决汇损问题'
    ]
    
    en_topics = [
        'TikTok Short Video Ad Strategies & ROI Boost for Global Expansion',
        'Google Ads Account Anti-ban Tips & Appeal Guide',
        'Meta (Facebook) High-Conversion Creative Design Guide',
        'In-depth Analysis of User Acquisition Costs (CAC) in Global Game Publishing',
        'Latest Traffic Acquisition Tactics & Conversion Optimization for Global E-commerce',
        'How Enterprise Global Fund Management Systems Solve FX Loss Issues'
    ]
    
    for i, topic in enumerate(topics):
        seed = random.randint(100, 9999)
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        zh_content = f"""## 1. 行业背景与核心观点

随着全球化进程的不断推进，**{topic}** 已经成为众多出海企业关注的核心焦点。在当前竞争激烈的市场环境下，传统的买量方式和粗放式运营已经无法满足企业对 ROI（投资回报率）的追求。

根据最新的市场调研数据，2026年出海营销的整体成本较往年上涨了约 15%，这就要求我们在制定出海策略时，必须更加精细化和数据驱动。

## 2. 深度分析与破局策略

在探讨具体的执行方案之前，我们需要先明确几个关键痛点：
- **流量红利见顶**：优质渠道的获客成本不断攀升。
- **本地化挑战**：不同国家和地区的文化差异导致素材转化率存在巨大波动。
- **合规与风控**：平台政策收紧，账户封禁风险增加。

### 2.1 精细化受众定位
通过搭建第一方数据中台，结合 AI 算法模型，我们可以对目标受众进行更深层次的标签化处理。这不仅仅是基于年龄、性别等基础人口统计学特征，更是基于用户的行为意图和消费习惯。

### 2.2 创意素材的 A/B 测试矩阵
素材是直接决定点击率（CTR）的核心要素。建议企业建立模块化的素材库，将视频/图片的开头前3秒、核心卖点展示、CTA（行动呼吁）按钮进行排列组合，通过高频次的 A/B 测试跑出爆款模型。

> "在数字化营销的下半场，谁能更快速地迭代创意，谁就能掌握流量的密码。" —— 以渔数媒研究院

## 3. 落地执行建议

1. **建立全链路追踪机制**：从前端点击到后端转化，确保每一个节点的数据都是清晰且可归因的。
2. **引入自动化投放工具**：利用 API 接口实现批量上计划和实时调价，降低人力成本。
3. **重视风控与账户安全**：合理分配预算，建立多层级的账户矩阵以对冲不可预见的封控风险。

## 4. 总结与展望

**{topic}** 并不是一蹴而就的，它需要企业在战略上保持长期主义，在战术上保持敏捷迭代。以渔数媒将持续为您提供最前沿的行业洞察和专业的技术支持，助力您的产品成功走向世界。
"""

        en_content = f"""## 1. Industry Background & Core Insights

As globalization accelerates, **{en_topics[i]}** has become a central focus for many expanding enterprises. In today's highly competitive market, traditional user acquisition methods and extensive operations are no longer sufficient to meet ROI expectations.

According to recent market research, overall global marketing costs in 2026 have increased by approximately 15% compared to previous years. This demands a more refined, data-driven approach when formulating global expansion strategies.

## 2. In-depth Analysis & Breakthrough Strategies

Before discussing specific execution plans, we must identify key pain points:
- **Peak Traffic Dividends**: The cost of acquiring users through premium channels continues to rise.
- **Localization Challenges**: Cultural differences across regions cause massive fluctuations in creative conversion rates.
- **Compliance & Risk Control**: Stricter platform policies increase the risk of account bans.

### 2.1 Refined Audience Targeting
By building a first-party data platform and integrating AI algorithms, we can achieve deeper tagging of target audiences. This goes beyond basic demographics like age and gender, focusing heavily on user behavioral intent and consumption habits.

### 2.2 A/B Testing Matrix for Creative Assets
Creatives are the core element directly determining Click-Through Rates (CTR). We recommend establishing a modular creative library, mixing and matching the first 3 seconds of videos/images, core selling points, and CTA (Call to Action) buttons. High-frequency A/B testing is essential to discover winning models.

> "In the second half of digital marketing, whoever iterates creatives the fastest holds the key to traffic." — Yiyu Digital Media Research Institute

## 3. Execution Recommendations

1. **Establish Full-Funnel Tracking**: Ensure data at every node, from front-end click to back-end conversion, is clear and attributable.
2. **Adopt Automated Ad Tech**: Utilize API integrations for batch campaign creation and real-time bidding to reduce manual labor costs.
3. **Prioritize Risk Control & Account Security**: Allocate budgets rationally and build a multi-tiered account matrix to hedge against unforeseen bans.

## 4. Conclusion & Outlook

Mastering **{en_topics[i]}** doesn't happen overnight. It requires a long-term strategic vision combined with agile tactical iterations. Yiyu Digital Media will continue to provide cutting-edge industry insights and professional technical support to help your products succeed globally.
"""

        c.execute('''
            INSERT INTO articles (category_id, title, summary, content, date, views, image, seo_keywords, title_en, summary_en, content_en)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            random.choice(['news', 'insight', 'guide', 'update']),
            topic,
            f'关于 {topic} 的最新行业洞察与核心实操指南，为您提供全方位的出海营销思路。',
            zh_content,
            date_str,
            random.randint(100, 5000),
            f'https://picsum.photos/seed/yiyu{seed}/800/500',
            '出海, 广告, 投放, 营销, 转化率',
            en_topics[i],
            f'Latest industry insights and core practical guides on {en_topics[i]}, providing comprehensive global marketing strategies.',
            en_content,
        ))
        
    conn.commit()
    conn.close()
    print('成功插入 6 篇测试文章！')

if __name__ == '__main__':
    generate_mock_articles()