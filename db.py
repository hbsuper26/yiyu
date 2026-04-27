import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'yiyu.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Create articles table
    c.execute('''
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id TEXT NOT NULL,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            content TEXT NOT NULL,
            date TEXT NOT NULL,
            views INTEGER DEFAULT 0,
            image TEXT NOT NULL,
            seo_keywords TEXT DEFAULT '',
            seo_score INTEGER DEFAULT 0
        )
    ''')
    
    # Insert some initial dummy data if the table is empty
    c.execute('SELECT COUNT(*) FROM articles')
    if c.fetchone()[0] == 0:
        initial_articles = [
            (
                'news',
                'Meta 广告账户充值通道全面升级，秒级到账体验',
                '为了提升出海企业的资金流转效率，以渔数媒今日正式完成对 Meta 广告充值通道的底层架构升级，现已支持7x24小时秒级到账。',
                '''为了提升出海企业的资金流转效率，以渔数媒今日正式完成对 Meta 广告充值通道的底层架构升级。新系统采用全新的直连 API 方案，彻底告别人工审核与网关延迟，现已全面支持7x24小时秒级到账。

## 升级背景：跨境广告资金的效率痛点
在过去的两年里，我们收到了大量出海广告主的反馈。由于时差、网关结算周期以及传统代理商的人工审核流程，企业在投放关键节点（如大促、爆量期）往往会面临"有钱充不进去"的尴尬局面。资金链的卡顿，直接导致了广告组掉量、甚至错失市场机会。

> "时间就是ROI。当我们的 TikTok 素材跑出 1:5 的回报时，我们最怕的就是账户突然余额不足，而代理商恰好下班了。" —— 某头部出海游戏发行负责人

## 本次升级的三大核心优势
针对上述痛点，以渔技术团队耗时 3 个月，重构了与海外清算银行及媒体方（Meta, Google, TikTok等）的对接链路。

**1. 秒级极速到账**
资金划转指令毫秒级处理，充值成功后账户余额实时更新，不再等待。

**2. 7x24小时服务**
完全自动化的充值链路，打破周末和节假日限制，深夜爆量也能随时补足弹药。''',
                '2026-04-23',
                1240,
                'https://picsum.photos/seed/yiyu1/800/500'
            ),
            (
                'insight',
                '2026 Q1 全球出海广告投放趋势报告',
                '结合以渔平台一季度的资金流水数据，我们为您深度解析 TikTok 与 Google 渠道的获客成本变化及爆款素材趋势。',
                '''一季度已经过去，我们从以渔平台的聚合数据中，发现了一些值得关注的出海营销新趋势。

## 1. 获客成本(CAC)整体趋于平稳
相较于去年的大起大落，今年 Q1 的获客成本在北美和东南亚市场均表现出企稳态势。

## 2. 短视频素材的"黄金三秒"
在 TikTok 上，如果视频前 3 秒无法留住用户，后续的转化率将呈断崖式下跌。

我们建议出海企业在接下来的 Q2，将更多预算倾斜到创意素材的 A/B 测试中。''',
                '2026-04-20',
                3512,
                'https://picsum.photos/seed/yiyu2/800/500'
            )
        ]
        
        c.executemany('''
            INSERT INTO articles (category_id, title, summary, content, date, views, image)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', initial_articles)
        
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

if __name__ == '__main__':
    init_db()