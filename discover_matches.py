"""Discover candidate match-page links from a public event listing page.

This intentionally discovers page links only. It does not bypass access controls,
extract protected media, or republish streams. Set FAWANEWS_URL to the exact
listing URL that the site operator permits you to access.
"""
import json
import os
import re
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def main():
    source_url = os.environ.get("FAWANEWS_URL", "").strip()
    if not source_url:
        raise SystemExit("Set FAWANEWS_URL to the permitted live-match listing URL.")
    parsed = urlparse(source_url)
    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise SystemExit("FAWANEWS_URL must be a valid http(s) URL.")

    response = requests.get(
        source_url,
        headers={"User-Agent": "LIVE-SPORTS match-list checker/1.0"},
        timeout=20,
    )
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    candidates = {}
    for anchor in soup.find_all("a", href=True):
        href = urljoin(source_url, anchor["href"].strip())
        label = " ".join(anchor.get_text(" ", strip=True).split())
        if not label or urlparse(href).netloc != parsed.netloc:
            continue
        # Keep likely event links; review results before enabling automation.
        hint = (label + " " + urlparse(href).path).lower()
        if re.search(r"match|live|cricket|football|vs|v-", hint):
            candidates[href] = label

    result = {
        "source_url": source_url,
        "http_status": response.status_code,
        "page_title": soup.title.get_text(" ", strip=True) if soup.title else "",
        "candidate_count": len(candidates),
        "candidates": [
            {"title": title, "url": url}
            for url, title in sorted(candidates.items())
        ],
        "note": "Candidate links only; verify titles and permissions before use.",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
