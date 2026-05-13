import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import agent


def make_article_payload(**overrides):
    payload = {
        "title": "TikTok 出海广告投放策略详解",
        "title_en": "TikTok Overseas Advertising Strategy Guide",
        "summary": "围绕投放策略、素材测试和预算控制的精简摘要。",
        "summary_en": "A concise summary covering strategy, creative testing, and budget control.",
        "category_id": "news",
        "content": "## 中文正文\n\n> 引言\n\n这是一篇足够完整的中文正文。",
        "content_en": "## English Content\n\n> Intro\n\nThis is a sufficiently complete English article.",
        "seo_keywords": "tiktok ads,overseas marketing,performance creative",
    }
    payload.update(overrides)
    return payload


class FakeMiniMaxClient:
    responses = []

    def __init__(self, *args, **kwargs):
        self._index = 0

    def text_chat(self, messages):
        if self._index >= len(self.responses):
            raise AssertionError("FakeMiniMaxClient responses exhausted")
        response = self.responses[self._index]
        self._index += 1
        return response


class AgentJsonResilienceTests(unittest.TestCase):
    def test_a_parses_json_wrapped_in_explanation_and_code_fence(self):
        wrapped_response = (
            "下面是按要求生成的内容，请查收。\n"
            "```json\n"
            f"{json.dumps(make_article_payload(), ensure_ascii=False)}\n"
            "```\n"
            "以上就是结果。"
        )

        article_data = agent._parse_article_response(wrapped_response)

        self.assertEqual(article_data["title"], "TikTok 出海广告投放策略详解")
        self.assertEqual(article_data["category_id"], "news")
        self.assertIn("performance creative", article_data["seo_keywords"])

    def test_b_normalizes_alias_category_and_keyword_list(self):
        response = json.dumps(
            make_article_payload(
                category_id="analysis",
                seo_keywords=["global ads", "account safety", "roi optimization"],
            ),
            ensure_ascii=False,
        )

        article_data = agent._parse_article_response(response)

        self.assertEqual(article_data["category_id"], "insight")
        self.assertEqual(
            article_data["seo_keywords"],
            "global ads,account safety,roi optimization",
        )

    def test_c_retries_invalid_response_and_persists_daily_articles(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test_articles.db"
            conn = sqlite3.connect(db_path)
            conn.execute(
                """
                CREATE TABLE articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    content TEXT NOT NULL,
                    date TEXT NOT NULL,
                    views INTEGER DEFAULT 0,
                    image TEXT NOT NULL,
                    seo_keywords TEXT DEFAULT '',
                    title_en TEXT NOT NULL,
                    summary_en TEXT NOT NULL,
                    content_en TEXT NOT NULL
                )
                """
            )
            conn.commit()
            conn.close()

            def open_test_db():
                test_conn = sqlite3.connect(db_path)
                test_conn.row_factory = sqlite3.Row
                return test_conn

            FakeMiniMaxClient.responses = [
                "这不是 JSON",
                f"```json\n{json.dumps(make_article_payload(), ensure_ascii=False)}\n```",
                json.dumps(
                    make_article_payload(
                        title="Google Ads 账户风控实战",
                        title_en="Google Ads Account Risk Control",
                        category_id="analysis",
                        seo_keywords=["google ads", "account safety", "appeal process"],
                    ),
                    ensure_ascii=False,
                ),
                json.dumps(
                    make_article_payload(
                        title="Meta 广告素材测试框架",
                        title_en="Meta Creative Testing Framework",
                        category_id="guide",
                    ),
                    ensure_ascii=False,
                ),
            ]

            with patch.object(agent, "MiniMaxClient", FakeMiniMaxClient), patch.object(
                agent, "get_db_connection", side_effect=open_test_db
            ), patch.object(
                agent.random,
                "sample",
                return_value=["topic-a", "topic-b", "topic-c"],
            ), patch.object(
                agent.random,
                "randint",
                side_effect=[101, 11, 202, 22, 303, 33],
            ), patch.object(agent.time, "sleep", return_value=None):
                success_count = agent.generate_daily_articles()

            self.assertEqual(success_count, 3)

            check_conn = sqlite3.connect(db_path)
            rows = check_conn.execute(
                "SELECT title, category_id, seo_keywords FROM articles ORDER BY id"
            ).fetchall()
            check_conn.close()

            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0][0], "TikTok 出海广告投放策略详解")
            self.assertEqual(rows[1][1], "insight")
            self.assertEqual(rows[1][2], "google ads,account safety,appeal process")
            self.assertEqual(rows[2][1], "guide")


if __name__ == "__main__":
    unittest.main()
