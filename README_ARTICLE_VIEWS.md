# Article View Counter

This site uses Cloudflare Pages Functions plus D1 to keep shared article view counts.

## Cloudflare setup

Create the D1 database:

```bash
npx wrangler d1 create yiyu-article-views
```

Copy `wrangler.example.jsonc` to `wrangler.jsonc`, then replace `database_id` with the id returned by Cloudflare.

Initialize the table:

```bash
npx wrangler d1 execute yiyu-article-views --remote --file=schema_article_views.sql
```

In Cloudflare Pages, bind the D1 database to the project with this binding name:

```text
ARTICLE_VIEWS
```

## Runtime behavior

- Opening `/article/<id>` calls `POST /api/article-view/<id>`.
- The first click uses the generated article `views` value as the base, then adds 1.
- Later clicks from any visitor increment the shared D1 count.
- `/articles` calls `GET /api/article-views?ids=...` and displays the shared count when it is higher than the generated base number.
