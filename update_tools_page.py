import re

with open('templates/tools.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the "Tools Grid Placeholder" section with actual card
tools_grid = """
    <!-- Tools Grid -->
    <section class="py-20 bg-slate-50 relative">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Copywriting Tool Card -->
                <a href="/tools/copywriting" class="group block relative bg-white rounded-2xl shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300 border border-slate-100 overflow-hidden">
                    <div class="absolute inset-0 bg-gradient-to-br from-blue-600/5 to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                    <div class="h-48 overflow-hidden relative">
                        <img src="https://images.unsplash.com/photo-1493612276216-ee3925520721?q=80&w=800&auto=format&fit=crop" alt="文案列表器" class="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-500">
                        <div class="absolute top-4 right-4 bg-white/90 backdrop-blur-sm px-3 py-1 rounded-full text-xs font-bold text-blue-600 shadow-sm flex items-center gap-1">
                            <i class="fas fa-bolt"></i> <span x-text="t[lang].toolLabels.hot">热门</span>
                        </div>
                    </div>
                    <div class="p-6 relative">
                        <div class="w-12 h-12 bg-blue-50 text-blue-600 rounded-xl flex items-center justify-center text-xl mb-4 -mt-12 relative z-10 shadow-sm border border-white">
                            <i class="fas fa-keyboard"></i>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-2 group-hover:text-blue-600 transition-colors" x-text="t[lang].tools.copywriting.title">文案裂变神器</h3>
                        <p class="text-sm text-slate-500 leading-relaxed mb-4" x-text="t[lang].tools.copywriting.desc">输入核心词汇，一键生成多平台（小红书、知乎、抖音等）爆款文案，支持变量裂变和情绪风格选择。</p>
                        <div class="flex items-center text-blue-600 text-sm font-semibold">
                            <span x-text="t[lang].useNow">立即使用</span>
                            <i class="fas fa-arrow-right ml-2 group-hover:translate-x-1 transition-transform"></i>
                        </div>
                    </div>
                </a>
                
                <!-- Placeholder for future tools -->
                <div class="group relative bg-slate-100/50 rounded-2xl border-2 border-dashed border-slate-200 flex flex-col items-center justify-center p-8 text-center h-[350px]">
                    <div class="w-16 h-16 bg-slate-200 rounded-full flex items-center justify-center mb-4">
                        <i class="fas fa-plus text-2xl text-slate-400"></i>
                    </div>
                    <h3 class="text-lg font-semibold text-slate-600 mb-2" x-text="t[lang].moreTools.title">更多工具正在路上</h3>
                    <p class="text-sm text-slate-400 max-w-[200px]" x-text="t[lang].moreTools.desc">敬请期待更多提效神器</p>
                </div>
            </div>
        </div>
    </section>
"""

# Replace the empty placeholder with our new grid
start_placeholder = html.find('<!-- Tools Grid Placeholder -->')
end_placeholder = html.find('</section>', start_placeholder) + 10

html = html[:start_placeholder] + tools_grid + html[end_placeholder:]

# Add translations
zh_insert = html.find('empty: {')
html = html[:zh_insert] + """toolLabels: { hot: "热门" },
                tools: {
                    copywriting: {
                        title: "文案裂变神器",
                        desc: "输入核心词汇，一键生成多平台（小红书、知乎、抖音等）爆款文案，支持变量裂变和情绪风格选择。"
                    }
                },
                useNow: "立即使用",
                moreTools: { title: "更多工具正在路上", desc: "敬请期待更多提效神器" },
                """ + html[zh_insert:]

en_insert = html.find('empty: {', html.find('en: {'))
html = html[:en_insert] + """toolLabels: { hot: "Hot" },
                tools: {
                    copywriting: {
                        title: "Copy Fission Tool",
                        desc: "Input keywords to instantly generate viral copy for multiple platforms (XHS, TikTok, etc.) with variables and emotional styles."
                    }
                },
                useNow: "Use Now",
                moreTools: { title: "More Tools Coming Soon", desc: "Stay tuned for more efficiency tools" },
                """ + html[en_insert:]


with open('templates/tools.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Tools template updated with module card.")
