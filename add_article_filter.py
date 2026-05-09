import re

with open('templates/articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add currentFilter to appData
if 'currentFilter: \'all\'' not in html:
    html = html.replace('lang: localStorage.getItem(\'yiyu_lang\') || \'zh\',', 'lang: localStorage.getItem(\'yiyu_lang\') || \'zh\',\n                currentFilter: \'all\',')

# 2. Add the filter bar
filter_bar = """
            <!-- Filter Bar -->
            <div class="flex flex-wrap justify-center gap-3 mb-12">
                <button @click="currentFilter = 'all'" :class="{'bg-blue-600 text-white shadow-md shadow-blue-500/20': currentFilter === 'all', 'bg-white text-slate-600 border border-slate-200 hover:border-blue-300 hover:bg-blue-50': currentFilter !== 'all'}" class="px-6 py-2.5 rounded-full text-sm font-semibold transition-all duration-300">
                    <span x-show="lang === 'zh'">全部文章</span>
                    <span x-show="lang === 'en'" x-cloak>All Articles</span>
                </button>
                <button @click="currentFilter = 'news'" :class="{'bg-blue-600 text-white shadow-md shadow-blue-500/20': currentFilter === 'news', 'bg-white text-slate-600 border border-slate-200 hover:border-blue-300 hover:bg-blue-50': currentFilter !== 'news'}" class="px-6 py-2.5 rounded-full text-sm font-semibold transition-all duration-300">
                    <span x-show="lang === 'zh'">官方公告</span>
                    <span x-show="lang === 'en'" x-cloak>Official News</span>
                </button>
                <button @click="currentFilter = 'insight'" :class="{'bg-blue-600 text-white shadow-md shadow-blue-500/20': currentFilter === 'insight', 'bg-white text-slate-600 border border-slate-200 hover:border-blue-300 hover:bg-blue-50': currentFilter !== 'insight'}" class="px-6 py-2.5 rounded-full text-sm font-semibold transition-all duration-300">
                    <span x-show="lang === 'zh'">行业洞察</span>
                    <span x-show="lang === 'en'" x-cloak>Insights</span>
                </button>
                <button @click="currentFilter = 'guide'" :class="{'bg-blue-600 text-white shadow-md shadow-blue-500/20': currentFilter === 'guide', 'bg-white text-slate-600 border border-slate-200 hover:border-blue-300 hover:bg-blue-50': currentFilter !== 'guide'}" class="px-6 py-2.5 rounded-full text-sm font-semibold transition-all duration-300">
                    <span x-show="lang === 'zh'">投放指南</span>
                    <span x-show="lang === 'en'" x-cloak>Ad Guide</span>
                </button>
                <button @click="currentFilter = 'update'" :class="{'bg-blue-600 text-white shadow-md shadow-blue-500/20': currentFilter === 'update', 'bg-white text-slate-600 border border-slate-200 hover:border-blue-300 hover:bg-blue-50': currentFilter !== 'update'}" class="px-6 py-2.5 rounded-full text-sm font-semibold transition-all duration-300">
                    <span x-show="lang === 'zh'">产品更新</span>
                    <span x-show="lang === 'en'" x-cloak>Updates</span>
                </button>
            </div>
"""

# Insert filter bar right before the grid
grid_start = html.find('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">')
if grid_start != -1 and 'currentFilter = \'all\'' not in html:
    html = html[:grid_start] + filter_bar + '            ' + html[grid_start:]

# 3. Add x-show and animation to the article card
# Need to use Alpine.js transition for smooth filtering
card_tag = '<article class="article-card card-hover flex flex-col h-full group cursor-pointer"'
card_new = '<article x-show="currentFilter === \'all\' || currentFilter === \'{{ article.category_id }}\'" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 transform scale-95" x-transition:enter-end="opacity-100 transform scale-100" class="article-card card-hover flex flex-col h-full group cursor-pointer"'
html = html.replace(card_tag, card_new)

with open('templates/articles.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Added AlpineJS filter UI to articles.html.")
