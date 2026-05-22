function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

const headers = {
  "user-agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
  accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
};

export async function onRequestPost({ request, env }) {
  let body = {};
  try {
    body = await request.json();
  } catch {
    body = {};
  }

  const sourceUrl = extractFirstUrl(String(body.url || ""));
  if (!sourceUrl) {
    return json({ success: false, message: "请先粘贴抖音视频链接。" }, 400);
  }

  try {
    const parsed = await parseDouyinVideo(sourceUrl, env);
    return json({ success: true, data: parsed });
  } catch (error) {
    return json({ success: false, message: error.message || "解析失败" }, 400);
  }
}

function extractFirstUrl(sourceText) {
  const match = String(sourceText || "").match(/https?:\/\/[^\s，。！？、；;]+/);
  if (!match) return "";
  return match[0].replace(/[.,;，。；、!！?？)'"”’】》]+$/g, "");
}

async function parseDouyinVideo(sourceUrl, env) {
  const gatewayResult = await parseWithGateway(sourceUrl, env);
  if (gatewayResult) return gatewayResult;

  const response = await fetch(sourceUrl, {
    headers,
    redirect: "follow",
  });

  if (!response.ok) {
    throw new Error(`访问抖音链接失败：HTTP ${response.status}`);
  }

  const resolvedUrl = response.url;
  if (!isDouyinUrl(resolvedUrl)) {
    throw new Error("当前链接不是可识别的抖音视频地址。");
  }

  const pageHtml = await response.text();
  const videoId = extractVideoId(resolvedUrl) || extractVideoId(sourceUrl);
  const payloads = extractJsonPayloads(pageHtml);
  const aweme = findAweme(payloads, videoId) || (await fetchAwemeDetail(videoId, resolvedUrl));

  if (!aweme) {
    if (videoId) {
      throw new Error(
        `已识别到视频 ID：${videoId}，但抖音当前返回的是加密页面或受限接口，暂时无法直接读取播放、点赞等数据。可以稍后重试，或接入 DOUYIN_PARSE_ENDPOINT 解析服务。`
      );
    }
    throw new Error("没有从页面中找到公开视频数据，可能是私密、删除、风控或页面结构已变化。");
  }

  const video = buildVideoPayload(aweme, sourceUrl, resolvedUrl, videoId);
  const transcript = await buildTranscriptPayload(video, env);
  const analysis = buildAnalysisPayload(video, transcript);

  return {
    video,
    metrics: buildMetricsPayload(video),
    transcript,
    analysis,
  };
}

async function parseWithGateway(sourceUrl, env) {
  const endpoint = (env && env.DOUYIN_PARSE_ENDPOINT) || "";
  if (!endpoint) return null;

  let payload;
  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "content-type": "application/json", accept: "application/json" },
      body: JSON.stringify({ url: sourceUrl }),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    payload = await response.json();
  } catch (error) {
    throw new Error(`外部抖音解析服务调用失败：${error.message}`);
  }

  const data = payload && payload.data;
  if (!data) {
    throw new Error((payload && payload.message) || "外部抖音解析服务没有返回有效数据。");
  }

  return normalizeGatewayPayload(data, sourceUrl);
}

function normalizeGatewayPayload(data, sourceUrl) {
  if (data.video && data.metrics && data.transcript && data.analysis) {
    return data;
  }

  const counts = data.counts || data.statistics || {};
  const video = {
    id: String(data.id || data.aweme_id || ""),
    sourceUrl,
    resolvedUrl: data.resolvedUrl || data.resolved_url || sourceUrl,
    title: data.title || data.desc || "未获取到视频文案",
    author: {
      nickname: data.author || data.nickname || "未知作者",
      uniqueId: data.uniqueId || data.unique_id || "",
      avatar: data.avatar || "",
    },
    publishedAt: data.publishedAt || data.published_at || "",
    durationSeconds: data.durationSeconds || data.duration_seconds || null,
    cover: data.cover || "",
    playUrl: data.playUrl || data.play_url || "",
    counts: {
      play: toInt(counts.play || counts.play_count),
      like: toInt(counts.like || counts.digg_count),
      favorite: toInt(counts.favorite || counts.collect_count),
      comment: toInt(counts.comment || counts.comment_count),
      share: toInt(counts.share || counts.share_count),
    },
  };
  const transcript = data.transcript || {
    status: data.transcriptText || data.transcript_text ? "ready" : "not_configured",
    message: data.transcriptText || data.transcript_text ? "" : "语音转文字服务未配置。",
    text: data.transcriptText || data.transcript_text || "",
    segments: data.segments || [],
  };

  return {
    video,
    metrics: buildMetricsPayload(video),
    transcript,
    analysis: data.analysis || buildAnalysisPayload(video, transcript),
  };
}

function isDouyinUrl(url) {
  try {
    const host = new URL(url).hostname.toLowerCase();
    return host.includes("douyin.com") || host.includes("iesdouyin.com");
  } catch {
    return false;
  }
}

function extractVideoId(url) {
  const patterns = [
    /\/video\/(\d+)/,
    /\/note\/(\d+)/,
    /[?&](?:modal_id|aweme_id|item_id)=(\d+)/,
  ];

  for (const pattern of patterns) {
    const match = url.match(pattern);
    if (match) return match[1];
  }
  return "";
}

function extractJsonPayloads(pageHtml) {
  const payloads = [];
  const patterns = [
    /<script[^>]+id=["']RENDER_DATA["'][^>]*>([\s\S]*?)<\/script>/g,
    /<script[^>]+id=["']SIGI_STATE["'][^>]*>([\s\S]*?)<\/script>/g,
    /<script[^>]+id=["']__UNIVERSAL_DATA_FOR_REHYDRATION__["'][^>]*>([\s\S]*?)<\/script>/g,
  ];

  for (const pattern of patterns) {
    for (const match of pageHtml.matchAll(pattern)) {
      const parsed = loadJson(match[1]);
      if (parsed) payloads.push(parsed);
    }
  }

  const windowPatterns = [
    /window\.__INITIAL_STATE__\s*=\s*({[\s\S]*?})\s*<\/script>/,
    /window\.__UNIVERSAL_DATA_FOR_REHYDRATION__\s*=\s*({[\s\S]*?})\s*<\/script>/,
  ];

  for (const pattern of windowPatterns) {
    const match = pageHtml.match(pattern);
    const parsed = match ? loadJson(match[1]) : null;
    if (parsed) payloads.push(parsed);
  }

  return payloads;
}

function loadJson(raw) {
  if (!raw) return null;
  const decoded = decodeHtml(raw.trim());
  const candidates = [decoded, safeDecodeURIComponent(decoded)];

  for (const candidate of candidates) {
    try {
      return JSON.parse(candidate);
    } catch {
      continue;
    }
  }
  return null;
}

function decodeHtml(text) {
  return text
    .replace(/&quot;/g, '"')
    .replace(/&#34;/g, '"')
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">");
}

function safeDecodeURIComponent(text) {
  try {
    return decodeURIComponent(text);
  } catch {
    return text;
  }
}

function findAweme(payloads, videoId) {
  const candidates = [];
  for (const payload of payloads) {
    walkForAweme(payload, candidates);
  }

  if (videoId) {
    const exact = candidates.find((item) => String(item.aweme_id || item.id || "") === String(videoId));
    if (exact) return exact;
  }

  return candidates[0] || null;
}

async function fetchAwemeDetail(videoId, resolvedUrl) {
  if (!videoId) return null;

  const detailHeaders = {
    ...headers,
    accept: "application/json, text/plain, */*",
    referer: resolvedUrl,
  };
  const urls = [
    `https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=${videoId}`,
    `https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id=${videoId}&aid=6383&device_platform=webapp`,
  ];

  for (const url of urls) {
    try {
      const response = await fetch(url, { headers: detailHeaders });
      if (!response.ok) continue;
      const text = await response.text();
      if (!text) continue;
      const payload = JSON.parse(text);
      const aweme = extractAwemeFromDetailPayload(payload);
      if (aweme) return aweme;
    } catch {
      continue;
    }
  }

  return null;
}

function extractAwemeFromDetailPayload(payload) {
  if (!payload || typeof payload !== "object") return null;
  if (looksLikeAweme(payload.aweme_detail)) return payload.aweme_detail;

  const itemList = payload.item_list || payload.aweme_list || [];
  if (Array.isArray(itemList)) {
    for (const item of itemList) {
      if (looksLikeAweme(item)) return item;
    }
  }

  const candidates = [];
  walkForAweme(payload, candidates);
  return candidates[0] || null;
}

function walkForAweme(node, found) {
  if (!node || typeof node !== "object") return;
  if (looksLikeAweme(node)) {
    found.push(node);
  }

  if (Array.isArray(node)) {
    for (const item of node) walkForAweme(item, found);
    return;
  }

  for (const value of Object.values(node)) {
    walkForAweme(value, found);
  }
}

function looksLikeAweme(node) {
  return Boolean(
    node &&
      typeof node === "object" &&
      node.statistics &&
      typeof node.statistics === "object" &&
      (node.aweme_id || node.desc || node.video)
  );
}

function buildVideoPayload(aweme, sourceUrl, resolvedUrl, videoId) {
  const statistics = aweme.statistics || {};
  const author = aweme.author || {};
  const video = aweme.video || {};
  const durationMs = toInt(video.duration);

  return {
    id: String(aweme.aweme_id || videoId || ""),
    sourceUrl,
    resolvedUrl,
    title: aweme.desc || aweme.title || "未获取到视频文案",
    author: {
      nickname: author.nickname || "未知作者",
      uniqueId: author.unique_id || author.short_id || "",
      avatar: firstUrl(author.avatar_thumb && author.avatar_thumb.url_list),
    },
    publishedAt: formatDatetime(toInt(aweme.create_time)),
    durationSeconds: durationMs ? Math.round((durationMs / 1000) * 10) / 10 : null,
    cover:
      firstUrl(video.cover && video.cover.url_list) ||
      firstUrl(video.origin_cover && video.origin_cover.url_list) ||
      firstUrl(video.dynamic_cover && video.dynamic_cover.url_list),
    playUrl: extractPlayUrl(video),
    counts: {
      play: toInt(statistics.play_count),
      like: toInt(statistics.digg_count),
      favorite: toInt(statistics.collect_count),
      comment: toInt(statistics.comment_count),
      share: toInt(statistics.share_count),
    },
  };
}

function extractPlayUrl(video) {
  const direct = firstUrl(video.play_addr && video.play_addr.url_list);
  if (direct) return direct;

  for (const item of video.bit_rate || []) {
    const url = firstUrl(item.play_addr && item.play_addr.url_list);
    if (url) return url;
  }
  return "";
}

function firstUrl(urls) {
  if (Array.isArray(urls) && urls.length) return urls[0];
  if (typeof urls === "string") return urls;
  return "";
}

function toInt(value) {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) ? parsed : 0;
}

function formatDatetime(timestamp) {
  if (!timestamp) return "";
  const date = new Date(timestamp * 1000);
  if (Number.isNaN(date.getTime())) return "";
  const pad = (value) => String(value).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
}

function buildMetricsPayload(video) {
  const counts = video.counts || {};
  const play = counts.play || 0;
  return {
    likeRate: rate(counts.like, play),
    favoriteRate: rate(counts.favorite, play),
    commentRate: rate(counts.comment, play),
    shareRate: rate(counts.share, play),
    engagementRate: rate(
      (counts.like || 0) + (counts.favorite || 0) + (counts.comment || 0) + (counts.share || 0),
      play
    ),
  };
}

function rate(numerator, denominator) {
  if (!denominator) {
    return { value: null, label: "暂无播放量" };
  }
  const value = (numerator || 0) / denominator;
  return { value, label: `${(value * 100).toFixed(2)}%` };
}

async function buildTranscriptPayload(video, env) {
  const endpoint = (env && env.DOUYIN_TRANSCRIBE_ENDPOINT) || "";
  if (!endpoint) {
    return {
      status: "not_configured",
      message: "语音转文字服务未配置。配置 DOUYIN_TRANSCRIBE_ENDPOINT 后，可自动提取视频讲话文字。",
      text: "",
      segments: [],
    };
  }

  if (!video.playUrl) {
    return {
      status: "missing_video_url",
      message: "未获取到可用于转写的视频播放地址。",
      text: "",
      segments: [],
    };
  }

  try {
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        video_url: video.playUrl,
        source_url: video.sourceUrl,
        video_id: video.id,
        title: video.title,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const payload = await response.json();
    const text = payload.text || "";
    const segments = Array.isArray(payload.segments) ? payload.segments : [];
    return {
      status: text || segments.length ? "ready" : "empty",
      message: payload.message || "",
      text,
      segments,
    };
  } catch (error) {
    return {
      status: "failed",
      message: `语音转文字服务调用失败：${error.message}`,
      text: "",
      segments: [],
    };
  }
}

function buildAnalysisPayload(video, transcript) {
  const sourceText = transcript.text || video.title || "";
  return {
    summary: makeSummary(sourceText, transcript.status),
    keywords: extractKeywords(sourceText),
  };
}

function makeSummary(text, transcriptStatus) {
  const clean = String(text || "").replace(/\s+/g, " ").trim();
  if (!clean) return "暂未获取到可用于摘要的文字内容。";
  const prefix = transcriptStatus === "ready" ? "视频口播摘要" : "基于视频文案的摘要";
  return `${prefix}：${clean.slice(0, 140)}${clean.length > 140 ? "..." : ""}`;
}

function extractKeywords(text) {
  const stopwords = new Set(["一个", "这个", "那个", "我们", "你们", "他们", "可以", "就是", "今天", "视频", "抖音"]);
  const matches = String(text || "").match(/[A-Za-z0-9]{2,}|[\u4e00-\u9fff]{2,6}/g) || [];
  const counts = new Map();

  for (const word of matches) {
    if (stopwords.has(word)) continue;
    counts.set(word, (counts.get(word) || 0) + 1);
  }

  return Array.from(counts.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([word]) => word);
}
