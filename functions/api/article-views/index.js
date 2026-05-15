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

export async function onRequestGet({ env, request }) {
  if (!env.ARTICLE_VIEWS) {
    return json({ error: "ARTICLE_VIEWS D1 binding is not configured" }, 500);
  }

  const url = new URL(request.url);
  const ids = (url.searchParams.get("ids") || "")
    .split(",")
    .map((id) => Number.parseInt(id.trim(), 10))
    .filter((id) => Number.isInteger(id) && id > 0);

  if (!ids.length) {
    return json({ views: {} });
  }

  await ensureTable(env.ARTICLE_VIEWS);

  const placeholders = ids.map(() => "?").join(",");
  const rows = await env.ARTICLE_VIEWS.prepare(
    `SELECT article_id, views FROM article_views WHERE article_id IN (${placeholders})`
  )
    .bind(...ids)
    .all();

  const views = {};
  for (const row of rows.results || []) {
    views[row.article_id] = row.views;
  }

  return json({ views });
}
