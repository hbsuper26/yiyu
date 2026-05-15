function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      "content-type": "application/json; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

async function ensureTable(db) {
  await db
    .prepare(
      "CREATE TABLE IF NOT EXISTS article_views (article_id INTEGER PRIMARY KEY, views INTEGER NOT NULL DEFAULT 0, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
    )
    .run();
}

export async function onRequestPost({ env, params, request }) {
  if (!env.ARTICLE_VIEWS) {
    return json({ error: "ARTICLE_VIEWS D1 binding is not configured" }, 500);
  }

  const articleId = Number.parseInt(params.id, 10);
  if (!Number.isInteger(articleId) || articleId <= 0) {
    return json({ error: "Invalid article id" }, 400);
  }

  let baseViews = 0;
  try {
    const body = await request.json();
    baseViews = Number.parseInt(body?.baseViews, 10);
    if (!Number.isInteger(baseViews) || baseViews < 0) {
      baseViews = 0;
    }
  } catch {
    baseViews = 0;
  }

  await ensureTable(env.ARTICLE_VIEWS);

  await env.ARTICLE_VIEWS.prepare(
    "INSERT INTO article_views (article_id, views, updated_at) VALUES (?, ? + 1, CURRENT_TIMESTAMP) ON CONFLICT(article_id) DO UPDATE SET views = article_views.views + 1, updated_at = CURRENT_TIMESTAMP"
  )
    .bind(articleId, baseViews)
    .run();

  const row = await env.ARTICLE_VIEWS.prepare(
    "SELECT views FROM article_views WHERE article_id = ?"
  )
    .bind(articleId)
    .first();

  return json({ articleId, views: row?.views ?? baseViews + 1 });
}
