import html
import re
import shutil
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parent
DB_PATH = REPO_DIR / "yiyu.db"
DIST_ARTICLE_DIR = REPO_DIR / "dist" / "article"
TARGET_IDS = range(1, 33)
HISTORY_SOURCES = {
    range(1, 21): "c79f51b",
    range(21, 33): "0cca0b2",
}


def backup_db() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = REPO_DIR / f"yiyu.db.backup-{timestamp}"
    shutil.copy2(DB_PATH, backup_path)
    return backup_path


def load_article_html(article_id: int) -> str:
    source_commit = None
    for id_range, commit in HISTORY_SOURCES.items():
        if article_id in id_range:
            source_commit = commit
            break

    if source_commit is None:
        local_path = DIST_ARTICLE_DIR / str(article_id)
        if local_path.exists():
            return local_path.read_text(encoding="utf-8")
        raise FileNotFoundError(f"未找到文章 {article_id} 的恢复来源。")

    blob = subprocess.check_output(
        ["git", "-C", str(REPO_DIR), "show", f"{source_commit}:dist/article/{article_id}"]
    )
    return blob.decode("utf-8", errors="ignore")


def extract(pattern: str, text: str, default: str = "") -> str:
    match = re.search(pattern, text, re.S)
    return html.unescape(match.group(1).strip()) if match else default


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def category_to_id(category_label: str) -> str:
    mapping = {
        "官方公告": "news",
        "行业洞察": "insight",
        "投放指南": "guide",
        "产品更新": "update",
        "资讯": "news",
    }
    return mapping.get(category_label.strip(), "news")


def parse_article(article_id: int, html_text: str) -> dict:
    header = extract(r"<header class=\"mb-10 text-center\">(.*?)</header>", html_text)
    title = extract(r"<h1[^>]*>\s*<span x-show=\"lang === 'zh'\">(.*?)</span>", header)
    title_en = extract(r"<h1[^>]*>.*?<span x-show=\"lang === 'en'\"[^>]*>(.*?)</span>", header)
    category_label = extract(
        r"<span class=\"px-3 py-1 bg-blue-50 text-blue-600 text-xs font-bold rounded-lg uppercase tracking-wider\">.*?<span x-show=\"lang === 'zh'\">\s*([^<\n]+)",
        header,
        "资讯",
    )
    date = extract(r"<i class=\"far fa-calendar-alt\"></i>\s*<span>(.*?)</span>", header)
    views_raw = extract(r"<i class=\"far fa-eye\"></i>\s*<span>(\d+)", header, "0")
    featured_block = extract(r"<!-- Featured Image -->(.*?)<!-- Rich Text Body -->", html_text)
    image = extract(r"<img src=\"(.*?)\" alt=\"Featured Image\"", featured_block)
    content = extract(
        r"<div class=\"prose max-w-none\" x-show=\"lang === 'zh'\">\s*(.*?)\s*</div>\s*<div class=\"prose max-w-none\" x-show=\"lang === 'en'\"",
        html_text,
    )
    content_en = extract(
        r"<div class=\"prose max-w-none\" x-show=\"lang === 'en'\"[^>]*>\s*(.*?)\s*</div>\s*<!-- Social Share",
        html_text,
    )

    summary_source = extract(r"<blockquote>(.*?)</blockquote>", content) or extract(r"<p>(.*?)</p>", content)
    summary = strip_tags(summary_source)[:120]
    summary_en_source = extract(r"<blockquote>(.*?)</blockquote>", content_en) or extract(r"<p>(.*?)</p>", content_en)
    summary_en = strip_tags(summary_en_source)[:180]

    return {
        "id": article_id,
        "category_id": category_to_id(category_label),
        "title": title,
        "summary": summary,
        "content": content,
        "date": date,
        "views": int(views_raw or 0),
        "image": image,
        "seo_keywords": "",
        "seo_score": 0,
        "title_en": title_en,
        "summary_en": summary_en,
        "content_en": content_en,
        "title_vi": "",
        "summary_vi": "",
        "content_vi": "",
    }


def restore_articles() -> int:
    backup_path = backup_db()
    print(f"已备份数据库: {backup_path.name}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    restored_count = 0
    for article_id in TARGET_IDS:
        article = parse_article(article_id, load_article_html(article_id))
        cur.execute(
            """
            INSERT OR REPLACE INTO articles (
                id, category_id, title, summary, content, date, views, image,
                seo_keywords, seo_score, title_en, summary_en, content_en,
                title_vi, summary_vi, content_vi
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                article["id"],
                article["category_id"],
                article["title"],
                article["summary"],
                article["content"],
                article["date"],
                article["views"],
                article["image"],
                article["seo_keywords"],
                article["seo_score"],
                article["title_en"],
                article["summary_en"],
                article["content_en"],
                article["title_vi"],
                article["summary_vi"],
                article["content_vi"],
            ),
        )
        restored_count += 1

    conn.commit()
    conn.close()
    return restored_count


if __name__ == "__main__":
    restored = restore_articles()
    print(f"恢复完成，本次补回 {restored} 篇历史文章。")
