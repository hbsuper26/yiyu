import sys
import os
import json
from datetime import datetime
import random
import time

# Add the parent directory to sys.path so we can import minimax_utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
# Add the current directory to sys.path so we can import db
sys.path.append(os.path.dirname(__file__))
from bravo_pay.minimax_utils import MiniMaxClient
from db import get_db_connection

def analyze_seo_performance():
    """
    Analyzes the database for high-performing articles (by views)
    and extracts successful SEO keywords/topics to guide future generation.
    """
    conn = get_db_connection()
    c = conn.cursor()
    # Get top 5 articles by views
    c.execute('SELECT title, seo_keywords, views FROM articles ORDER BY views DESC LIMIT 5')
    top_articles = c.fetchall()
    conn.close()
    
    if not top_articles:
        return "暂无历史数据，请自由发挥"
        
    analysis = "根据历史数据，以下主题和关键词表现较好，请在生成时作为参考：\n"
    for art in top_articles:
        analysis += f"- 标题: {art['title']} | 关键词: {art['seo_keywords']} | 浏览量: {art['views']}\n"
    
    return analysis

def generate_article(client, topic, seo_context):
    """
    Generates a single article using the MiniMax API.
    """
    system_prompt = f"""
    你是一个资深的全球广告出海营销专家、SEO优化师和SaaS产品经理，目前在"以渔数媒"工作。
    "以渔数媒"是一个企业级海外广告账户开户、充值管理平台，主要解决出海企业资金流转慢、多账户管理难的问题。
    
    {seo_context}
    
    请根据提供的主题，结合SEO优化原则（自然融入长尾词、吸引点击的标题、清晰的结构），写一篇高质量的行业动态/技术干货文章。要求内容极其详实、包含具体的实操建议或案例数据。
    
    必须以 JSON 格式输出，包含以下字段（请同时生成中文和英文版本）：
    {{
      "title": "文章标题（中文，吸引人、包含核心关键词）",
      "title_en": "文章标题（英文）",
      "summary": "文章的摘要（中文，100字以内，简明扼要，适合meta description）",
      "summary_en": "文章的摘要（英文）",
      "category_id": "必须是这几个之一：news(官方公告), insight(行业洞察), guide(投放指南), update(产品更新)",
      "content": "文章正文（中文）。使用 Markdown 格式排版，必须包含多级标题（h2(##)、h3(###)）、长段落深度论述、加粗划重点、引言(> )、以及具体实操案例或数据支撑。字数要求 2000-3000 字左右，内容必须极其详实、结构极其丰富、有极高的专业深度和实战价值，自然融入相关关键词。",
      "content_en": "文章正文（英文）。对中文正文的精准专业翻译，同样保留丰富的 Markdown 多级排版和长篇幅的深度内容。",
      "seo_keywords": "3-5个核心长尾关键词，用逗号分隔"
    }}
    只输出 JSON，不要输出其他多余的解释。
    """
    
    user_prompt = f"请以《{topic}》为主题或灵感来源，生成一篇符合SEO标准的优质文章。"
    
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    
    response_text = client.text_chat(messages, model='MiniMax-M2.7')
    
    # Clean up JSON formatting
    if response_text.startswith("```json"):
        response_text = response_text[7:-3].strip()
    elif response_text.startswith("```"):
        response_text = response_text[3:-3].strip()
        
    return json.loads(response_text)

def generate_daily_articles():
    """
    Generates a batch of 6 articles, utilizing SEO feedback from previous runs.
    """
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Starting AI Agent to generate 6 daily articles...")
    
    client = MiniMaxClient()
    seo_context = analyze_seo_performance()
    print("SEO Feedback loaded:\n", seo_context)
    
    base_topics = [
        "TikTok 短视频广告出海投放策略与ROI提升",
        "Google Ads 搜索广告账户防封技巧与申诉",
        "Meta (Facebook) 广告高转化素材设计指南",
        "海外游戏发行的买量成本(CAC)深度分析",
        "出海电商独立站引流最新玩法与转化优化",
        "企业级海外资金管理系统如何解决汇损问题",
        "东南亚/拉美新兴市场广告投放本地化指南",
        "AI技术在海外广告创意与素材生成中的应用",
        "出海合规：不同媒体平台的最新政策解读",
        "如何通过精细化账户架构提升投放效率"
    ]
    
    # Select 6 unique topics for today's batch
    daily_topics = random.sample(base_topics, 6)
    
    conn = get_db_connection()
    c = conn.cursor()
    
    success_count = 0
    for i, topic in enumerate(daily_topics):
        print(f"\nGenerating article {i+1}/6: {topic}")
        try:
            article_data = generate_article(client, topic, seo_context)
            
            # Add random image
            seed = random.randint(100, 9999)
            image_url = f"https://picsum.photos/seed/yiyu{seed}/800/500"
            
            date_str = datetime.now().strftime('%Y-%m-%d')
            # Initial views, might be updated later by user traffic
            views = random.randint(10, 100) 
            
            c.execute('''
                INSERT INTO articles (category_id, title, summary, content, date, views, image, seo_keywords, title_en, summary_en, content_en)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article_data['category_id'],
                article_data['title'],
                article_data['summary'],
                article_data['content'],
                date_str,
                views,
                image_url,
                article_data.get('seo_keywords', ''),
                article_data.get('title_en', ''),
                article_data.get('summary_en', ''),
                article_data.get('content_en', '')
            ))
            
            success_count += 1
            print(f"Success: {article_data['title']}")
            
            # Sleep slightly to avoid rate limiting
            time.sleep(2)
            
        except Exception as e:
            print(f"Failed to generate article for topic '{topic}': {e}")
            
    conn.commit()
    conn.close()
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Batch generation complete. Successfully published {success_count}/6 articles.")

if __name__ == '__main__':
    generate_daily_articles()