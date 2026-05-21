import json
import os
import random
import re
import sys
import time
from datetime import datetime, timedelta, timezone

# Add the current directory to sys.path so we can import local helpers.
sys.path.append(os.path.dirname(__file__))
from db import get_db_connection
from minimax_utils import MiniMaxClient


DAILY_ARTICLE_COUNT = 3
VALID_CATEGORY_IDS = {"news", "insight", "guide", "update"}
BEIJING_TZ = timezone(timedelta(hours=8))

ARTICLE_FORMATS = [
    "运营清单：用可执行步骤和检查项组织，不要写成长篇论文",
    "案例拆解：用一个具体场景开头，拆出问题、判断、处理动作和结果",
    "问答短文：用 4-6 个真实业务问题展开，答案要直接、有判断",
    "周报观察：像行业编辑短评，突出本周变化、影响和建议",
    "SOP 手册：按步骤写，适合运营同事照着执行",
    "观点评论：先给明确结论，再用少量事实和运营经验支撑",
]


def beijing_now():
    return datetime.now(BEIJING_TZ)


def analyze_seo_performance():
    """
    Use historical high-performing articles as light SEO context.
    """
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT title, seo_keywords, views FROM articles ORDER BY views DESC LIMIT 5")
    top_articles = c.fetchall()
    conn.close()

    if not top_articles:
        return "暂无历史数据，请围绕海外广告账户、充值管理、素材投放、出海增长写作。"

    analysis = "历史阅读表现较好的主题如下，可参考但不要照抄结构：\n"
    for art in top_articles:
        analysis += f"- 标题: {art['title']} | 关键词: {art['seo_keywords']} | 浏览量: {art['views']}\n"
    return analysis


def generate_article(client, topic, seo_context, article_format):
    """
    Generate one medium-length SEO article with a varied editorial structure.
    """
    system_prompt = f"""
你是“以渔数媒”的内容编辑、海外广告投放顾问和 SEO 优化师。
以渔数媒服务出海企业，核心场景包括海外广告账户开户、充值、余额预警、多账户管理、广告素材投放、财务对账与投放风控。

{seo_context}

本篇文章采用这种形式：{article_format}

写作要求：
1. 中文正文控制在 900-1400 字左右，英文正文为专业翻译，不要写成 2000 字以上的长文。
2. 每篇文章都要有不同的结构，不要固定写“背景-策略-总结”三段式。
3. 内容要具体，优先写投放、账户、充值、素材、对账、风控中的真实运营问题。
4. 可以使用清单、步骤、案例、问答、短评、SOP 等形式，让文章看起来有新意。
5. 不要编造夸张数据；如需举例，用“某工具类 App”“某跨境电商团队”等匿名案例。
6. 标题不要总是“深度解析”“完整指南”，要更像真实官网文章标题。
7. Markdown 正文至少包含 2 个二级标题，可以包含三级标题、引用或列表，但不要堆砌。
8. SEO 关键词自然出现即可，不要机械重复。

必须只输出一个合法 JSON 对象，不要输出代码块、前言或解释。字段如下：
{{
  "title": "中文标题",
  "title_en": "英文标题",
  "summary": "中文摘要，80-120 字",
  "summary_en": "英文摘要",
  "category_id": "必须是 news、insight、guide、update 之一",
  "content": "中文 Markdown 正文",
  "content_en": "英文 Markdown 正文",
  "seo_keywords": "3-5 个长尾关键词，用逗号分隔"
}}
"""

    user_prompt = (
        f"请以“{topic}”为主题或灵感，生成一篇适合以渔官网发布的 SEO 文章。"
        f"文章形式必须体现：{article_format}。"
    )

    last_error = None
    for attempt in range(1, 4):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        if attempt > 1:
            messages.append(
                {
                    "role": "user",
                    "content": (
                        "上一版输出未能被系统解析。请重新输出，并严格满足："
                        "1. 只返回一个合法 JSON 对象；"
                        "2. 不要输出 ```json 代码块标记；"
                        "3. 不要有任何前言、解释或结尾说明；"
                        "4. 所有必填字段都要非空；"
                        "5. 正文不要超长，保持中等篇幅。"
                    ),
                }
            )

        response_text = client.text_chat(messages)
        try:
            return _parse_article_response(response_text)
        except Exception as exc:
            last_error = exc

    raise RuntimeError(f"文章 JSON 解析失败，重试 3 次后仍未成功：{last_error}") from last_error


def _strip_code_fence(text: str) -> str:
    stripped = text.strip()
    if stripped.startswith("```json"):
        stripped = stripped[7:]
    elif stripped.startswith("```"):
        stripped = stripped[3:]
    if stripped.endswith("```"):
        stripped = stripped[:-3]
    return stripped.strip()


def _extract_json_object(text: str) -> str:
    stripped = _strip_code_fence(text)
    if not stripped:
        raise ValueError("模型返回了空内容")

    if stripped.startswith("{") and stripped.endswith("}"):
        return stripped

    match = re.search(r"\{[\s\S]*\}", stripped)
    if not match:
        raise ValueError(f"未在模型输出中找到 JSON 对象，输出前 200 字符：{stripped[:200]}")
    return match.group(0)


def _normalize_article_data(article_data: dict) -> dict:
    required_fields = [
        "title",
        "title_en",
        "summary",
        "summary_en",
        "category_id",
        "content",
        "content_en",
        "seo_keywords",
    ]
    for field in required_fields:
        value = article_data.get(field)
        if isinstance(value, str):
            article_data[field] = value.strip()
        if not article_data.get(field):
            raise ValueError(f"字段 {field} 为空")

    category_id = article_data["category_id"].strip().lower()
    if category_id not in VALID_CATEGORY_IDS:
        category_map = {
            "official": "news",
            "announcement": "news",
            "analysis": "insight",
            "insights": "insight",
            "tutorial": "guide",
            "howto": "guide",
            "product": "update",
        }
        category_id = category_map.get(category_id, "insight")
    article_data["category_id"] = category_id

    if isinstance(article_data["seo_keywords"], list):
        article_data["seo_keywords"] = ",".join(
            str(item).strip() for item in article_data["seo_keywords"] if str(item).strip()
        )

    return article_data


def _parse_article_response(response_text: str) -> dict:
    json_text = _extract_json_object(response_text)
    article_data = json.loads(json_text)
    if not isinstance(article_data, dict):
        raise ValueError("模型返回的 JSON 不是对象")
    return _normalize_article_data(article_data)


def generate_daily_articles():
    """
    Generate a small daily batch to keep scheduled runs stable.
    """
    print(
        f"[{beijing_now().strftime('%Y-%m-%d %H:%M:%S')}] "
        f"Starting AI Agent to generate {DAILY_ARTICLE_COUNT} daily articles..."
    )

    client = MiniMaxClient()
    seo_context = analyze_seo_performance()
    print("SEO feedback loaded:\n", seo_context)

    base_topics = [
        "广告账户余额预警如何避免放量中断",
        "TikTok Shop 新品冷启动素材池搭建",
        "Google Ads 账户申诉材料怎么准备",
        "Meta 广告素材复盘如何区分能跑和能卖",
        "多账户投放团队如何做账户分层管理",
        "海外广告充值、消耗和发票如何统一对账",
        "东南亚与拉美市场投放本地化常见误区",
        "AI 广告文案如何避免同质化",
        "出海广告合规巡检 SOP",
        "跨境电商独立站投放预算如何分配",
        "代理开户服务为什么需要系统化看板",
        "企业级海外广告资金管理的运营指标",
    ]

    daily_topics = random.sample(base_topics, DAILY_ARTICLE_COUNT)
    daily_formats = random.sample(ARTICLE_FORMATS, DAILY_ARTICLE_COUNT)

    conn = get_db_connection()
    c = conn.cursor()

    success_count = 0
    for i, (topic, article_format) in enumerate(zip(daily_topics, daily_formats)):
        print(f"\nGenerating article {i + 1}/{DAILY_ARTICLE_COUNT}: {topic} ({article_format})")
        try:
            article_data = generate_article(client, topic, seo_context, article_format)

            seed = random.randint(100, 9999)
            image_url = f"https://picsum.photos/seed/yiyu{seed}/800/500"
            date_str = beijing_now().strftime("%Y-%m-%d")
            views = random.randint(10, 100)

            c.execute(
                """
                INSERT INTO articles (
                    category_id, title, summary, content, date, views, image,
                    seo_keywords, title_en, summary_en, content_en
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    article_data["category_id"],
                    article_data["title"],
                    article_data["summary"],
                    article_data["content"],
                    date_str,
                    views,
                    image_url,
                    article_data.get("seo_keywords", ""),
                    article_data.get("title_en", ""),
                    article_data.get("summary_en", ""),
                    article_data.get("content_en", ""),
                ),
            )

            success_count += 1
            print(f"Success: {article_data['title']}")
            time.sleep(2)
        except Exception as e:
            print(f"Failed to generate article for topic '{topic}': {e}")

    conn.commit()
    conn.close()
    print(
        f"\n[{beijing_now().strftime('%Y-%m-%d %H:%M:%S')}] Batch generation complete. "
        f"Successfully published {success_count}/{DAILY_ARTICLE_COUNT} articles."
    )
    return success_count


if __name__ == "__main__":
    generate_daily_articles()
