import os
from typing import Dict, List

import requests


MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "")
MINIMAX_GROUP_ID = os.getenv("MINIMAX_GROUP_ID", "")
MINIMAX_BASE_URL = "https://api.minimax.chat/v1"


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

    def text_chat(self, messages: List[Dict], model: str = "MiniMax-M2.7") -> str:
        self._validate_credentials()
        url = f"{MINIMAX_BASE_URL}/text/chatcompletion_v2"
        payload = {
            "model": model,
            "messages": messages,
            "group_id": self.group_id,
        }
        response = requests.post(url, headers=self.headers, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        if "choices" not in result:
            raise RuntimeError(
                f"MiniMax API Error: {result.get('base_resp', {}).get('status_msg', 'Unknown error')}"
            )
        return result["choices"][0]["messages"][-1]["text"]
