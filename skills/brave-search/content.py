#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx>=0.27.0",
# ]
# ///
"""
Extract content from a webpage using Firecrawl API.

Usage:
    content.py <url>
    content.py <url> --html          # Include HTML output
    content.py <url> --links         # Include links
    content.py <url> --screenshot    # Take screenshot (returns path)

Examples:
    content.py https://example.com/article
    content.py https://docs.firecrawl.dev --links
"""

import json
import os
import sys

import httpx


def scrape_url(url: str, formats: list[str] | None = None) -> dict:
    """Scrape a URL using Firecrawl API."""
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("Error: FIRECRAWL_API_KEY environment variable is required", file=sys.stderr)
        sys.exit(1)

    api_url = os.environ.get("FIRECRAWL_API_URL", "https://api.firecrawl.dev")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "url": url,
        "formats": formats or ["markdown"],
    }

    try:
        response = httpx.post(
            f"{api_url}/v1/scrape",
            headers=headers,
            json=payload,
            timeout=60.0,
        )
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        error_body = e.response.text
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get("error", error_body)
        except json.JSONDecodeError:
            error_msg = error_body
        print(f"HTTP {e.response.status_code}: {error_msg}", file=sys.stderr)
        sys.exit(1)
    except httpx.RequestError as e:
        print(f"Request error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if "--help" in sys.argv or "-h" in sys.argv else 1)

    url = sys.argv[1]
    
    # Parse format flags
    formats = ["markdown"]
    if "--html" in sys.argv:
        formats.append("html")
    if "--links" in sys.argv:
        formats.append("links")
    if "--screenshot" in sys.argv:
        formats.append("screenshot")

    result = scrape_url(url, formats)

    if not result.get("success"):
        print(f"Scrape failed: {result.get('error', 'Unknown error')}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data", {})
    metadata = data.get("metadata", {})

    # Print title if available
    title = metadata.get("title")
    if title:
        print(f"# {title}\n")

    # Print metadata summary
    if metadata.get("description"):
        print(f"> {metadata['description']}\n")
    
    print(f"Source: {metadata.get('sourceURL', url)}")
    if metadata.get("language"):
        print(f"Language: {metadata['language']}")
    print()

    # Print markdown content
    markdown = data.get("markdown")
    if markdown:
        print(markdown)
    
    # Print HTML if requested
    html = data.get("html")
    if html and "--html" in sys.argv:
        print("\n--- HTML ---\n")
        print(html[:5000] + ("..." if len(html) > 5000 else ""))

    # Print links if requested
    links = data.get("links")
    if links and "--links" in sys.argv:
        print("\n--- Links ---\n")
        for link in links[:50]:
            print(f"- {link}")
        if len(links) > 50:
            print(f"... and {len(links) - 50} more links")

    # Print screenshot path if requested
    screenshot = data.get("screenshot")
    if screenshot and "--screenshot" in sys.argv:
        print(f"\n--- Screenshot ---\n{screenshot}")


if __name__ == "__main__":
    main()
