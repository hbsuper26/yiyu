import re
import os

with open('d:/AI生成原型/yiyu_digital_media/templates/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_sections = """
    <!-- Pain Points vs Solutions -->
    <section id="painpoints" class="py-24 bg-slate-900 relative overflow-hidden">
        <div class="absolute top-0 left-0 w-full h-full bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-5"></div>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div class="text-center mb-16 reveal">
                <h2 class="text-4xl font-bold text-white mb-4"><span x-text="t[lang].painpoints.title">打破传统，</span><span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500" x-text="t[lang].painpoints.highlight">直击出海广告管理痛点</span></h2>
                <p class="text-slate-400" x-text="t[lang].painpoints.subtitle">为什么选择以渔数媒？因为我们懂您的业务瓶颈</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <!-- Pain Points -->
                <div class="bg-white/5 backdrop-blur-xl p-8 rounded-3xl border border-red-500/20 border-l-4 border-l-red-500 hover:-translate-y-2 transition-transform duration-300 reveal-left">
                    <div class="flex items-center mb-8">
                        <div class="w-12 h-12 rounded-xl bg-red-500/20 flex items-center justify-center text-red-400 text-xl mr-4 shadow-lg shadow-red-500/20">
                            <i class="fas fa-times-circle"></i>
                        </div>
                        <h3 class="text-2xl font-bold text-white" x-text="t[lang].painpoints.bad_title">传统模式的痛点</h3>
                    </div>
                    <ul class="space-y-6 text-slate-300">
                        <li class="flex items-start"><i class="fas fa-exclamation-triangle mt-1.5 mr-4 text-red-400"></i> <div><strong class="text-white block mb-1" x-text="t[lang].painpoints.b1_t">开户流程繁琐</strong> <span class="text-sm" x-text="t[lang].painpoints.b1_d">多渠道来回切换，人工沟通成本高，进度不透明。</span></div></li>
                        <li class="flex items-start"><i class="fas fa-exclamation-triangle mt-1.5 mr-4 text-red-400"></i> <div><strong class="text-white block mb-1" x-text="t[lang].painpoints.b2_t">资金流转极慢</strong> <span class="text-sm" x-text="t[lang].painpoints.b2_d">充值减款依靠人工对账，容易出错且影响广告投放时效。</span></div></li>
                        <li class="flex items-start"><i class="fas fa-exclamation-triangle mt-1.5 mr-4 text-red-400"></i> <div><strong class="text-white block mb-1" x-text="t[lang].painpoints.b3_t">资产管理混乱</strong> <span class="text-sm" x-text="t[lang].painpoints.b3_d">BM授权、解绑操作杂乱，坏账/封户资金退回困难。</span></div></li>
                        <li class="flex items-start"><i class="fas fa-exclamation-triangle mt-1.5 mr-4 text-red-400"></i> <div><strong class="text-white block mb-1" x-text="t[lang].painpoints.b4_t">无据可查</strong> <span class="text-sm" x-text="t[lang].painpoints.b4_d">需求响应慢，缺乏操作日志，财务复盘极为困难。</span></div></li>
                    </ul>
                </div>

                <!-- Solutions -->
                <div class="bg-gradient-to-br from-blue-900/40 to-purple-900/40 backdrop-blur-xl p-8 rounded-3xl border border-blue-500/30 border-l-4 border-l-blue-500 hover:-translate-y-2 transition-transform duration-300 reveal-right shadow-2xl shadow-blue-900/20">
                    <div class="flex items-center mb-8">
                        <div class="w-12 h-12 rounded-xl bg-blue-500/20 flex items-center justify-center text-blue-400 text-xl mr-4 shadow-lg shadow-blue-500/20">
                            <i class="fas fa-check-circle"></i>
                        </div>
                        <h3 class="text-2xl font-bold text-white" x-text="t[lang].painpoints.good_title">我们的解决方案</h3>
                    </div>
                    <ul class="space-y-6 text-slate-300">
                        <li class="flex items-start"><i class="fas fa-check-circle mt-1.5 mr-4 text-blue-400"></i> <div><strong class="text-white block mb-1" x-text="t[lang].painpoints.g1_t">一站式自动化开户</strong> <span class="text-sm" x-text="t[lang].painpoints.g1_d">聚合全媒体平台，一键批量提交开户申请，全流程工单化追踪。</span></div></li>
                        <li class="flex items-start"><i class="fas fa-check-circle mt-1.5 mr-4 text-blue-400"></i> <div><strong class="text-white block mb-1" x-text="t[lang].painpoints.g2_t">秒级资金调度系统</strong> <span class="text-sm" x-text="t[lang].painpoints.g2_d">充值/减款/清零一键直达，严格的钱包额度校验，保障资金安全。</span></div></li>
                        <li class="flex items-start"><i class="fas fa-check-circle mt-1.5 mr-4 text-blue-400"></i> <div><strong class="text-white block mb-1" x-text="t[lang].painpoints.g3_t">安全的账户管家</strong> <span class="text-sm" x-text="t[lang].painpoints.g3_d">一对一授权机制，灵活的BM管理与解绑，封禁账户一键兜底清零。</span></div></li>
                        <li class="flex items-start"><i class="fas fa-check-circle mt-1.5 mr-4 text-emerald-400"></i> <div><strong class="text-emerald-400 block mb-1" x-text="t[lang].painpoints.g4_t">人效指数级提升</strong> <span class="text-sm text-emerald-500/80" x-text="t[lang].painpoints.g4_d">赋能团队高效作业，化繁为简批量处理，全面加速业务运转。</span></div></li>
                    </ul>
                </div>
            </div>
        </div>
    </section>

    <!-- Core Features Section -->
    <section id="features" class="py-24 bg-slate-50 relative overflow-hidden">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div class="text-center mb-16 reveal">
                <div class="inline-block px-4 py-1.5 rounded-full bg-blue-100 text-sm font-bold text-blue-600 mb-4 tracking-wider uppercase" x-text="t[lang].features.badge">Core Features</div>
                <h2 class="text-4xl font-bold text-slate-900 mb-4" x-text="t[lang].features.title">四大核心模块，驱动业务高速运转</h2>
                <p class="text-slate-500 text-lg" x-text="t[lang].features.subtitle">将复杂的操作转化为简单的鼠标点击</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <!-- Feature 1 -->
                <div class="bg-white p-8 rounded-3xl border border-slate-100 shadow-xl shadow-slate-200/50 hover:-translate-y-2 transition-all duration-300 group reveal" style="transition-delay: 0ms;">
                    <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-cyan-400 rounded-2xl flex items-center justify-center text-white text-2xl mb-6 shadow-lg shadow-blue-500/30 group-hover:scale-110 transition-transform">
                        <i class="fas fa-bolt"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-slate-900 mb-4" x-text="t[lang].features.f1_title">极速开户流转</h3>
                    <p class="text-slate-500 text-sm mb-6 leading-relaxed" x-text="t[lang].features.f1_desc">支持10+海外主流媒体。从申请提交 ➔ 运营认领 ➔ 审核下发，状态实时同步。支持单次批量添加账户。</p>
                    <div class="mt-auto w-full pt-4 border-t border-slate-100 flex gap-2">
                        <span class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-md" x-text="t[lang].features.tag_all_channel">全渠道覆盖</span>
                        <span class="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-md" x-text="t[lang].features.tag_batch">批量下发</span>
                    </div>
                </div>

                <!-- Feature 2 -->
                <div class="bg-white p-8 rounded-3xl border border-slate-100 shadow-xl shadow-slate-200/50 hover:-translate-y-2 transition-all duration-300 group reveal" style="transition-delay: 150ms;">
                    <div class="w-16 h-16 bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl flex items-center justify-center text-white text-2xl mb-6 shadow-lg shadow-purple-500/30 group-hover:scale-110 transition-transform">
                        <i class="fas fa-wallet"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-slate-900 mb-4" x-text="t[lang].features.f2_title">智能资金调度</h3>
                    <p class="text-slate-500 text-sm mb-6 leading-relaxed" x-text="t[lang].features.f2_desc">告别错账漏账！支持账户批量充值与减款，子钱包余额精准校验。更支持封禁账户的“一键清零”兜底退款。</p>
                    <div class="mt-auto w-full pt-4 border-t border-slate-100 flex gap-2">
                        <span class="text-xs font-bold text-purple-600 bg-purple-50 px-3 py-1 rounded-md" x-text="t[lang].features.tag_fast_fund">秒级到账</span>
                        <span class="text-xs font-bold text-purple-600 bg-purple-50 px-3 py-1 rounded-md" x-text="t[lang].features.tag_safe">一键清零兜底</span>
                    </div>
                </div>

                <!-- Feature 3 -->
                <div class="bg-white p-8 rounded-3xl border border-slate-100 shadow-xl shadow-slate-200/50 hover:-translate-y-2 transition-all duration-300 group reveal" style="transition-delay: 300ms;">
                    <div class="w-16 h-16 bg-gradient-to-br from-orange-500 to-yellow-400 rounded-2xl flex items-center justify-center text-white text-2xl mb-6 shadow-lg shadow-orange-500/30 group-hover:scale-110 transition-transform">
                        <i class="fas fa-shield-alt"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-slate-900 mb-4" x-text="t[lang].features.f3_title">资产授权与闭环</h3>
                    <p class="text-slate-500 text-sm mb-6 leading-relaxed" x-text="t[lang].features.f3_desc">严格的1对1账户授权机制，支持解绑与重新分配。所有工单（充减款、解绑等）均有专人认领审核，永久可查。</p>
                    <div class="mt-auto w-full pt-4 border-t border-slate-100 flex gap-2">
                        <span class="text-xs font-bold text-orange-600 bg-orange-50 px-3 py-1 rounded-md" x-text="t[lang].features.tag_bm">BM管理</span>
                        <span class="text-xs font-bold text-orange-600 bg-orange-50 px-3 py-1 rounded-md" x-text="t[lang].features.tag_ticket">工单审核</span>
                    </div>
                </div>

                <!-- Feature 4 -->
                <div class="bg-gradient-to-b from-slate-900 to-slate-800 p-8 rounded-3xl border border-slate-700 shadow-2xl hover:-translate-y-2 transition-all duration-300 group reveal" style="transition-delay: 450ms;">
                    <div class="w-16 h-16 bg-gradient-to-br from-emerald-400 to-teal-500 rounded-2xl flex items-center justify-center text-white text-2xl mb-6 shadow-lg shadow-emerald-500/30 group-hover:scale-110 transition-transform">
                        <i class="fas fa-tachometer-alt"></i>
                    </div>
                    <h3 class="text-2xl font-bold text-white mb-4" x-text="t[lang].features.f4_title">人员增速提效</h3>
                    <p class="text-slate-400 text-sm mb-6 leading-relaxed" x-text="t[lang].features.f4_desc">通过工单认领制与批量自动化流转，深度赋能运营与财务团队，化解机械重复劳动，大幅提升团队整体人效。</p>
                    <div class="mt-auto w-full pt-4 border-t border-slate-700 flex gap-2">
                        <span class="text-xs font-bold text-emerald-400 bg-emerald-400/10 px-3 py-1 rounded-md" x-text="t[lang].features.tag_hr">释放人力</span>
                        <span class="text-xs font-bold text-emerald-400 bg-emerald-400/10 px-3 py-1 rounded-md" x-text="t[lang].features.tag_auto">批量自动化</span>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Ticket Workflow Section -->
    <section class="py-24 bg-white relative overflow-hidden">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center max-w-3xl mx-auto mb-16 reveal">
                <div class="inline-block px-4 py-1.5 rounded-full bg-purple-100 text-sm font-bold text-purple-600 mb-4 tracking-wider uppercase" x-text="t[lang].workflow.badge">Service Loop</div>
                <h2 class="text-4xl font-bold text-slate-900 mb-6" x-text="t[lang].workflow.title">客户工单闭环，打造极致服务体验</h2>
                <p class="text-lg text-slate-500" x-text="t[lang].workflow.subtitle">充值、减款、解绑、清零等诉求统一收口，响应效率肉眼可见。</p>
            </div>
            
            <div class="bg-slate-50 rounded-3xl p-8 md:p-12 relative overflow-hidden border border-slate-100 reveal">
                <!-- Background decorative text -->
                <div class="absolute -right-10 -top-10 text-9xl text-slate-200/50 font-bold italic select-none">WORKFLOW</div>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center relative z-10">
                    <div class="p-6 bg-white rounded-2xl shadow-sm border border-slate-100 hover:-translate-y-2 transition-all duration-300">
                        <div class="w-20 h-20 mx-auto bg-emerald-50 rounded-full flex items-center justify-center text-3xl text-emerald-500 border-4 border-emerald-100 mb-6">
                            <i class="fas fa-paper-plane"></i>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3" x-text="t[lang].workflow.s1_title">1. 需求统一汇聚</h3>
                        <p class="text-slate-500 text-sm" x-text="t[lang].workflow.s1_desc">客户在前端发起的任何资金变动、BM授权/解绑申请，瞬间直达后台任务池，等待响应。</p>
                    </div>

                    <div class="p-6 bg-white rounded-2xl shadow-sm border border-slate-100 hover:-translate-y-2 transition-all duration-300 relative">
                        <div class="hidden md:block absolute top-1/3 -left-8 w-16 h-0.5 bg-gradient-to-r from-transparent via-blue-300 to-transparent"></div>
                        <div class="hidden md:block absolute top-1/3 -right-8 w-16 h-0.5 bg-gradient-to-r from-transparent via-blue-300 to-transparent"></div>
                        <div class="w-20 h-20 mx-auto bg-blue-50 rounded-full flex items-center justify-center text-3xl text-blue-500 border-4 border-blue-100 mb-6">
                            <i class="fas fa-hand-pointer"></i>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3" x-text="t[lang].workflow.s2_title">2. 批量极速认领</h3>
                        <p class="text-slate-500 text-sm" x-text="t[lang].workflow.s2_desc">客服通过多维条件筛选待办任务，支持批量认领。明确操作人，杜绝推诿扯皮。</p>
                    </div>

                    <div class="p-6 bg-white rounded-2xl shadow-sm border border-slate-100 hover:-translate-y-2 transition-all duration-300">
                        <div class="w-20 h-20 mx-auto bg-purple-50 rounded-full flex items-center justify-center text-3xl text-purple-500 border-4 border-purple-100 mb-6">
                            <i class="fas fa-clipboard-check"></i>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-3" x-text="t[lang].workflow.s3_title">3. 严谨审核批复</h3>
                        <p class="text-slate-500 text-sm" x-text="t[lang].workflow.s3_desc">财务核对金额与要求后批复。审核金额、时间、操作人、备注信息永久记录入库，不可篡改。</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
"""

pattern = r"<!-- Client/Tenant Management Section -->.*?<!-- Success Stories / Case Studies Section -->"
content = re.sub(pattern, new_sections + "\\n    <!-- Success Stories / Case Studies Section -->", content, flags=re.DOTALL)

translation_zh_update = """
                painpoints: {
                    title: "打破传统，",
                    highlight: "直击出海广告管理痛点",
                    subtitle: "为什么选择以渔数媒？因为我们懂您的业务瓶颈",
                    bad_title: "传统模式的痛点",
                    b1_t: "开户流程繁琐", b1_d: "多渠道来回切换，人工沟通成本高，进度不透明。",
                    b2_t: "资金流转极慢", b2_d: "充值减款依靠人工对账，容易出错且影响广告投放时效。",
                    b3_t: "资产管理混乱", b3_d: "BM授权、解绑操作杂乱，坏账/封户资金退回困难。",
                    b4_t: "无据可查", b4_d: "需求响应慢，缺乏操作日志，财务复盘极为困难。",
                    good_title: "我们的解决方案",
                    g1_t: "一站式自动化开户", g1_d: "聚合全媒体平台，一键批量提交开户申请，全流程工单化追踪。",
                    g2_t: "秒级资金调度系统", g2_d: "充值/减款/清零一键直达，严格的钱包额度校验，保障资金安全。",
                    g3_t: "安全的账户管家", g3_d: "一对一授权机制，灵活的BM管理与解绑，封禁账户一键兜底清零。",
                    g4_t: "人效指数级提升", g4_d: "赋能团队高效作业，化繁为简批量处理，全面加速业务运转。"
                },
                features: {
                    badge: "核心能力",
                    title: "四大核心模块，驱动业务高速运转",
                    subtitle: "将复杂的操作转化为简单的鼠标点击",
                    f1_title: "极速开户流转", f1_desc: "支持10+海外主流媒体。从申请提交 ➔ 运营认领 ➔ 审核下发，状态实时同步。支持单次批量添加账户。",
                    f2_title: "智能资金调度", f2_desc: "告别错账漏账！支持账户批量充值与减款，子钱包余额精准校验。更支持封禁账户的“一键清零”兜底退款。",
                    f3_title: "资产授权与闭环", f3_desc: "严格的1对1账户授权机制，支持解绑与重新分配。所有工单（充减款、解绑等）均有专人认领审核，永久可查。",
                    f4_title: "人员增速提效", f4_desc: "通过工单认领制与批量自动化流转，深度赋能运营与财务团队，化解机械重复劳动，大幅提升团队整体人效。",
                    tag_all_channel: "全渠道覆盖", tag_batch: "批量下发",
                    tag_fast_fund: "秒级到账", tag_safe: "一键清零兜底",
                    tag_bm: "BM管理", tag_ticket: "工单审核",
                    tag_hr: "释放人力", tag_auto: "批量自动化"
                },
                workflow: {
                    badge: "服务闭环",
                    title: "客户工单闭环，打造极致服务体验",
                    subtitle: "充值、减款、解绑、清零等诉求统一收口，响应效率肉眼可见。",
                    s1_title: "1. 需求统一汇聚", s1_desc: "客户在前端发起的任何资金变动、BM授权/解绑申请，瞬间直达后台任务池，等待响应。",
                    s2_title: "2. 批量极速认领", s2_desc: "客服通过多维条件筛选待办任务，支持批量认领。明确操作人，杜绝推诿扯皮。",
                    s3_title: "3. 严谨审核批复", s3_desc: "财务核对金额与要求后批复。审核金额、时间、操作人、备注信息永久记录入库，不可篡改。"
                },
"""

translation_en_update = """
                painpoints: {
                    title: "Break Traditions, ",
                    highlight: "Solve Ad Pain Points",
                    subtitle: "Why choose Yiyu Digital? Because we understand your bottlenecks.",
                    bad_title: "Traditional Pain Points",
                    b1_t: "Complex Opening", b1_d: "Switching between channels, high communication costs, opaque progress.",
                    b2_t: "Slow Fund Transfer", b2_d: "Manual reconciliation causes errors and affects ad delivery timelines.",
                    b3_t: "Chaotic Management", b3_d: "Messy BM binding/unbinding, difficult to recover funds from banned accounts.",
                    b4_t: "Untraceable Operations", b4_d: "Slow response, no operation logs, making financial audits extremely difficult.",
                    good_title: "Our Solutions",
                    g1_t: "One-Stop Auto Opening", g1_d: "Aggregate all platforms, batch submit applications, full-process ticket tracking.",
                    g2_t: "Second-Level Dispatch", g2_d: "One-click recharge/deduct/clear with strict wallet balance verification.",
                    g3_t: "Secure Account Manager", g3_d: "1-on-1 binding mechanism, flexible BM management, one-click fund recovery.",
                    g4_t: "Exponential Efficiency", g4_d: "Empower teams with batch processing, accelerating business operations comprehensively."
                },
                features: {
                    badge: "Core Capabilities",
                    title: "Four Core Modules to Drive High-Speed Operations",
                    subtitle: "Turn complex operations into simple mouse clicks.",
                    f1_title: "Fast Account Opening", f1_desc: "Support 10+ media platforms. Real-time sync from submission to approval. Support batch account addition.",
                    f2_title: "Smart Fund Dispatch", f2_desc: "Say goodbye to errors! Batch recharge/deduction with precise balance checks. One-click clearing for banned accounts.",
                    f3_title: "Asset Auth & Loop", f3_desc: "Strict 1-on-1 authorization mechanism. All tickets (recharge, unbind) are claimed, reviewed, and permanently traceable.",
                    f4_title: "Team Efficiency Boost", f4_desc: "Through ticket claiming and automated flows, we empower ops and finance teams, eliminating repetitive tasks.",
                    tag_all_channel: "All Channels", tag_batch: "Batch Delivery",
                    tag_fast_fund: "Instant Arrival", tag_safe: "One-click Clear",
                    tag_bm: "BM Management", tag_ticket: "Ticket Audit",
                    tag_hr: "Free Up HR", tag_auto: "Batch Automation"
                },
                workflow: {
                    badge: "Service Loop",
                    title: "Customer Ticket Loop for Ultimate Experience",
                    subtitle: "Unified intake for recharge, deduct, unbind, and clear requests. Visible response efficiency.",
                    s1_title: "1. Unified Intake", s1_desc: "Any fund or BM request initiated by the client instantly reaches the backend task pool.",
                    s2_title: "2. Fast Claiming", s2_desc: "Agents filter and batch claim tasks. Clear accountability eliminates buck-passing.",
                    s3_title: "3. Strict Audit", s3_desc: "Finance verifies and approves. Amounts, times, operators, and notes are permanently recorded."
                },
"""

content = content.replace("hero: {", translation_zh_update + "hero: {", 1)

en_index = content.find("hero: {", content.find("en: {"))
content = content[:en_index] + translation_en_update + content[en_index:]

with open('d:/AI生成原型/yiyu_digital_media/templates/index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated successfully!")
