"""Discover candidate match-page links from a public event listing page.

This intentionally discovers page links only. It does not bypass access controls,
extract protected media, or republish streams. Set FAWANEWS_URL to the exact
listing URL that the site operator permits you to access.
"""
import json
import os
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


def main():
    source_url = os.environ.get("FAWANEWS_URL", "http://fawanews.sc/").strip()
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
        # Match pages normally contain a team-v-team slug; skip news/article links.
        path_label = urlparse(href).path.rsplit("/", 1)[-1]
        stem = re.sub(r"\.html?$", "", path_label, flags=re.IGNORECASE)
        if not re.search(r"\s+vs?\s+", stem, flags=re.IGNORECASE):
            continue
        title = re.sub(r"\s+", " ", stem.replace("_", " ")).strip()
        candidates[href] = {"title": title, "category_hint": label}

    result = {
        "source_url": source_url,
        "http_status": response.status_code,
        "page_title": soup.title.get_text(" ", strip=True) if soup.title else "",
        "candidate_count": len(candidates),
        "candidates": [
            {"title": item["title"], "category_hint": item["category_hint"], "url": url}
            for url, item in sorted(candidates.items())
        ],
        "note": "Candidate links only; verify titles and permissions before use.",
    }
    Path("discovered_matches.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
