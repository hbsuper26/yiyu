import html
import json
import os
import re
import shutil
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests


class DouyinParseError(Exception):
    pass


REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

ALLOWED_HOST_KEYWORDS = ("douyin.com", "iesdouyin.com")
CACHE_DIR = Path(__file__).resolve().parent / "douyin_cache"
MAX_TRANSCRIBE_FILE_BYTES = 24 * 1024 * 1024


def parse_douyin_video(source_text):
    source_text = (source_text or "").strip()
    source_url = _extract_first_url(source_text)
    if not source_url:
        raise DouyinParseError("请先粘贴抖音视频链接。")

    gateway_result = _parse_with_gateway(source_url)
    if gateway_result:
        return gateway_result

    try:
        resolved_url, page_html = _resolve_page(source_url)
    except DouyinParseError:
        resolved_url, page_html = source_url, ""

    if not _is_douyin_url(resolved_url):
        raise DouyinParseError("当前链接不是可识别的抖音视频地址。")

    video_id = _extract_video_id(resolved_url) or _extract_video_id(source_url)
    cached = _read_cached_result(video_id)
    if cached:
        return cached

    payloads = _extract_json_payloads(page_html)
    aweme = _find_aweme(payloads, video_id) or _fetch_aweme_detail(video_id, resolved_url)

    if not aweme:
        aweme = _fetch_aweme_with_browser(video_id, resolved_url)
        if aweme:
            video_id = str(aweme.get("aweme_id") or video_id or "")
            if video_id and not _extract_video_id(resolved_url):
                resolved_url = f"https://www.douyin.com/video/{video_id}"

    if not aweme:
        if video_id:
            raise DouyinParseError(
                f"已识别到视频 ID：{video_id}，但抖音当前返回的是加密页面或受限接口，暂时无法直接读取播放、点赞等数据。"
                "可以稍后重试，或接入 DOUYIN_PARSE_ENDPOINT 解析服务。"
            )
        raise DouyinParseError("没有从页面中找到公开视频数据，可能是私密、删除、风控或页面结构已变化。")

    video = _build_video_payload(aweme, source_url, resolved_url, video_id)
    transcript = _build_transcript_payload(video)
    analysis = _build_analysis_payload(video, transcript)

    result = {
        "video": video,
        "metrics": _build_metrics_payload(video),
        "transcript": transcript,
        "analysis": analysis,
    }
    _write_cached_result(video.get("id"), result)
    return result


def _extract_first_url(source_text):
    match = re.search(r"https?://[^\s，。！？、；；]+", source_text or "")
    if not match:
        return ""

    url = match.group(0).strip()
    return url.rstrip(".,;，。；、!！?？)'\"”’】》")


def _parse_with_gateway(source_url):
    endpoint = os.environ.get("DOUYIN_PARSE_ENDPOINT", "").strip()
    if not endpoint:
        return None

    try:
        response = requests.post(
            endpoint,
            json={"url": source_url},
            headers={"Accept": "application/json"},
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise DouyinParseError(f"外部抖音解析服务调用失败：{exc}") from exc

    data = payload.get("data") if isinstance(payload, dict) else None
    if not data:
        raise DouyinParseError(payload.get("message", "外部抖音解析服务没有返回有效数据。"))

    return _normalize_gateway_payload(data, source_url)


def _normalize_gateway_payload(data, source_url):
    if data.get("video") and data.get("metrics") and data.get("transcript") and data.get("analysis"):
        return data

    counts = data.get("counts") or data.get("statistics") or {}
    video = {
        "id": str(data.get("id") or data.get("aweme_id") or ""),
        "sourceUrl": source_url,
        "resolvedUrl": data.get("resolvedUrl") or data.get("resolved_url") or source_url,
        "title": data.get("title") or data.get("desc") or "未获取到视频文案",
        "author": {
            "nickname": data.get("author") or data.get("nickname") or "未知作者",
            "uniqueId": data.get("uniqueId") or data.get("unique_id") or "",
            "avatar": data.get("avatar") or "",
        },
        "publishedAt": data.get("publishedAt") or data.get("published_at") or "",
        "durationSeconds": data.get("durationSeconds") or data.get("duration_seconds"),
        "cover": data.get("cover") or "",
        "playUrl": data.get("playUrl") or data.get("play_url") or "",
        "counts": {
            "play": _to_int(counts.get("play") or counts.get("play_count")),
            "like": _to_int(counts.get("like") or counts.get("digg_count")),
            "favorite": _to_int(counts.get("favorite") or counts.get("collect_count")),
            "comment": _to_int(counts.get("comment") or counts.get("comment_count")),
            "share": _to_int(counts.get("share") or counts.get("share_count")),
        },
    }
    transcript = data.get("transcript") or {
        "status": "not_configured",
        "message": "语音转文字服务未配置。",
        "text": data.get("transcriptText") or data.get("transcript_text") or "",
        "segments": data.get("segments") or [],
    }

    return {
        "video": video,
        "metrics": _build_metrics_payload(video),
        "transcript": transcript,
        "analysis": data.get("analysis") or _build_analysis_payload(video, transcript),
    }


def _read_cached_result(video_id):
    if not video_id:
        return None
    cache_path = CACHE_DIR / f"{video_id}.json"
    if not cache_path.exists():
        return None
    try:
        with cache_path.open("r", encoding="utf-8") as file:
            cached = json.load(file)
    except (OSError, json.JSONDecodeError):
        return None
    transcript = cached.get("transcript") or {}
    if _transcription_configured() and transcript.get("status") in ("not_configured", "missing_video_url", "failed", None):
        return None
    return cached


def _write_cached_result(video_id, result):
    if not video_id or not result:
        return
    try:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_path = CACHE_DIR / f"{video_id}.json"
        with cache_path.open("w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=2)
    except OSError:
        pass


def _transcription_configured():
    return bool(
        os.environ.get("DOUYIN_TRANSCRIBE_ENDPOINT", "").strip()
        or os.environ.get("OPENAI_API_KEY", "").strip()
    )


def _resolve_page(source_url):
    try:
        response = requests.get(
            source_url,
            headers=REQUEST_HEADERS,
            allow_redirects=True,
            timeout=12,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise DouyinParseError(f"访问抖音链接失败：{exc}") from exc

    resolved_url = response.url
    page_html = response.text or ""

    if not page_html and resolved_url:
        try:
            second_response = requests.get(
                resolved_url,
                headers=REQUEST_HEADERS,
                allow_redirects=True,
                timeout=12,
            )
            second_response.raise_for_status()
            page_html = second_response.text or ""
            resolved_url = second_response.url
        except requests.RequestException:
            pass

    return resolved_url, page_html


def _fetch_aweme_detail(video_id, resolved_url):
    if not video_id:
        return None

    urls = [
        f"https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids={video_id}",
        f"https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={video_id}&aid=6383&device_platform=webapp",
    ]
    headers = {
        **REQUEST_HEADERS,
        "Accept": "application/json, text/plain, */*",
        "Referer": resolved_url,
    }

    for url in urls:
        try:
            response = requests.get(url, headers=headers, timeout=12)
            response.raise_for_status()
            if not response.text:
                continue
            payload = response.json()
        except (requests.RequestException, ValueError):
            continue

        aweme = _extract_aweme_from_detail_payload(payload)
        if aweme:
            return aweme

    return None


def _fetch_aweme_with_browser(video_id, resolved_url):
    if os.environ.get("DOUYIN_BROWSER_FALLBACK", "1") == "0":
        return None

    try:
        from playwright.sync_api import sync_playwright
    except Exception:
        return None

    executable_path = _find_browser_executable()
    if not executable_path:
        return None

    target_aweme = {"value": None}
    for attempt in range(2):
        if target_aweme["value"]:
            break
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    executable_path=executable_path,
                    args=["--disable-blink-features=AutomationControlled"],
                )
                page = browser.new_page(
                    user_agent=REQUEST_HEADERS["User-Agent"],
                    viewport={"width": 1280, "height": 720},
                )

                def capture_response(response):
                    url = response.url
                    if "/aweme/v1/web/aweme/detail/" not in url:
                        return
                    try:
                        payload = response.json()
                    except Exception:
                        return
                    aweme = _extract_aweme_from_detail_payload(payload)
                    aweme_id = str((aweme or {}).get("aweme_id") or "")
                    if aweme and (not video_id or aweme_id == str(video_id)):
                        target_aweme["value"] = aweme

                page.on("response", capture_response)
                try:
                    page.goto(resolved_url, wait_until="domcontentloaded", timeout=40000)
                    for _ in range(35):
                        if target_aweme["value"]:
                            break
                        page.wait_for_timeout(1000)
                    if not target_aweme["value"]:
                        page.reload(wait_until="domcontentloaded", timeout=30000)
                        for _ in range(12):
                            if target_aweme["value"]:
                                break
                            page.wait_for_timeout(1000)
                except Exception:
                    pass
                finally:
                    browser.close()
        except Exception:
            continue

    return target_aweme["value"]


def _find_browser_executable():
    configured = os.environ.get("DOUYIN_BROWSER_EXECUTABLE", "").strip()
    candidates = [
        configured,
        shutil.which("chrome"),
        shutil.which("msedge"),
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    return ""


def _extract_aweme_from_detail_payload(payload):
    if not isinstance(payload, dict):
        return None

    if _looks_like_aweme(payload.get("aweme_detail")):
        return payload["aweme_detail"]

    item_list = payload.get("item_list") or payload.get("aweme_list") or []
    if isinstance(item_list, list):
        for item in item_list:
            if _looks_like_aweme(item):
                return item

    for candidate in _walk_for_aweme(payload):
        return candidate
    return None


def _is_douyin_url(url):
    try:
        host = urlparse(url).netloc.lower()
    except ValueError:
        return False
    return any(keyword in host for keyword in ALLOWED_HOST_KEYWORDS)


def _extract_video_id(url):
    patterns = [
        r"/video/(\d+)",
        r"/note/(\d+)",
        r"[?&](?:modal_id|aweme_id|item_id)=(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def _extract_json_payloads(page_html):
    payloads = []
    if not page_html:
        return payloads

    script_patterns = [
        r'<script[^>]+id=["\']RENDER_DATA["\'][^>]*>(.*?)</script>',
        r'<script[^>]+id=["\']SIGI_STATE["\'][^>]*>(.*?)</script>',
        r'<script[^>]+id=["\']__UNIVERSAL_DATA_FOR_REHYDRATION__["\'][^>]*>(.*?)</script>',
    ]
    for pattern in script_patterns:
        for raw in re.findall(pattern, page_html, flags=re.S):
            loaded = _loads_json(raw)
            if loaded is not None:
                payloads.append(loaded)

    window_patterns = [
        r"window\.__INITIAL_STATE__\s*=\s*({.*?})\s*</script>",
        r"window\.__UNIVERSAL_DATA_FOR_REHYDRATION__\s*=\s*({.*?})\s*</script>",
    ]
    for pattern in window_patterns:
        match = re.search(pattern, page_html, flags=re.S)
        if match:
            loaded = _loads_json(match.group(1))
            if loaded is not None:
                payloads.append(loaded)

    return payloads


def _loads_json(raw):
    raw = html.unescape(raw or "").strip()
    if not raw:
        return None

    candidates = [raw, unquote(raw)]
    for candidate in candidates:
        candidate = candidate.strip()
        if not candidate:
            continue
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return None


def _find_aweme(payloads, video_id):
    candidates = []
    for payload in payloads:
        candidates.extend(_walk_for_aweme(payload))

    if video_id:
        for candidate in candidates:
            if str(candidate.get("aweme_id") or candidate.get("id") or "") == str(video_id):
                return candidate

    return candidates[0] if candidates else None


def _walk_for_aweme(node):
    found = []
    if isinstance(node, dict):
        if _looks_like_aweme(node):
            found.append(node)
        for value in node.values():
            found.extend(_walk_for_aweme(value))
    elif isinstance(node, list):
        for item in node:
            found.extend(_walk_for_aweme(item))
    return found


def _looks_like_aweme(node):
    return (
        isinstance(node, dict)
        and isinstance(node.get("statistics"), dict)
        and (node.get("aweme_id") or node.get("desc") or node.get("video"))
    )


def _build_video_payload(aweme, source_url, resolved_url, video_id):
    statistics = aweme.get("statistics") or {}
    author = aweme.get("author") or {}
    video = aweme.get("video") or {}
    create_time = _to_int(aweme.get("create_time"))
    duration_ms = _to_int(video.get("duration"))
    real_video_id = str(aweme.get("aweme_id") or video_id or "")

    return {
        "id": real_video_id,
        "sourceUrl": source_url,
        "resolvedUrl": resolved_url,
        "title": aweme.get("desc") or aweme.get("title") or "未获取到视频文案",
        "author": {
            "nickname": author.get("nickname") or "未知作者",
            "uniqueId": author.get("unique_id") or author.get("short_id") or "",
            "avatar": _first_url((author.get("avatar_thumb") or {}).get("url_list")),
        },
        "publishedAt": _format_datetime(create_time),
        "durationSeconds": round(duration_ms / 1000, 1) if duration_ms else None,
        "cover": _first_url((video.get("cover") or {}).get("url_list"))
        or _first_url((video.get("origin_cover") or {}).get("url_list"))
        or _first_url((video.get("dynamic_cover") or {}).get("url_list")),
        "playUrl": _extract_play_url(video),
        "counts": {
            "play": _to_int(statistics.get("play_count")),
            "like": _to_int(statistics.get("digg_count")),
            "favorite": _to_int(statistics.get("collect_count")),
            "comment": _to_int(statistics.get("comment_count")),
            "share": _to_int(statistics.get("share_count")),
        },
    }


def _extract_play_url(video):
    direct = _first_url((video.get("play_addr") or {}).get("url_list"))
    if direct:
        return direct

    for bit_rate in video.get("bit_rate") or []:
        play_url = _first_url(((bit_rate or {}).get("play_addr") or {}).get("url_list"))
        if play_url:
            return play_url
    return ""


def _first_url(urls):
    if isinstance(urls, list) and urls:
        return urls[0]
    if isinstance(urls, str):
        return urls
    return ""


def _to_int(value):
    if value in (None, ""):
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _format_datetime(timestamp):
    if not timestamp:
        return ""
    try:
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
    except (OSError, OverflowError, ValueError):
        return ""


def _build_metrics_payload(video):
    counts = video["counts"]
    play = counts.get("play") or 0

    return {
        "likeRate": _rate(counts.get("like"), play),
        "favoriteRate": _rate(counts.get("favorite"), play),
        "commentRate": _rate(counts.get("comment"), play),
        "shareRate": _rate(counts.get("share"), play),
        "engagementRate": _rate(
            (counts.get("like") or 0)
            + (counts.get("favorite") or 0)
            + (counts.get("comment") or 0)
            + (counts.get("share") or 0),
            play,
        ),
    }


def _rate(numerator, denominator):
    numerator = numerator or 0
    denominator = denominator or 0
    if not denominator:
        return {"value": None, "label": "暂无播放量"}
    value = numerator / denominator
    return {"value": value, "label": f"{value * 100:.2f}%"}


def _build_transcript_payload(video):
    endpoint = os.environ.get("DOUYIN_TRANSCRIBE_ENDPOINT", "").strip()
    if endpoint:
        return _transcribe_with_endpoint(video, endpoint)

    if os.environ.get("OPENAI_API_KEY", "").strip():
        return _transcribe_with_openai(video)

    return {
        "status": "not_configured",
        "message": "语音转文字服务未配置。线上配置 OPENAI_API_KEY 后，可自动提取视频讲话文字。",
        "text": "",
        "segments": [],
    }


def _transcribe_with_endpoint(video, endpoint):
    if not endpoint:
        return {
            "status": "not_configured",
            "message": "语音转文字服务未配置。配置 DOUYIN_TRANSCRIBE_ENDPOINT 后，可自动提取视频讲话文字。",
            "text": "",
            "segments": [],
        }

    if not video.get("playUrl"):
        return {
            "status": "missing_video_url",
            "message": "未获取到可用于转写的视频播放地址。",
            "text": "",
            "segments": [],
        }

    try:
        response = requests.post(
            endpoint,
            json={
                "video_url": video["playUrl"],
                "source_url": video["sourceUrl"],
                "video_id": video["id"],
                "title": video["title"],
            },
            timeout=90,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as exc:
        return {
            "status": "failed",
            "message": f"语音转文字服务调用失败：{exc}",
            "text": "",
            "segments": [],
        }
    except ValueError:
        return {
            "status": "failed",
            "message": "语音转文字服务没有返回有效 JSON。",
            "text": "",
            "segments": [],
        }

    text = payload.get("text") or ""
    segments = payload.get("segments") or []
    return {
        "status": "ready" if text or segments else "empty",
        "message": payload.get("message") or "",
        "text": text,
        "segments": segments,
    }


def _transcribe_with_openai(video):
    if not video.get("playUrl"):
        return {
            "status": "missing_video_url",
            "message": "未获取到可用于转写的视频播放地址。",
            "text": "",
            "segments": [],
        }

    temp_path = None
    try:
        temp_path = _download_video_for_transcription(video["playUrl"])
        return _call_openai_transcription(temp_path)
    except Exception as exc:
        return {
            "status": "failed",
            "message": f"语音转文字失败：{exc}",
            "text": "",
            "segments": [],
        }
    finally:
        if temp_path:
            try:
                os.remove(temp_path)
            except OSError:
                pass


def _download_video_for_transcription(play_url):
    response = requests.get(
        play_url,
        headers={
            **REQUEST_HEADERS,
            "Referer": "https://www.douyin.com/",
        },
        stream=True,
        timeout=45,
    )
    response.raise_for_status()

    content_length = _to_int(response.headers.get("content-length"))
    if content_length and content_length > MAX_TRANSCRIBE_FILE_BYTES:
        raise DouyinParseError("视频文件超过语音识别 25MB 限制，暂不支持自动转写。")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
        total = 0
        for chunk in response.iter_content(chunk_size=1024 * 512):
            if not chunk:
                continue
            total += len(chunk)
            if total > MAX_TRANSCRIBE_FILE_BYTES:
                temp_file.close()
                os.remove(temp_file.name)
                raise DouyinParseError("视频文件超过语音识别 25MB 限制，暂不支持自动转写。")
            temp_file.write(chunk)
        return temp_file.name


def _call_openai_transcription(file_path):
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe").strip()
    response_format = "json"
    if model == "whisper-1":
        response_format = "verbose_json"

    with open(file_path, "rb") as audio_file:
        response = requests.post(
            f"{base_url}/audio/transcriptions",
            headers={"Authorization": f"Bearer {api_key}"},
            data={
                "model": model,
                "language": "zh",
                "response_format": response_format,
            },
            files={"file": ("douyin-video.mp4", audio_file, "video/mp4")},
            timeout=180,
        )
    response.raise_for_status()
    payload = response.json()

    text = payload.get("text") or ""
    segments = []
    for segment in payload.get("segments") or []:
        segments.append({
            "start": segment.get("start", 0),
            "end": segment.get("end", 0),
            "text": segment.get("text", ""),
        })

    return {
        "status": "ready" if text or segments else "empty",
        "message": "",
        "text": text,
        "segments": segments,
    }


def _build_analysis_payload(video, transcript):
    source_text = transcript.get("text") or video.get("title") or ""
    summary = _make_summary(source_text, transcript.get("status"))

    return {
        "summary": summary,
        "keywords": _extract_keywords(source_text),
    }


def _make_summary(text, transcript_status):
    clean = re.sub(r"\s+", " ", text or "").strip()
    if not clean:
        return "暂未获取到可用于摘要的文字内容。"

    prefix = "视频口播摘要" if transcript_status == "ready" else "基于视频文案的摘要"
    return f"{prefix}：{clean[:140]}{'...' if len(clean) > 140 else ''}"


def _extract_keywords(text):
    text = text or ""
    words = re.findall(r"[A-Za-z0-9]{2,}|[\u4e00-\u9fff]{2,6}", text)
    stopwords = {
        "一个",
        "这个",
        "那个",
        "我们",
        "你们",
        "他们",
        "可以",
        "就是",
        "今天",
        "视频",
        "抖音",
    }
    counter = Counter(word for word in words if word not in stopwords)
    return [word for word, _count in counter.most_common(8)]
