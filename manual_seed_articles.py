﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿﻿import os
import sqlite3
from datetime import datetime


DB_PATH = os.path.join(os.path.dirname(__file__), "yiyu.db")
TODAY = datetime.now().strftime("%Y-%m-%d")


ARTICLES = [
    {
        "category_id": "news",
        "title": "2026 下半年 Meta 与 TikTok 开户政策变化：账户、资金、素材三线应对指南",
        "title_en": "H2 2026 Meta and TikTok Policy Changes: A Three-Layer Guide for Accounts, Funding, and Creatives",
        "summary": "Meta 与 TikTok 在 2026 年下半年同步强化开户审核、素材一致性和资金链路稽核。本文结合以渔服务案例，拆解企业如何用账户矩阵、预算前置与创意分层来稳定投放。",
        "summary_en": "Meta and TikTok are tightening account review, creative consistency, and funding verification in H2 2026. This article explains how advertisers can respond with stronger account architecture, funding buffers, and creative governance.",
        "seo_keywords": "Meta开户政策,TikTok广告审核,海外广告充值,广告账户风控,出海广告合规",
        "image": "https://picsum.photos/seed/yiyu-manual-101/800/500",
        "views": 2680,
        "intro_quote": "2026 年最危险的投放问题，已经不是买不到流量，而是明明预算在手，却因为开户、充值或素材稽核不同步，导致投放链路在临门一脚时断掉。",
        "overview": "过去很多团队把平台开户当作一次性动作，但平台在 2026 年下半年明显把审核逻辑从单点校验升级为全链路一致性校验。营业执照主体、商务管理平台、支付资料、公共主页、落地页品牌名和素材承诺之间，只要出现明显割裂，就容易触发限额、补件或人工复核。很多企业明明拥有不错的产品和素材，却在真正要放量时被底层链路绊住，这说明增长问题已经不再只是投放策略问题，而是经营链路设计问题。",
        "problem": "以渔服务客户时发现，最常见的高风险场景有三类。第一类是主体信息不一致，品牌邮箱、落地页品牌和付款抬头来自不同历史阶段，平台很容易将其识别为代理链过长或主体模糊。第二类是充值动作滞后，很多团队等到账户余额低于一天预算才补款，导致模型在学习期被迫中断。第三类是素材承诺与站点证明脱节，视频里强调折扣、发货和售后，但用户进入站点后找不到对应说明，短期 CTR 看似不错，长期健康度却持续下滑。",
        "framework": [
            "第一步是重做账户矩阵。不要再用一个主账户承接所有市场和所有阶段，而是至少拆成拓新、活动承接和重定向三层账户池。这样即使某一个账户进入复核，其余预算仍能继续承接转化，组织不会因为单点故障全面停摆。",
            "第二步是把资金预警前置。成熟团队通常把预警阈值设为过去 7 日平均消耗的 1.8 倍，并要求核心市场预留 3 到 5 天预算缓冲。这样做的价值并不是让账户里堆更多余额，而是让补款成为制度动作，而不是情绪化救火。",
            "第三步是建立素材承诺分层机制。品牌信任素材负责说明为什么可信，转化素材负责说明为什么值得行动，活动素材负责说明为什么现在就要下单。三类素材分别对应不同审核敏感点和不同站点证明材料，不能再用一套爆款脚本试图兼容所有场景。",
        ],
        "case": "一家跨境家居品牌在黑五前准备了 14 套视频和 6 个落地页，但由于 BM 主体和支付抬头历史不一致，账户连续出现小额补款失败和素材复核拉长。以渔协助其重做账户分组与预算阈值，并统一文案、物流和售后口径。两周后，首充与补款成功率从 82% 提升到 97%，审核时长从 19 小时降到 6 小时，活动稳定放量期从 4 天延长到 11 天，ROAS 从 2.1 提升到 2.8。这个案例证明，合规治理不是增长的阻力，而是放量的前提。",
        "metrics": [
            ("开户补件一次通过率", ">= 85%", "低于该值说明主体资料与站点表述未形成统一口径"),
            ("首充成功率", ">= 95%", "低于该值通常意味着支付通道、额度或主体匹配存在问题"),
            ("素材复核平均时长", "< 8 小时", "超过阈值会直接拖慢测试节奏和预算释放"),
            ("异常账户切换耗时", "< 30 分钟", "反映备用账户池与审批流程是否可执行"),
        ],
        "actions": [
            "先盘点所有主体和支付资料，把账户主体、站点品牌、支付抬头、公共主页命名和客服邮箱放到同一张表里，找出任何一个会被平台交叉识别为异常的断点。",
            "按市场和业务阶段拆分账户，把拓新、重定向和活动承接分到不同池子中，并为每一类账户配置不同的预算阈值与备用路径。",
            "在素材命名、活动编号和支付回执中引入统一字段，让设计、投手、财务和合规看到的是同一份状态面板，而不是四套互不相通的表格。",
        ],
    },
    {
        "category_id": "insight",
        "title": "东南亚与拉美广告账户资金效率基准：从充值成功率到回款周期的经营视角",
        "title_en": "Funding Efficiency Benchmarks in Southeast Asia and LATAM: From Recharge Success to Cash Recovery",
        "summary": "真正决定出海广告扩量上限的，不只是媒体流量成本，更是账户资金链路是否稳定。本文以东南亚与拉美市场为样本，拆解充值效率、拒付损失、回款周期和预算冗余的经营指标。",
        "summary_en": "The real cap on media scaling is often funding stability rather than traffic cost. This article benchmarks recharge efficiency, dispute loss, recovery cycles, and budget redundancy across Southeast Asia and LATAM.",
        "seo_keywords": "东南亚广告投放,拉美广告账户,充值成功率,广告资金管理,回款周期",
        "image": "https://picsum.photos/seed/yiyu-manual-102/800/500",
        "views": 2416,
        "intro_quote": "很多团队把花钱买量当成营销问题，但在出海业务里，预算能否高质量地流动，本身就是增长能力的一部分。",
        "overview": "如果把获客成本看作前台指标，那么充值成功率、退款争议率、回款周期和汇损比例就是后台指标。前台决定今天能买到多少流量，后台决定下个月还能不能继续加码。东南亚和拉美都是流量与支付同时碎片化的市场，看似机会很大，但只要资金链路设计不成熟，企业就会在放量阶段被隐性损耗吞掉利润。很多团队周报里充满了 CTR、CPA 和 ROAS，却根本没有把资金效率写进经营决策，这也是为什么规模上来以后反而更焦虑。",
        "problem": "东南亚常见的问题是同一个阈值管理多个国家，导致快周转市场补款不及时、慢周转市场余额长期闲置。拉美常见的问题则是把媒体回报看成净利润，却忽略拒付、结算延迟和换汇成本正在侵蚀现金流。还有一类团队把投放、财务、代理和运营分得过开，掉量时第一反应永远是素材或出价，却不知道真实问题可能出在回执延迟或本地支付链路阻塞。",
        "framework": [
            "按市场和业务模式重做资金地图。印尼、泰国、越南、巴西和墨西哥不该共用一套补款节奏，因为节假日、支付偏好和结算速度完全不同。市场越复杂，阈值越不能一刀切。",
            "把净回报纳入经营看板。任何一个看似高 ROAS 的市场，都必须同步审视拒付、税费和汇损，否则团队会被表面好看的广告回报带偏，误判真实利润空间。",
            "建立异常定位 SLA。首充成功率、2 小时到账率、回款周期中位数和月度汇损比例，应当成为经营层例会指标，而不是只留给财务或代理商单独追踪。",
        ],
        "case": "某家具品牌同时在泰国、越南、巴西和墨西哥投放，过去一直使用统一补款阈值。结果泰国和越南在周末活动爆量时常常来不及补款，巴西市场却长期维持过高余额，造成闲置与汇损并存。以渔帮助其按市场与业务模式拆分资金池，对快周转市场采用自动阈值补款，对长回款市场采用周度计划。改造后，2 小时到账率从 76% 提升到 95%，月度平均闲置余额下降 31%，整体净利润率提升 4.7 个百分点。",
        "metrics": [
            ("首充成功率", ">= 94%", "衡量链路可用性，尤其适合高频补款市场"),
            ("2 小时到账率", ">= 90%", "直接影响活动期预算承接能力"),
            ("回款周期中位数", "< 14 天", "周期过长会显著挤压扩量弹性"),
            ("月度汇损比例", "< 1.5%", "决定跨市场扩量后的真实利润留存"),
        ],
        "actions": [
            "先按市场和业务模型拆分账户，不要再按组织部门拆。让东南亚快周转市场与拉美长回款市场采用不同阈值和审批节奏。",
            "把净回报而非媒体回报作为周报核心。每个市场都要同步审视拒付、税费和汇损带来的利润侵蚀。",
            "建立一小时内可定位异常的工作流，让运营、财务和代理在同一条链路中闭环，而不是掉量后再翻聊天记录追责。",
        ],
    },
    {
        "category_id": "guide",
        "title": "TikTok Shop 冷启动投放作战手册：账户矩阵、预算节奏与素材迭代",
        "title_en": "TikTok Shop Cold-Start Playbook: Account Matrix, Budget Rhythm, and Creative Iteration",
        "summary": "TikTok Shop 冷启动不是简单地多上素材，而是要让账户矩阵、商品池、补款节奏与短视频迭代一起运作。本文给出首月投放的分阶段打法与可落地指标。",
        "summary_en": "A successful TikTok Shop cold start is not about uploading more creatives. It requires account matrix design, product pooling, funding rhythm, and disciplined creative iteration. This playbook maps the first 30 days.",
        "seo_keywords": "TikTok Shop冷启动,TikTok广告投放,账户矩阵,素材迭代,短视频带货",
        "image": "https://picsum.photos/seed/yiyu-manual-103/800/500",
        "views": 2879,
        "intro_quote": "在 TikTok Shop 里，真正决定冷启动能否跑起来的，不是第一条素材的偶然爆发，而是你能否用制度持续生产可被验证的下一条素材。",
        "overview": "很多团队把 TikTok Shop 冷启动理解成先投一点看看，于是账户、商品、达人素材、直播切片和支付预算全部临时拼凑。这样的结果通常是第一条视频也许能跑出点击，但第二条、第三条跟不上，模型还没建立稳定信号，团队就已经开始焦虑要不要换品或停投。高效冷启动必须围绕三个问题展开：账户矩阵如何承接不同目的预算，商品池如何形成可测试的层次，素材迭代如何在 72 小时内完成假设、上线、反馈和重构的闭环。",
        "problem": "最常见的失败不是预算不够，而是预算分配和创意节奏没有分层。很多团队首日把绝大部分预算打在单一素材和单一商品上，导致横向信号不足。还有一些团队每天上十几条视频，却说不清每条视频究竟测试的是开场、痛点、价格、场景还是证据。内容产量上去了，学习效率却没有上去，最后只能靠情绪化停投或盲目加价来试图挽救结果。",
        "framework": [
            "首月预算建议按 60% 测试、25% 放量、15% 活动预留来分配。测试预算负责横向信号，放量预算只承接已验证组合，活动预留预算负责热点素材和达人联动加速。",
            "账户至少准备三类池子：测款账户、测素材账户和承接账户。测款看商品点击与加购潜力，测素材看开场留存与点击效率，承接账户聚焦稳定 ROAS 与日预算上限。",
            "素材迭代按开场 3 秒、证据段和成交段三层结构组织。每 72 小时必须复盘一次本轮测试究竟改动了什么，并把变化与 CTR、CVR、加购率对应起来。",
        ],
        "case": "某美妆品牌冷启动初期每天上新素材超过 15 条，但所有预算都压在单一承接账户里，结果 CTR 看起来不错，成交却极不稳定。调整后，品牌建立了三层账户池，并把 12 个 SKU 划分为引流款、利润款和形象款。两周后，优质素材命中率从 8% 提升到 21%，加购成本下降 27%。到第 30 天，品牌在英国和马来西亚形成稳定内容节奏，每周新增 18 条结构化测试素材，保留 4 条放量素材和 2 条大促素材，整体 ROAS 从 1.4 提升到 2.6。",
        "metrics": [
            ("优质素材命中率", ">= 15%", "反映测试框架是否有效，而不是单条爆款运气"),
            ("72 小时复盘完成率", "100%", "确保每轮测试都有假设与结论"),
            ("2 小时补款响应率", ">= 95%", "热点素材出现后必须能及时承接预算"),
            ("加购成本周环比", "持续下降", "比单日 ROAS 更适合判断冷启动趋势"),
        ],
        "actions": [
            "第 1 周只做测款和测开场，不急着大预算承接，先找到用户愿意停留和点击的商品与镜头语言。",
            "第 2 周建立素材版本库，把痛点、证据和 CTA 模块化，确保团队能在 24 小时内产出新的验证版本。",
            "第 3 至 4 周再开启承接账户，把连续两天达到门槛的素材接入更高预算，同时保留测试池持续更新下一批候选素材。",
        ],
    },
    {
        "category_id": "guide",
        "title": "Google Ads 搜索 + Performance Max 协同投放：高客单出海品牌的漏斗重构",
        "title_en": "Search + Performance Max Synergy: Rebuilding the Funnel for High-Ticket Global Brands",
        "summary": "对高客单出海品牌来说，Google Ads 的关键不是单独优化 Search 或 PMax，而是让高意图词、品牌防御、再营销和素材资产共享同一套经营目标。本文拆解协同投放的设计方法。",
        "summary_en": "For high-ticket global brands, Google Ads performance improves when Search, brand defense, remarketing, and PMax share one commercial objective instead of being optimized in silos. This article explains how.",
        "seo_keywords": "Google Ads搜索广告,Performance Max,高客单品牌,出海投放,漏斗重构",
        "image": "https://picsum.photos/seed/yiyu-manual-104/800/500",
        "views": 2534,
        "intro_quote": "Search 负责接住最明确的需求，PMax 负责扩展高潜人群，但两者只有在同一套利润模型下协同时，才会真正形成放大量级。",
        "overview": "高客单出海品牌最常见的误区，是把 Search 看作转化渠道，把 PMax 看作扩量渠道，然后分别由不同同事、不同代理甚至不同周报体系管理。这样做的直接后果是 Search 在抢品牌词，PMax 在吃再营销，团队表面上看起来两个渠道都在转化，实际上只是在相互抬价并重复计算价值。真正成熟的协同方法，是先明确品牌当前处于需求收割优先还是新客扩张优先的经营阶段，再决定 Search 与 PMax 的角色边界。",
        "problem": "如果没有角色边界，任何自动化都会把最容易转化的人群反复吃透，而不是帮你打开新的增量。很多品牌的问题不是广告工具不够先进，而是线索回传过于表层，系统只知道谁提交了表单，却不知道谁成为了真正高质量商机。表面 ROAS 很好看，销售团队却在抱怨线索质量越来越差。自动化并没有错，错的是企业没有用经营目标去定义自动化边界。",
        "framework": [
            "预算上采用核心意图优先与增量实验可控的原则。品牌词、竞品词和高意图词是底盘预算，不能被 PMax 的短期漂亮数据挤占；PMax 应承担新客实验与中层需求拓展职责。",
            "把 CRM 评分、离线成交和有效商机标签回传到广告系统。否则平台最终只能优化到表单提交，而不是优化到企业真正需要的高质量商机。",
            "按受众阶段拆分内容资产。品牌认知资产讲痛点和方法，比较决策资产讲案例和 ROI，促成成交资产讲实施周期、报价透明度和服务保障。",
        ],
        "case": "某 B2B SaaS 品牌过去把 Search 交给效果团队，把 PMax 交给品牌团队，双方共享预算却不共享目标。调整后，品牌重新定义漏斗：Search 负责品牌词、高意图词和问题词，PMax 只承接新客实验与中层需求拓展；同时把 CRM 中的销售合格线索评分回传到广告后台。两个月内，无效点击比例下降 23%，PMax 新客占比提升 18%，销售合格率提升 31%。广告系统终于开始对高质量线索负责，而不是只对表单数量负责。",
        "metrics": [
            ("品牌词保护覆盖率", ">= 95%", "防止高意图流量被竞品截走"),
            ("PMax 新客占比", "持续上升", "衡量自动化是否真的在做增量"),
            ("销售合格线索率", ">= 30%", "高客单业务应优先看线索质量"),
            ("离线回传覆盖率", ">= 80%", "决定系统是否能学习真实收入目标"),
        ],
        "actions": [
            "先重画漏斗，把 Search 与 PMax 的职责界定清楚，不允许两个渠道继续争抢同一批用户。",
            "把销售反馈接入广告系统，至少让系统知道什么是合格线索，避免自动化持续优化低质量表单。",
            "建立双周复盘机制，同时审视搜索词、资产组、线索评分和站点内容，以经营目标为准而不是单一平台指标。",
        ],
    },
    {
        "category_id": "update",
        "title": "以渔数媒多账户资金看板升级说明：预算预警、批量充值与异常留痕全面增强",
        "title_en": "Yiyu Multi-Account Funding Dashboard Upgrade: Stronger Alerts, Bulk Top-Ups, and Exception Logs",
        "summary": "以渔数媒本周上线多账户资金看板升级版，重点增强预算预警、批量充值、异常留痕和审批协同，帮助团队把广告资金管理从人工救火升级为制度化运营。",
        "summary_en": "Yiyu has launched a major upgrade to its multi-account funding dashboard, improving alerting, bulk top-ups, exception logs, and approval collaboration so teams can move from reactive firefighting to systemized operations.",
        "seo_keywords": "资金看板,批量充值,预算预警,广告账户管理,以渔数媒更新",
        "image": "https://picsum.photos/seed/yiyu-manual-105/800/500",
        "views": 3122,
        "intro_quote": "很多企业并不缺预算，缺的是看见预算风险的能力，以及在风险到来前做出动作的能力。",
        "overview": "我们在服务客户时发现，广告资金管理最常见的低效并不是系统没有数据，而是信息分散在多个聊天群、Excel、充值回执和代理回复里。投手看到的是余额不足，财务看到的是待审批，老板看到的是 ROI 波动，但没有人能在第一时间知道问题究竟卡在预警、审批、补款还是到账确认。因此，本次以渔数媒多账户资金看板升级的核心不是多做几个图表，而是围绕企业真实流程重构资金协同方式。",
        "problem": "过去很多团队只记录结果，不记录过程。季度复盘时大家知道曾经有过资金问题，却不知道究竟是审批慢、通道不稳、代理响应迟还是账户结构本身不合理。还有一些企业在活动期使用静态阈值，平时会导致余额闲置，大促期又来不及补款。系统有数据，组织却无法基于数据行动，这正是资金看板需要被重新设计的原因。",
        "framework": [
            "预算预警从静态阈值升级为动态阈值。新版支持按过去 3 日、7 日平均消耗和活动档期设置不同规则，让团队把注意力优先放在真正危险的账户上。",
            "批量充值支持按账户组执行。运营可按市场、业务线或活动类型发起批量补款，财务与审批人看到的是聚合后的任务流，而不是几十条零散申请。",
            "异常留痕从结果记录升级为过程记录。系统会记录申请时间、审批完成时间、通道反馈、到账确认和人工备注，方便团队在复盘时真正定位问题层级。",
        ],
        "case": "某跨境工具产品过去每周都要处理多次余额告急但责任不清的问题。升级后的首个大促周，客户把美区、欧区和中东区账户分别配置动态阈值，并使用批量充值功能集中处理 26 个账户。系统自动记录每一笔补款的申请、审批、回执和到账过程，使团队在 2 小时内就定位出 3 个通道延迟问题。当周异常处理平均时长从 9.5 小时缩短到 1.8 小时，预算闲置比例下降 22%，运营和财务之间的重复沟通次数下降超过一半。",
        "metrics": [
            ("预算预警命中率", ">= 90%", "预警应真正指向风险，而不是制造噪音"),
            ("批量充值审批完成时长", "< 30 分钟", "决定活动期补款的承接效率"),
            ("异常定位时长", "< 2 小时", "反映团队是否具备同日闭环能力"),
            ("资金闲置比例", "持续下降", "证明看板正在提升资金利用效率"),
        ],
        "actions": [
            "第一阶段先统一账户分组规则，让预警、批量任务和复盘都围绕同一套市场或业务维度展开。",
            "第二阶段再把审批人与财务节点接入看板，确保系统里的状态能真实反映组织动作，而不是只由运营单边记录。",
            "第三阶段把异常备注与活动 ID 绑定，让资金问题能够被追溯到具体业务场景，形成真正可复用的改进闭环。",
        ],
    },
    {
        "category_id": "insight",
        "title": "拉美本地支付与广告合规新趋势：如何降低拒付、汇损与代理链条风险",
        "title_en": "LATAM Local Payments and Ad Compliance: Reducing Chargebacks, FX Loss, and Agency Chain Risk",
        "summary": "拉美市场正在成为出海投放的新增长极，但支付碎片化、代理链复杂和合规要求升级，也让预算效率面临新挑战。本文从支付、本地化和账户结构三个维度给出应对策略。",
        "summary_en": "LATAM is becoming a major growth region for cross-border advertisers, yet fragmented payments, layered agency chains, and tougher compliance are putting pressure on funding efficiency. This article outlines what to do next.",
        "seo_keywords": "拉美广告投放,本地支付,广告合规,拒付管理,汇损控制",
        "image": "https://picsum.photos/seed/yiyu-manual-106/800/500",
        "views": 2297,
        "intro_quote": "拉美市场不是不能做，而是不能用北美思维和单一路径去做。",
        "overview": "越来越多出海品牌把拉美视为下一个增长市场，但真正进入后才发现，问题并不只是语言翻译和物流时效，而是支付习惯、税务结构、代理链条和平台审核逻辑同时变复杂。尤其当品牌通过多个本地合作方承接充值、运营和结算时，任何一个环节信息不一致，都会放大账户风控和资金损耗。拉美市场的独特之处在于，广告增长和资金合规几乎同时发生，不能先粗放跑量再补做制度。",
        "problem": "很多企业沿用北美的支付和账户结构进入拉美，前两周数据看起来不错，随后就遇到拒付上升、补款回执延迟和汇率波动侵蚀利润的问题。还有一些团队为了快速落地，使用过长的代理链去覆盖市场，结果主体一致性、回执追踪和税务归档都变得难以审计。短期像是在降低进入门槛，长期却在抬高合规与经营成本。",
        "framework": [
            "进入拉美前，先建立市场优先级与资金路径优先级的双层地图。不是所有国家都值得同时铺开，也不是所有市场都必须复用同一套充值和结算模式。",
            "把拒付率、到账时效、异常回执定位时长和月度汇损纳入经营周报。不要再只看媒体回报而忽略真实利润。",
            "逐步缩短代理链，引入更清晰的本地主体、付款关系和对账机制。代理链越短，异常越容易定位，长期合规成本也越低。",
        ],
        "case": "某订阅工具产品最初沿用北美支付和账户结构进入巴西，虽然前两周拿到不错注册量，但很快就遇到支付争议增多、补款回执延迟和汇率波动侵蚀利润的问题。以渔协助其把巴西市场单独拆出资金池，优化本地支付承接路径，并把素材中的优惠承诺与站点付款说明同步重写。同时，团队把拒付率和汇损纳入周报，要求投手、财务和管理层共同复盘。执行 6 周后，拒付率下降 34%，汇损比例降到 1.2%，净回报提升 19%。",
        "metrics": [
            ("拒付率", "< 0.8%", "过高会直接侵蚀利润并影响支付健康度"),
            ("到账时效", "< 4 小时", "决定活动期预算是否能被及时承接"),
            ("月度汇损比例", "< 1.5%", "应作为市场利润判断的一部分"),
            ("异常回执定位时长", "< 2 小时", "代理链越复杂越要压缩这个指标"),
        ],
        "actions": [
            "先选一到两个重点国家做深，不要一开始就用同一套流程覆盖整个拉美。",
            "把拒付、汇损和回款周期写进经营周报，让营销、财务和管理层共同看见真实利润。",
            "让素材承诺、站点支付说明和账户主体保持一致，避免增长一旦起来就被合规与支付问题反噬。",
        ],
    },
]


def render_table(rows):
    lines = [
        "| 指标 | 建议值 | 说明 |",
        "| --- | --- | --- |",
    ]
    for metric, target, note in rows:
        lines.append(f"| {metric} | {target} | {note} |")
    return "\n".join(lines)


def build_cn_content(article):
    parts = [
        f"> {article['intro_quote']}",
        "## 行业背景与问题定义",
        article["overview"],
        "## 为什么很多团队会在这里失速",
        article["problem"],
        "## 可执行的方法框架",
    ]
    parts.extend([f"### 方法 {index}\n{item}" for index, item in enumerate(article["framework"], start=1)])
    parts.extend(
        [
            "## 实战案例拆解",
            article["case"],
            "## 建议关注的核心指标",
            render_table(article["metrics"]),
            "## 90 天执行清单",
        ]
    )
    parts.extend([f"### 动作 {index}\n{item}" for index, item in enumerate(article["actions"], start=1)])
    parts.extend(
        [
            "## 结论",
            "真正稳定的出海增长，从来不是某一条素材、某一个渠道或某一次大促的偶然成功，而是账户、资金、内容、站点与组织流程被设计成一条可以复用的经营链路。企业越早把这些能力前置，越能在平台规则变化时保持可控，在市场放量时保持效率。",
        ]
    )
    return "\n\n".join(parts)


def build_en_content(article):
    metric_rows = [
        "| Metric | Target | Why It Matters |",
        "| --- | --- | --- |",
    ]
    for metric, target, note in article["metrics"]:
        metric_rows.append(f"| {metric} | {target} | {note} |")

    parts = [
        f"> {article['summary_en']}",
        "## Context",
        "This topic matters because cross-border performance is no longer determined by media optimization alone. Platforms, payment paths, account governance, and operational discipline now shape delivery stability together.",
        "## What Usually Goes Wrong",
        "Many teams still treat account setup, payment operations, creative review, and campaign management as separate workflows. That creates blind spots, slows response time, and causes growth to stall right when budgets are ready to scale.",
        "## Practical Framework",
    ]
    parts.extend([f"### Step {index}\n{item}" for index, item in enumerate(article["framework"], start=1)])
    parts.extend(
        [
            "## Operating Case",
            article["case"],
            "## Recommended Metrics",
            "\n".join(metric_rows),
            "## 90-Day Actions",
        ]
    )
    parts.extend([f"### Action {index}\n{item}" for index, item in enumerate(article["actions"], start=1)])
    parts.extend(
        [
            "## Takeaway",
            "The companies that scale well across markets are rarely the ones with the most aggressive budgets. They are the ones that make funding, compliance, creative production, and media buying speak the same operational language.",
        ]
    )
    return "\n\n".join(parts)


def insert_articles():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    inserted = 0
    skipped = 0

    for article in ARTICLES:
        exists = cursor.execute("SELECT 1 FROM articles WHERE title = ?", (article["title"],)).fetchone()
        if exists:
            skipped += 1
            print(f"Skip existing article: {article['title']}")
            continue

        cursor.execute(
            """
            INSERT INTO articles (
                category_id, title, summary, content, date, views, image,
                seo_keywords, title_en, summary_en, content_en
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                article["category_id"],
                article["title"],
                article["summary"],
                build_cn_content(article),
                TODAY,
                article["views"],
                article["image"],
                article["seo_keywords"],
                article["title_en"],
                article["summary_en"],
                build_en_content(article),
            ),
        )
        inserted += 1
        print(f"Inserted article: {article['title']}")

    conn.commit()
    conn.close()
    print(f"Done. inserted={inserted}, skipped={skipped}")
    return inserted


if __name__ == "__main__":
    insert_articles()
