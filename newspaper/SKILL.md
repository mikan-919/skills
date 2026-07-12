---
name: newspaper
description: Build a daily Markdown "newspaper" from the user's news sources — RSS/Atom feeds AND non-RSS HTML news index pages (e.g. Anthropic, OpenAI). Fetch each source, filter against the user's taste (taste.json), summarize each kept article in Japanese without embellishment, and write newspaper/YYYY-MM-DD.md grouped by category. Use when the user says "build today's newspaper", "新聞を作って", "collect/summarize my news", "newspaper build", or "reject this article / newspaper reject <url>".
---

# Newspaper

Collect today's news from the user's sources, keep only what matches their taste, and lay it out as a dated Markdown newspaper. **You are the filter and the summarizer** — there is no separate LLM service; you fetch, judge, and write directly.

Three values from the concept govern every decision:
- **Sources stay visible** — every article shows which source feed it came from. Never hide the origin.
- **No embellishment** — summarize facts only. No narrative framing, no "this is exciting", no added context the article didn't state.
- **No hidden filtering** — always report what was rejected and why. The user must be able to see what you dropped.

## Files (in the working directory, or a path the user names)

- `source.yaml` — the news sources, each a URL + category, with an optional `type`. Required. See [source.example.yaml](source.example.yaml) for a ready-to-copy starter.
- `taste.json` — articles/sources the user has rejected, with reasons. Optional (absent = nothing rejected).
- `newspaper/YYYY-MM-DD.md` — the output.

`source.yaml`:
```yaml
- url: https://arxiv.org/rss/cs.AI      # RSS/Atom feed
  category: 論文
- url: https://www.anthropic.com/news   # non-RSS HTML index page
  category: LLM Provider
  type: page                            # optional hint; omit to auto-detect
```

`taste.json`:
```json
[
  { "url": "https://example.com/old-article", "reason": "技術スタックが古い", "category": "技術記事" }
]
```

## Build workflow ("newspaper build")

1. **Read** `source.yaml` and `taste.json`. If `source.yaml` is missing, tell the user to create it (show the format above) and stop.

2. **Fetch each source** with WebFetch. Pull only *recent* items — published today or yesterday; if an item has no date, include it.
   - **Feed** (`type: feed` or auto): ask WebFetch to list recent items as title, link, published date, and the feed's own description/summary.
   - **Page** (`type: page`, or auto-detected as an HTML index — e.g. Anthropic/OpenAI news): ask WebFetch to list the recent article headlines and their links from the index. Cross-host redirect returned instead of followed → call WebFetch again with that URL.
   - A source that fails to load: warn and skip it. Only error out if *every* source failed.

3. **Filter.** Drop an article if its URL matches any `taste.json` entry, or if it clearly conflicts with the rejection reasons there (same stale tech, same disliked topic). When in doubt, keep it — under-filtering is recoverable, silently dropping signal is not. Track every kept and every rejected article with a one-line reason.

4. **Fetch content** of each kept article with WebFetch (prompt for the main body text). On failure, fall back to the feed's own summary — one article's failure must not stop the build.

5. **Summarize** each kept article in Japanese, 2–3 sentences, facts only. No narrative, no commentary, no "注目", no invented context.

6. **Write** `newspaper/YYYY-MM-DD.md` (use the user's `--date` if given, else today). Group by category in `source.yaml` order:
   ```markdown
   # 2026-06-26

   ## 論文

   ### <タイトル>
   [LINK](<url>) · source: <source feed url or name>

   <2–3文の日本語要約>
   ```

7. **Report** to the user: output path, `N kept, M rejected`, and the rejected list with reasons (honoring "no hidden filtering"). If you create the file for a date that already exists, mention you overwrote it.

## Reject workflow ("newspaper reject <url> [reason]")

Append `{ "url": <url>, "reason": <reason or "">, "category": "user" }` to `taste.json` (create the file as a JSON array if absent), then confirm. The next build excludes that URL and uses the reason as filtering signal.

## When NOT to use

- The user just wants to read one specific article → fetch it directly, no newspaper.
- No `source.yaml` and the user hasn't described their sources → ask what feeds/pages they follow first.
- The user wants the old Go CLI behavior (providers, API keys, Ollama) → that implementation is superseded by this skill; Claude is the model now.
