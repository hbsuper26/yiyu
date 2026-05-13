import os
import time
from typing import Any, Dict, List

import requests


MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_GROUP_ID = os.getenv("MINIMAX_GROUP_ID", "")
MINIMAX_BASE_URL = "https://api.minimax.chat/v1"
MINIMAX_CHAT_COMPLETIONS_URL = os.getenv(
    "MINIMAX_CHAT_COMPLETIONS_URL",
    f"{MINIMAX_BASE_URL}/chat/completions",
)
MINIMAX_MODEL = os.getenv("MINIMAX_MODEL", "MiniMax-M2.7-Highspeed")
MINIMAX_TIMEOUT_SECONDS = int(os.getenv("MINIMAX_TIMEOUT_SECONDS", "240"))
MINIMAX_MAX_RETRIES = int(os.getenv("MINIMAX_MAX_RETRIES", "3"))


def _looks_like_placeholder(value: str) -> bool:
    if not value:
        return True
    normalized = value.strip().lower()
    placeholder_tokens = [
        "your",
        "placeholder",
        "api_key",
        "group_id",
        "your_api_key",
        "your_group_id",
        "你的_",
        "你的api",
        "你的group",
    ]
    return any(token in normalized for token in placeholder_tokens)


def _ensure_ascii_header_value(name: str, value: str) -> None:
    try:
        value.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError(
            f"{name} 包含非 ASCII 字符，当前看起来仍是占位符或错误配置，请使用真实的 MiniMax 凭证。"
        ) from exc


class MiniMaxClient:
    def __init__(self, api_key: str = None, group_id: str = None):
        self.api_key = api_key or MINIMAX_API_KEY
        self.group_id = group_id or MINIMAX_GROUP_ID
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def _validate_credentials(self) -> None:
        if _looks_like_placeholder(self.api_key) or _looks_like_placeholder(self.group_id):
            raise ValueError(
                "MiniMax API 凭证未正确配置。请将 MINIMAX_API_KEY 和 MINIMAX_GROUP_ID 从占位符替换为真实值后再运行。"
            )
        _ensure_ascii_header_value("MINIMAX_API_KEY", self.api_key)
        _ensure_ascii_header_value("MINIMAX_GROUP_ID", self.group_id)

    def _extract_text(self, result: Dict[str, Any]) -> str:
        choices = result.get("choices") or []
        if not choices:
            raise RuntimeError(
                f"MiniMax API Error: {result.get('base_resp', {}).get('status_msg', 'Missing choices')}"
            )

        first_choice = choices[0]

        if "messages" in first_choice and first_choice["messages"]:
            last_message = first_choice["messages"][-1]
            if isinstance(last_message, dict) and "text" in last_message:
                return last_message["text"]

        message = first_choice.get("message")
        if isinstance(message, dict):
            content = message.get("content")
            if isinstance(content, str) and content.strip():
                return content
            if isinstance(content, list):
                text_parts = []
                for item in content:
                    if isinstance(item, dict):
                        if isinstance(item.get("text"), str):
                            text_parts.append(item["text"])
                        elif item.get("type") == "text" and isinstance(item.get("content"), str):
                            text_parts.append(item["content"])
                if text_parts:
                    return "".join(text_parts)

        if isinstance(first_choice.get("text"), str) and first_choice["text"].strip():
            return first_choice["text"]

        if isinstance(result.get("reply"), str) and result["reply"].strip():
            return result["reply"]

        raise RuntimeError(
            f"MiniMax 返回结构中未找到文本内容，可用顶层字段：{list(result.keys())}，"
            f"choice 字段：{list(first_choice.keys()) if isinstance(first_choice, dict) else type(first_choice).__name__}"
        )

    def text_chat(self, messages: List[Dict], model: str = MINIMAX_MODEL) -> str:
        self._validate_credentials()
        payload = {
            "model": model,
            "messages": messages,
            "group_id": self.group_id,
        }
        last_error = None

        for attempt in range(1, MINIMAX_MAX_RETRIES + 1):
            try:
                response = requests.post(
                    MINIMAX_CHAT_COMPLETIONS_URL,
                    headers=self.headers,
                    json=payload,
                    timeout=MINIMAX_TIMEOUT_SECONDS,
                )
                response.raise_for_status()
                result = response.json()
                return self._extract_text(result)
            except (requests.Timeout, requests.ConnectionError, requests.HTTPError, RuntimeError) as exc:
                last_error = exc
                if attempt == MINIMAX_MAX_RETRIES:
                    break
                # Exponential backoff makes scheduled jobs more tolerant to transient API slowness.
                time.sleep(min(2 ** attempt, 10))

        raise RuntimeError(
            f"MiniMax 请求在 {MINIMAX_MAX_RETRIES} 次尝试后仍失败：{last_error}"
        ) from last_error
