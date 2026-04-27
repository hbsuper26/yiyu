import sqlite3
import random
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'yiyu.db')

def generate_mock_articles():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Clear old data
    c.execute('DELETE FROM articles')
    
    articles_data = [
        {
            "category": "guide",
            "title": "TikTok 短视频广告出海投放策略与ROI提升",
            "title_en": "TikTok Short Video Ad Strategies & ROI Boost for Global Expansion",
            "summary": "解析TikTok算法推荐机制，利用本地化UGC内容与创意钩子，实现ROI的倍数级增长。",
            "summary_en": "Analyze TikTok's algorithm to multiply ROI using localized UGC and creative hooks.",
            "keywords": "TikTok, 短视频, ROI, UGC, 出海营销",
            "zh_content": """## 1. TikTok 算法解析：从公域到私域

在短视频时代，TikTok 的核心魅力在于其强大的**兴趣分发算法**。与传统的搜索广告不同，TikTok 属于“货找人”的逻辑。
要提升 ROI，第一步就是顺应算法：
- **完播率**：前 3 秒的视觉冲击力决定了用户是否滑走。
- **互动率**：点赞、评论和分享是算法衡量素材优质与否的核心指标。

## 2. 本地化 UGC 的威力

“不要看起来像个广告（Don't make ads, make TikToks）” 是官方的核心倡导。
出海企业在制作素材时，往往容易陷入“自嗨”的精美包装中。实际上，采用当地网红（KOC）的真实评测、开箱展示或者生活化场景植入，转化率往往比精美的棚拍视频高出 **300%**。

### 实操建议：
1. 建立海外素人短视频素材库。
2. 使用原生贴纸、热门音乐和趋势特效。
3. 结合 Hashtag Challenge（话题挑战赛）引爆自然流量。

## 3. 破局：从低效买量到长效经营

短视频投放不能只看单次转化，还要结合**落地页优化**。确保视频中的卖点与独立站的着陆页高度一致，减少跳转流失，才是提升最终 ROI 的关键。""",
            "en_content": """## 1. TikTok Algorithm Demystified

In the short-video era, TikTok's core strength lies in its **interest-based distribution algorithm**. Unlike traditional search ads, TikTok operates on a "product finds the user" logic.
To boost ROI, align with the algorithm:
- **Completion Rate**: The visual impact of the first 3 seconds determines if a user scrolls away.
- **Engagement Rate**: Likes, comments, and shares are key metrics for assessing creative quality.

## 2. The Power of Localized UGC

"Don't make ads, make TikToks" is the platform's core mantra.
Global brands often fall into the trap of over-producing ads. In reality, authentic reviews, unboxing, or lifestyle integrations by local micro-influencers (KOCs) can yield a **300%** higher conversion rate than polished studio shoots.

### Actionable Advice:
1. Build a library of raw, localized video assets.
2. Use native stickers, trending sounds, and effects.
3. Leverage Hashtag Challenges to trigger organic virality.

## 3. Breakthrough: From Inefficient Buying to Long-Term Growth

Short-video ad campaigns shouldn't just focus on one-time conversions. **Landing page optimization** is equally crucial. Ensuring that the selling points in the video perfectly match the landing page reduces bounce rates and is key to ultimately boosting ROI."""
        },
        {
            "category": "news",
            "title": "Google Ads 搜索广告账户防封技巧与申诉",
            "title_en": "Google Ads Account Anti-ban Tips & Appeal Guide",
            "summary": "针对近期Google风控收紧，梳理常见的规避系统违规原因及详细的申诉流程与预防机制。",
            "summary_en": "Address recent Google risk controls with reasons for system circumvention and a detailed appeal process.",
            "keywords": "Google Ads, 防封, 规避系统, 申诉, 风控",
            "zh_content": """## 1. 为什么你的 Google 账户总被封？

近期，Google Ads 的风控政策进一步收紧，大量出海企业遭遇了“规避系统（Circumventing Systems）”的封号提示。
这往往不是因为恶意违规，而是因为**不合规的账户操作习惯**：
- 多个账户共用同一张虚拟信用卡或同一个 IP 环境。
- 落地页存在跳转代码、隐藏文本或是未完善的隐私政策（Privacy Policy）。
- 短期内频繁大幅度修改广告预算和出价。

## 2. 核心防封要素与资产隔离

要想在 Google Ads 生态中长期稳定投放，**资产隔离**是重中之重。

> "鸡蛋不要放在一个篮子里，但更重要的是，不要让系统认为这些篮子属于同一个人。"

### 解决方案：
1. **环境隔离**：使用纯净的指纹浏览器和独立的住宅 IP 登录不同账户。
2. **资金合规**：使用企业级的海外资金管理系统（如以渔数媒提供的专属开户及虚拟卡服务），确保账单地址与付款人信息的一致性。
3. **网站审查**：确保你的独立站具有清晰的退换货条款、联系方式及无欺诈性声明。

## 3. 申诉流程全解析

一旦不幸被封，不要盲目重复提交申诉。
正确的做法是：**先排查，后整理证据，最后写一封逻辑清晰的英文申诉信。**
附上你的营业执照、业务模式说明、以及你为了修正错误所做的具体改动截图。真诚且专业的态度，是解封的唯一途径。""",
            "en_content": """## 1. Why Do Your Google Accounts Keep Getting Banned?

Recently, Google Ads has tightened its risk control policies, leaving many cross-border enterprises with "Circumventing Systems" account suspensions.
This is often not due to malicious intent, but rather **non-compliant account management habits**:
- Sharing a single virtual credit card or IP environment across multiple accounts.
- Landing pages containing redirect scripts, hidden text, or incomplete Privacy Policies.
- Frequent, massive changes to ad budgets and bids within a short period.

## 2. Core Anti-Ban Elements and Asset Isolation

For long-term, stable advertising within the Google Ads ecosystem, **asset isolation** is paramount.

> "Don't put all your eggs in one basket, but more importantly, don't let the system think all the baskets belong to the same person."

### Solutions:
1. **Environment Isolation**: Use clean anti-detect browsers and dedicated residential IPs for different accounts.
2. **Financial Compliance**: Utilize enterprise-level global fund management systems (like Yiyu Digital Media's exclusive account opening and virtual card services) to ensure billing and payer information match.
3. **Website Audits**: Ensure your site has clear return/refund policies, contact info, and zero deceptive claims.

## 3. Comprehensive Appeal Process

If suspended, do not blindly submit repetitive appeals.
The correct approach: **Investigate first, gather evidence, and write a logically sound English appeal letter.**
Include your business license, a description of your business model, and screenshots of the specific changes you made to rectify the issue. A sincere, professional attitude is the only path to recovery."""
        },
        {
            "category": "insight",
            "title": "Meta (Facebook) 广告高转化素材设计指南",
            "title_en": "Meta (Facebook) High-Conversion Creative Design Guide",
            "summary": "掌握Meta视觉层级原理，克服素材疲劳，利用轮播图与视频广告提升点击率与转化率。",
            "summary_en": "Master Meta's visual hierarchy to overcome ad fatigue and boost CTR and conversions.",
            "keywords": "Meta广告, 素材设计, CTR, 转化率, 视觉层级",
            "zh_content": """## 1. 视觉钩子：前三秒定生死

在 Meta（Facebook/Instagram）的信息流中，用户滑过一条动态的平均时间不足 **1.5秒**。
如果你的素材不能在这个极短的时间内抓住眼球，再好的产品也会被淹没。

- **高对比度色彩**：使用与 Facebook 蓝色主色调形成反差的暖色（如橙色、黄色）来吸引注意力。
- **直击痛点**：视频的开场不要放 Logo，而是直接抛出用户面临的问题，或者展示震撼的使用效果。

## 2. 避免素材疲劳的轮换策略

即使是爆款素材，在连续跑了 2-3 周后，也会不可避免地遭遇**素材疲劳（Ad Fatigue）**，导致 CPA（获客成本）飙升。

### 应对方法：
1. **微调迭代**：保留核心视频内容，仅更换视频的前 3 秒 Hook、背景音乐或是封面图。
2. **格式多样化**：不要只投单视频。将表现好的视频截图，配上卖点文案，制作成轮播图（Carousel）或单图广告，覆盖不同偏好的受众。

## 3. 互动型广告的崛起

如今的消费者越来越抵触生硬的推销。
尝试在你的广告中加入互动元素：
- **投票贴**：让用户在两个产品中做出选择。
- **AR 试穿/试用**：利用 Meta 的 Spark AR 技术，让用户在广告中直接体验产品。
只有让用户参与进来，才能建立更深的情感连接，从而推动最终的转化。""",
            "en_content": """## 1. Visual Hooks: The First 3 Seconds Decide Your Fate

In the Meta (Facebook/Instagram) news feed, the average time a user spends scrolling past a post is less than **1.5 seconds**.
If your creative cannot grab attention in this extremely short window, even the best product will go unnoticed.

- **High-Contrast Colors**: Use warm colors (like orange or yellow) that contrast with Facebook's primary blue to draw the eye.
- **Directly Address Pain Points**: Don't start your video with a logo. Immediately present a problem the user faces or show a stunning visual of the product's effect.

## 2. Rotation Strategies to Avoid Ad Fatigue

Even winning creatives will inevitably suffer from **Ad Fatigue** after running for 2-3 weeks, causing CPAs (Cost Per Acquisition) to skyrocket.

### Countermeasures:
1. **Micro-Iterations**: Keep the core video content, but swap out the first 3-second hook, background music, or thumbnail.
2. **Format Diversification**: Don't rely solely on single videos. Take screenshots of high-performing videos, add selling point copy, and turn them into Carousel or Single Image ads to reach audiences with different preferences.

## 3. The Rise of Interactive Ads

Today's consumers are increasingly resistant to hard selling.
Try incorporating interactive elements into your ads:
- **Polls**: Ask users to choose between two products.
- **AR Try-ons**: Utilize Meta's Spark AR technology to let users experience the product directly within the ad.
Only by engaging the user can you build a deeper emotional connection, which ultimately drives conversion."""
        },
        {
            "category": "insight",
            "title": "海外游戏发行的买量成本(CAC)深度分析",
            "title_en": "In-depth Analysis of User Acquisition Costs (CAC) in Global Game Publishing",
            "summary": "透视全球游戏市场买量现状，平衡LTV与CAC的黄金比例，探索低成本获客的新渠道。",
            "summary_en": "Analyze global game UA markets, balance the LTV/CAC ratio, and explore low-cost acquisition channels.",
            "keywords": "游戏出海, CAC, 买量成本, LTV, 获客",
            "zh_content": """## 1. 游戏买量成本的严峻现状

2026年，全球手游市场的存量博弈愈演愈烈。特别是对于重度 SLG 和 RPG 游戏，北美和日韩等 T1 市场的单用户获取成本（CAC）已经突破了历史高点。
传统的“洗流量”模式已经失效，游戏发行商面临着巨大的利润压缩挑战。

## 2. LTV 与 CAC 的黄金比例

在买量发行的财务模型中，**LTV（用户生命周期价值） > CAC** 是铁律。
但很多企业忽略了回收周期的问题。

> "如果你的 LTV 需要 12 个月才能覆盖 CAC，那你的现金流在第 3 个月就会断裂。"

### 优化策略：
- **前置付费点**：通过新手礼包、首充优惠等设计，将用户的首付时间压缩到前 3 天。
- **精细化事件归因**：不要只优化“安装（Install）”，必须向广告平台回传“完成深度事件（如到达10级、首次购买）”的数据，利用 AEO/VO 跑出高价值大 R 玩家。

## 3. 破圈：跨界联动与达人营销

为了降低对传统买量渠道的依赖，越来越多的游戏厂商开始探索品效合一的破圈玩法。
通过与当地知名动漫 IP 联动，或是邀请 YouTube 游戏主播进行专场直播，虽然前期的品牌曝光成本较高，但随之而来的长尾自然量（Organic Traffic）能极大程度地摊薄整体的综合获客成本。""",
            "en_content": """## 1. The Harsh Reality of Game UA Costs

In 2026, the zero-sum game in the global mobile gaming market has intensified. Particularly for mid-core and hardcore SLG and RPG titles, the Customer Acquisition Cost (CAC) in T1 markets like North America, Japan, and South Korea has broken historical highs.
The traditional "traffic washing" model is obsolete, leaving game publishers facing massive profit margin compression.

## 2. The Golden Ratio of LTV to CAC

In the financial modeling of UA publishing, **LTV (Life Time Value) > CAC** is an unbreakable rule.
However, many companies ignore the payback period.

> "If your LTV takes 12 months to cover the CAC, your cash flow will break by month 3."

### Optimization Strategies:
- **Front-loaded Monetization**: Compress the user's first payment window to the first 3 days through beginner packs and first-top-up discounts.
- **Granular Event Attribution**: Don't just optimize for "Installs." You must pass back data for "Deep Funnel Events" (e.g., reaching level 10, first purchase) to the ad network, leveraging AEO/VO to find high-value whales.

## 3. Breaking Boundaries: Cross-overs and Influencer Marketing

To reduce reliance on traditional UA channels, more publishers are exploring brand-performance integrated strategies.
Collaborating with well-known local anime IPs, or inviting YouTube gaming influencers for dedicated livestreams, may incur high initial branding costs. However, the subsequent long-tail organic traffic significantly dilutes the overall blended acquisition cost."""
        },
        {
            "category": "update",
            "title": "出海电商独立站引流最新玩法与转化优化",
            "title_en": "Latest Traffic Acquisition Tactics & Conversion Optimization for Global E-commerce",
            "summary": "摆脱平台内卷，构建独立站品牌私域。探讨SEO驱动、弃单挽回及邮件营销的实战技巧。",
            "summary_en": "Escape platform competition by building independent brand domains. Explore SEO, cart abandonment, and email marketing.",
            "keywords": "独立站, 电商出海, 转化优化, 弃单挽回, SEO",
            "zh_content": """## 1. 摆脱平台依赖：独立站的崛起

随着亚马逊等第三方电商平台的合规要求愈发严苛、平台抽成增加，建立属于自己的 Shopify 或 WooCommerce **独立站**，沉淀品牌私域资产，已成为出海商家的必然选择。
然而，独立站最大的痛点在于：**流量从哪里来？**

## 2. SEO 与内容营销的双轮驱动

单纯依赖 Facebook 或 Google 的付费广告，利润空间会被不断挤压。
建立长效机制的关键在于 **SEO（搜索引擎优化）**：
- **博客策略**：围绕产品撰写使用教程、对比评测等长尾词文章（例如：“2026最佳户外露营帐篷推荐”）。
- **反向链接（Backlinks）**：与海外垂直领域的媒体和测评博客合作，提升网站的域名权重（DR）。

## 3. 转化率优化的魔鬼细节

引来了流量，却没人买单？你需要关注独立站的内部转化漏斗。

### 3.1 弃单挽回（Abandoned Cart Recovery）
高达 70% 的用户会在购物车页面流失。
- 部署自动化的邮件（EDM）或短信（SMS）追回序列。
- 在用户离开前 1 小时发送一封带有 10% 专属折扣码的提醒邮件。

### 3.2 提升网站信任度
海外消费者极其看重购物安全。
在结算页面显眼位置放置 PayPal、Visa 等支付渠道的信任徽章（Trust Badges），并展示来自真实客户的带图带星级评论（Reviews），能有效打消用户的付款疑虑。""",
            "en_content": """## 1. Escaping Platform Dependency: The Rise of Independent Sites

As third-party e-commerce platforms like Amazon enforce stricter compliance and take higher commissions, building an independent site via Shopify or WooCommerce to accumulate private brand assets has become a necessary choice for global merchants.
However, the biggest pain point of independent sites is: **Where does the traffic come from?**

## 2. The Dual Engine of SEO and Content Marketing

Relying solely on paid ads from Facebook or Google constantly squeezes profit margins.
The key to establishing a long-term mechanism is **SEO (Search Engine Optimization)**:
- **Blog Strategy**: Write long-tail keyword articles around your products, such as tutorials or comparative reviews (e.g., "Best Outdoor Camping Tents in 2026").
- **Backlinks**: Partner with niche overseas media and review blogs to increase your website's Domain Rating (DR).

## 3. The Devil in the Details of Conversion Optimization

Driving traffic but getting no sales? You need to focus on your site's internal conversion funnel.

### 3.1 Abandoned Cart Recovery
Up to 70% of users drop off at the cart page.
- Deploy automated Email (EDM) or SMS recovery sequences.
- Send a reminder email with an exclusive 10% discount code 1 hour after the user abandons the cart.

### 3.2 Boosting Website Trust
Overseas consumers highly value shopping security.
Placing Trust Badges for payment gateways like PayPal and Visa prominently on the checkout page, and displaying photo and star-rated reviews from real customers, effectively dispels payment hesitations."""
        },
        {
            "category": "update",
            "title": "企业级海外资金管理系统如何解决汇损问题",
            "title_en": "How Enterprise Global Fund Management Systems Solve FX Loss Issues",
            "summary": "剖析跨境支付中的隐形利润杀手，介绍以渔数媒虚拟卡矩阵与多币种账户的高效资金解决方案。",
            "summary_en": "Analyze the hidden profit killers in cross-border payments and introduce Yiyu's virtual card and multi-currency solutions.",
            "keywords": "资金管理, 汇损, 虚拟卡, 跨境支付, 以渔数媒",
            "zh_content": """## 1. 隐形的利润杀手：汇率损耗与手续费

对于月消耗在百万美金级别的大型出海企业而言，跨境资金的流转效率和成本直接关系到公司的生死存亡。
传统的跨境汇款和企业信用卡支付，往往伴随着两个巨大的痛点：
- **多次汇率转换（汇损）**：从人民币换成美元，再从美元换成当地币种支付广告费，中间的汇损可能高达 2%-3%。
- **高昂的跨境手续费**：每笔交易都被银行或支付网关收取额外的手续费用。

## 2. 虚拟信用卡矩阵的作用

为了应对复杂的海外媒体广告平台扣款机制，**虚拟信用卡（VCC）矩阵**成为了企业的标配。
企业可以通过资金管理后台，瞬间生成成百上千张虚拟卡，并为每个广告账户绑定独立卡片。
- **防止连坐封号**：一张卡仅对应一个账户，一旦某个账户因违规被封停，资金风险被隔离，不会波及其他健康账户。
- **精准的预算控制**：可以为每张虚拟卡设定每日/每月的交易限额，杜绝广告跑飞导致的超额扣款。

## 3. 以渔数媒的资金管理方案

作为专业的出海服务商，**以渔数媒** 提供的不仅是广告开户，更是一套完整的企业级资金流转底层基础设施。

我们提供：
1. **多币种本地收款账户**：支持美元、欧元、英镑等主流货币的无损原币种入账。
2. **极速充值通道**：通过 API 直连全球清算网络，实现广告费的秒级到账，确保旺季投放绝不断粮。
3. **透明的汇率机制**：采用实时极优汇率报价，告别隐形加价，将每一分利润都留在企业内部。""",
            "en_content": """## 1. The Hidden Profit Killer: FX Losses and Transaction Fees

For large global enterprises spending millions of dollars monthly, the efficiency and cost of cross-border fund transfers are a matter of life and death.
Traditional cross-border wire transfers and corporate credit card payments often come with two massive pain points:
- **Multiple Currency Conversions (FX Loss)**: Converting from RMB to USD, then from USD to local currency to pay for ads, can result in FX losses of up to 2%-3%.
- **Exorbitant Cross-Border Fees**: Extra fees are charged by banks or payment gateways on every single transaction.

## 2. The Role of Virtual Credit Card Matrices

To cope with the complex billing mechanisms of overseas ad platforms, a **Virtual Credit Card (VCC) Matrix** has become standard for enterprises.
Through a fund management backend, companies can instantly generate hundreds of virtual cards and bind unique cards to each ad account.
- **Preventing Chain Bans**: One card strictly corresponds to one account. If an account is suspended for policy violations, the financial risk is isolated and won't affect other healthy accounts.
- **Precise Budget Control**: Daily/monthly transaction limits can be set for each virtual card, eliminating overcharging caused by runaway ad campaigns.

## 3. Yiyu Digital Media's Fund Management Solution

As a professional global service provider, **Yiyu Digital Media** offers more than just ad account opening; we provide a complete enterprise-level fund transfer infrastructure.

We offer:
1. **Multi-Currency Local Receiving Accounts**: Support lossless, original-currency deposits for major currencies like USD, EUR, and GBP.
2. **Lightning-Fast Recharge Channels**: API direct connections to global clearing networks enable second-level crediting of ad funds, ensuring campaigns never run dry during peak seasons.
3. **Transparent FX Mechanisms**: Utilizing real-time, highly competitive exchange rates, we say goodbye to hidden markups, keeping every cent of profit within your enterprise."""
        }
    ]
    
    for i, data in enumerate(articles_data):
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
            random.randint(100, 5000),
            f'https://picsum.photos/seed/yiyu{seed}/800/500',
            data["keywords"],
            data["title_en"],
            data["summary_en"],
            data["en_content"],
        ))
        
    conn.commit()
    conn.close()
    print('成功插入 6 篇内容各异的测试文章！')

if __name__ == '__main__':
    generate_mock_articles()