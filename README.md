# LIVE-SPORTS

Automatic public match-page discovery and M3U generation for **authorized streams**.

The workflow runs every 30 minutes or manually from **Actions → Update live sports playlist → Run workflow**.

- `generate.py` extracts match titles and page links from the source homepage.
- `matches.json` is the discovered match metadata.
- `streams.json` maps match-page URLs to actual HLS/DASH URLs you have permission to distribute.
- `live_sports.m3u` includes only mapped, authorized streams. HTML page links are not playable video URLs.

Example of `streams.json` format (illustrative only, not a working stream):
```json
{
  "https://example.com/Team-A-vs-Team-B.html": "https://streams.example.com/authorized/live.m3u8"
}
```

Playlist URL: https://raw.githubusercontent.com/ayaannm2007/LIVE-SPORTS/main/live_sports.m3u

**Note:** Source site accessibility and HTML structure are not yet verified. If the site blocks GitHub Actions, or uses JavaScript-only listings, the scraper will need adjustment. The workflow fails without overwriting the existing playlist if the source fetch fails. No DRM keys or access tokens should be committed.
