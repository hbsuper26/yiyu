import re

with open('templates/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Enhance the layout of the hero section text to match the GIF's centered, bold style
# Current text is left-aligned. The GIF has giant text and centered text overlay.
# Let's adjust the grid layout of the hero section to be more striking.
# We will keep all the text elements but center them and make them float over the animation.

hero_content_start = html.find('<div class="grid lg:grid-cols-2 gap-12 items-center relative z-10 pointer-events-none">')
hero_content_end = html.find('<!-- Supported Platforms -->')

if hero_content_start != -1 and hero_content_end != -1:
    old_hero_content = html[hero_content_start:hero_content_end]
    
    # We want to change the layout from grid to flex-center, and stack the text and mockup nicely
    new_hero_content = """
            <div class="flex flex-col lg:flex-row items-center justify-center gap-16 relative z-10 w-full pointer-events-none">
                <div class="text-center lg:text-left flex-1 max-w-3xl">
                    <div class="inline-flex items-center justify-center lg:justify-start gap-2 px-5 py-2.5 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-sm font-bold mb-8 backdrop-blur-sm shadow-[0_0_15px_rgba(59,130,246,0.2)]">
                        <span class="w-2.5 h-2.5 rounded-full bg-blue-500 animate-pulse shadow-[0_0_10px_rgba(59,130,246,0.8)]"></span>
                        <span x-text="t[lang].hero.badge" class="tracking-wide uppercase">企业级海外广告资金管理系统</span>
                    </div>
                    <h1 class="text-6xl md:text-7xl lg:text-8xl font-black tracking-tight text-white mb-6 leading-[1.1] drop-shadow-2xl">
                        <span x-text="t[lang].hero.title1" class="inline-block relative z-20">全球广告账户</span><br>
                        <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-indigo-400 to-purple-500 inline-block relative z-20 drop-shadow-2xl" x-text="t[lang].hero.titleHighlight">开户 · 充值 · 减款</span>
                    </h1>
                    <p class="mt-8 text-xl md:text-2xl text-slate-300/90 mb-12 leading-relaxed max-w-2xl mx-auto lg:mx-0 font-medium backdrop-blur-sm drop-shadow-lg" x-text="t[lang].hero.subtitle">
                        专为出海企业打造的资金流转中枢。支持 Google, Meta, TikTok 等主流媒体，实现账户秒级开通、余额实时划转、预算灵活调配。
                    </p>
                    <div class="flex flex-col sm:flex-row justify-center lg:justify-start gap-6 pointer-events-auto relative z-30">
                        <a href="https://t.me/yiyiyiads" target="_blank" class="px-10 py-5 rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-bold text-lg hover:from-blue-500 hover:to-indigo-500 transition-all shadow-[0_0_30px_rgba(79,70,229,0.4)] hover:shadow-[0_0_40px_rgba(79,70,229,0.6)] hover:-translate-y-1 flex items-center justify-center gap-3 border border-white/10">
                            <span x-text="t[lang].hero.cta_primary" class="tracking-wide">现在试用</span>
                            <i class="fas fa-arrow-right text-sm"></i>
                        </a>
                        <a href="https://t.me/yiyiyiads" target="_blank" class="px-10 py-5 rounded-xl glass-panel text-white font-bold text-lg hover:bg-white/10 transition-all hover:-translate-y-1 flex items-center justify-center border border-white/20 shadow-[0_0_20px_rgba(0,0,0,0.2)]">
                            <span x-text="t[lang].hero.cta_secondary" class="tracking-wide">联系我们</span>
                        </a>
                    </div>
                </div>
                
                <!-- 3D Dashboard Mockup -->
                <div class="relative hidden lg:block floating pointer-events-auto flex-1 max-w-2xl transform hover:scale-105 transition-transform duration-700">
                    <div class="absolute -inset-1 bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-600 rounded-3xl blur-2xl opacity-40 animate-pulse"></div>
                    <div class="relative glass-panel rounded-3xl p-6 shadow-[0_0_50px_rgba(0,0,0,0.5)] border border-white/10 backdrop-blur-xl bg-slate-900/40">
                        <div class="flex items-center gap-2 mb-6 border-b border-white/10 pb-4">
                            <div class="w-3.5 h-3.5 rounded-full bg-red-500 shadow-[0_0_10px_rgba(239,68,68,0.5)]"></div>
                            <div class="w-3.5 h-3.5 rounded-full bg-yellow-500 shadow-[0_0_10px_rgba(234,179,8,0.5)]"></div>
                            <div class="w-3.5 h-3.5 rounded-full bg-green-500 shadow-[0_0_10px_rgba(34,197,94,0.5)]"></div>
                            <div class="text-xs text-slate-400/80 ml-4 font-mono tracking-wider">yiyu-dashboard.com</div>
                        </div>
                        <div class="grid grid-cols-2 gap-6 mb-6">
                            <div class="bg-white/5 p-5 rounded-2xl border border-white/5 shadow-inner">
                                <div class="text-slate-400 text-xs mb-2 uppercase tracking-wider font-bold">Total Balance</div>
                                <div class="text-3xl font-black text-white drop-shadow-md">$12,450.00</div>
                                <div class="text-emerald-400 text-xs mt-3 font-bold flex items-center gap-1"><i class="fas fa-arrow-up"></i> 15% this week</div>
                            </div>
                            <div class="bg-white/5 p-5 rounded-2xl border border-white/5 shadow-inner">
                                <div class="text-slate-400 text-xs mb-2 uppercase tracking-wider font-bold">Active Accounts</div>
                                <div class="text-3xl font-black text-white drop-shadow-md">24</div>
                                <div class="flex gap-3 mt-3">
                                    <i class="fab fa-google text-blue-400 text-lg drop-shadow-md"></i>
                                    <i class="fab fa-facebook text-blue-600 text-lg drop-shadow-md"></i>
                                    <i class="fab fa-tiktok text-black bg-white rounded-full p-0.5 text-xs drop-shadow-md"></i>
                                </div>
                            </div>
                        </div>
                        <div class="bg-white/5 h-40 rounded-2xl border border-white/5 p-4 relative overflow-hidden shadow-inner">
                             <!-- Fake Chart -->
                             <div class="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-blue-500/30 to-transparent"></div>
                             <svg class="absolute bottom-0 w-full h-full" preserveAspectRatio="none" viewBox="0 0 100 100">
                                <path d="M0,100 L0,50 Q25,30 50,60 T100,20 L100,100 Z" fill="url(#grad)" />
                                <path d="M0,50 Q25,30 50,60 T100,20" fill="none" stroke="#60a5fa" stroke-width="3" stroke-linecap="round" filter="drop-shadow(0px 0px 5px rgba(96,165,250,0.8))"/>
                                <defs>
                                    <linearGradient id="grad" x1="0%" y1="0%" x2="0%" y2="100%">
                                        <stop offset="0%" style="stop-color:rgba(59,130,246,0.4);stop-opacity:1" />
                                        <stop offset="100%" style="stop-color:rgba(59,130,246,0);stop-opacity:1" />
                                    </linearGradient>
                                </defs>
                             </svg>
                        </div>
                    </div>
                    
                    <!-- Floating Elements -->
                    <div class="absolute -right-12 -top-12 glass-panel p-4 rounded-2xl shadow-[0_0_30px_rgba(34,197,94,0.3)] border border-green-500/30 animate-bounce backdrop-blur-xl bg-slate-900/60 z-20">
                        <div class="flex items-center gap-4 text-white">
                            <div class="w-10 h-10 bg-green-500/20 rounded-full flex items-center justify-center text-green-400 text-lg shadow-[0_0_15px_rgba(34,197,94,0.4)]"><i class="fas fa-check"></i></div>
                            <div>
                                <div class="text-sm font-black tracking-wide">充值成功</div>
                                <div class="text-xs text-green-400 font-mono mt-0.5">+$5,000 USD</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
"""
    html = html.replace(old_hero_content, new_hero_content)

with open('templates/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Hero layout updated.")
