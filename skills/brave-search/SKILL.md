---
name: brave-search
description: Web search via Brave Search API and content extraction via Firecrawl. Use for searching documentation, facts, or extracting clean content from any URL.
---

# Brave Search + Firecrawl

Web search using Brave Search API and content extraction using Firecrawl API. No browser required.

## Requirements

- [uv](https://docs.astral.sh/uv/) (dependencies managed automatically via inline metadata)
- `BRAVE_API_KEY` environment variable (for search)
- `FIRECRAWL_API_KEY` environment variable (for content extraction)

## Search

```bash
{baseDir}/search.py "query"                    # Basic search (5 results)
{baseDir}/search.py "query" -n 10              # More results
{baseDir}/search.py "query" --content          # Include page content as markdown
{baseDir}/search.py "query" -n 3 --content     # Combined
```

## Extract Page Content (Firecrawl)

```bash
{baseDir}/content.py https://example.com/article              # Markdown output
{baseDir}/content.py https://example.com/article --links      # Include extracted links
{baseDir}/content.py https://example.com/article --html       # Include raw HTML
{baseDir}/content.py https://example.com/article --screenshot # Get screenshot URL
```

Firecrawl handles:
- JavaScript-rendered pages
- Anti-bot bypassing
- Clean markdown conversion
- Metadata extraction (title, description, language)

## Output Format

### Search
```
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Snippet: Description from search results
Content: (if --content flag used)
  Markdown content extracted from the page...

--- Result 2 ---
...
```

### Content Extraction
```
# Page Title

> Page description

Source: https://example.com/article
Language: en

[Clean markdown content...]
```

## When to Use

- **Search**: Finding documentation, API references, facts, current information
- **Content extraction**: Getting clean, readable content from any URL
- JavaScript-heavy sites that need rendering
- Sites with anti-bot protection
