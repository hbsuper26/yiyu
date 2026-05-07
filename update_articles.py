import re

with open('templates/articles.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update translations in the JS object to include category names
zh_translations = """
                empty: { title: "暂无文章", desc: "目前暂未发布任何内容" },
                categories: {
                    all: "全部文章",
                    news: "官方公告",
                    insight: "行业洞察",
                    guide: "投放指南",
                    update: "产品更新"
                },
                card: { readMore: "阅读全文", team: "以渔官方团队" }"""

en_translations = """
                empty: { title: "No Articles Yet", desc: "No content has been published here currently." },
                categories: {
                    all: "All",
                    news: "Official News",
                    insight: "Insights",
                    guide: "Ad Guide",
                    update: "Updates"
                },
                card: { readMore: "Read More", team: "Yiyu Official Team" }"""

# We need to replace the old `empty:` and `card:` lines with the new ones including `categories:`
# Find the zh block
zh_start = html.find('empty: { title: "暂无文章"')
if zh_start != -1:
    zh_end = html.find('card: { readMore: "阅读全文"', zh_start) + len('card: { readMore: "阅读全文", team: "以渔官方团队" }')
    html = html[:zh_start] + zh_translations.strip() + html[zh_end:]

# Find the en block
en_start = html.find('empty: { title: "No Articles Yet"')
if en_start != -1:
    en_end = html.find('card: { readMore: "Read More"', en_start) + len('card: { readMore: "Read More", team: "Yiyu Official Team" }')
    html = html[:en_start] + en_translations.strip() + html[en_end:]

# 2. Add activeCategory state to appData()
appdata_start = html.find('lang: localStorage.getItem(\'yiyu_lang\') || \'zh\',')
if appdata_start != -1:
    html = html[:appdata_start] + "activeCategory: 'all',\n                " + html[appdata_start:]

# 3. Inject the Tabs UI right after `<section class="py-16"> <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">`
tabs_ui = """
            <!-- Category Filter -->
            <div class="flex flex-wrap justify-center gap-3 mb-12" x-cloak>
                <button @click="activeCategory = 'all'" 
                        :class="activeCategory === 'all' ? 'bg-blue-600 text-white shadow-md shadow-blue-500/30' : 'bg-white text-slate-600 hover:bg-slate-50 border border-slate-200'"
                        class="px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300">
                    <span x-text="t[lang].categories.all">全部文章</span>
                </button>
                <button @click="activeCategory = 'insight'" 
                        :class="activeCategory === 'insight' ? 'bg-blue-600 text-white shadow-md shadow-blue-500/30' : 'bg-white text-slate-600 hover:bg-slate-50 border border-slate-200'"
                        class="px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300">
                    <span x-text="t[lang].categories.insight">行业洞察</span>
                </button>
                <button @click="activeCategory = 'guide'" 
                        :class="activeCategory === 'guide' ? 'bg-blue-600 text-white shadow-md shadow-blue-500/30' : 'bg-white text-slate-600 hover:bg-slate-50 border border-slate-200'"
                        class="px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300">
                    <span x-text="t[lang].categories.guide">投放指南</span>
                </button>
                <button @click="activeCategory = 'update'" 
                        :class="activeCategory === 'update' ? 'bg-blue-600 text-white shadow-md shadow-blue-500/30' : 'bg-white text-slate-600 hover:bg-slate-50 border border-slate-200'"
                        class="px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300">
                    <span x-text="t[lang].categories.update">产品更新</span>
                </button>
                <button @click="activeCategory = 'news'" 
                        :class="activeCategory === 'news' ? 'bg-blue-600 text-white shadow-md shadow-blue-500/30' : 'bg-white text-slate-600 hover:bg-slate-50 border border-slate-200'"
                        class="px-5 py-2.5 rounded-full text-sm font-semibold transition-all duration-300">
                    <span x-text="t[lang].categories.news">官方公告</span>
                </button>
            </div>
"""

insert_pos = html.find('<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">')
if insert_pos != -1:
    html = html[:insert_pos] + tabs_ui + html[insert_pos:]

# 4. Add x-show to the article cards
article_card_start = html.find('<article class="article-card')
# We need to replace all instances of this in the template, but since it's Jinja `{% for article in articles %}`, there's only one.
if article_card_start != -1:
    html = html.replace('<article class="article-card', '<article x-show="activeCategory === \'all\' || activeCategory === \'{{ article.category_id }}\'" x-transition:enter="transition ease-out duration-300" x-transition:enter-start="opacity-0 transform scale-95" x-transition:enter-end="opacity-100 transform scale-100" x-transition:leave="transition ease-in duration-200" x-transition:leave-start="opacity-100 transform scale-100" x-transition:leave-end="opacity-0 transform scale-95" class="article-card')

# Write the file
with open('templates/articles.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated articles.html")
