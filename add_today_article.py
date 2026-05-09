import sqlite3
import random
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'yiyu.db')

def add_today_mock_article():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    data = {
        "category": "news",
        "title": f"【今日更新】以渔数媒发布最新智能分析引擎",
        "title_en": "Yiyu Digital Media Releases New Smart Analysis Engine",
        "summary": "以渔数媒今日正式上线了基于AI的广告数据智能分析引擎，助力出海企业精准提升ROI。",
        "summary_en": "Yiyu Digital Media officially launched its AI-based ad data smart analysis engine today to help global enterprises accurately boost ROI.",
        "keywords": "AI分析, 广告数据, ROI, 产品更新, 以渔数媒",
        "zh_content": """## 1. 智能分析引擎正式上线

随着出海营销进入精细化运营阶段，以渔数媒今日宣布，全新的**智能数据分析引擎**正式上线。该引擎深度集成了先进的机器学习算法，旨在为企业提供更精准的流量洞察。

## 2. 核心功能亮点

- **实时预警系统**：毫秒级监控广告账户的消耗异常，自动触发防超额扣款保护。
- **多维度ROI归因**：打通独立站、应用商店与各大媒体平台的转化数据，让每一分预算的去向都清晰可见。
- **素材生命周期预测**：基于历史表现，预测创意素材的疲劳周期，提前建议优化替换。

> “在存量竞争时代，数据就是出海企业最锐利的武器。”

## 3. 客户赋能与未来展望

目前，该功能已向所有企业级客户免费开放测试。未来，我们将继续深耕技术底层，结合最新的 AI 大模型，为广告主提供一键生成优化策略的闭环服务。""",
        "en_content": """## 1. Official Launch of Smart Analysis Engine

As global marketing enters an era of refined operations, Yiyu Digital Media announced today the official launch of its new **Smart Data Analysis Engine**. This engine deeply integrates advanced machine learning algorithms to provide enterprises with more accurate traffic insights.

## 2. Core Feature Highlights

- **Real-time Alert System**: Millisecond-level monitoring of ad account spend anomalies, automatically triggering protection against overcharging.
- **Multi-dimensional ROI Attribution**: Bridging conversion data across independent sites, app stores, and major media platforms, making the destination of every cent clear.
- **Creative Lifecycle Prediction**: Based on historical performance, it predicts the fatigue cycle of creative assets and suggests optimizations in advance.

> "In the era of zero-sum competition, data is the sharpest weapon for global enterprises."

## 3. Empowering Clients & Future Outlook

Currently, this feature is open for free beta testing to all enterprise clients. In the future, we will continue to deepen our underlying technology and integrate the latest large AI models to provide advertisers with a closed-loop service for one-click optimization strategies."""
    }
    
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
    print('成功追加了1篇今日的更新文章！')

if __name__ == '__main__':
    add_today_mock_article()