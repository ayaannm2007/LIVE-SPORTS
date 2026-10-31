# LIVE-SPORTS

GitHub Actions playlist generator for operator-provided authorized streams.

## Current behavior
- `streams.json` contains a mapping of titles to stream URLs, optionally with a `referer` property.
- `generate.py` creates `live_sports.m3u` and `matches.json` from those configured entries.
- `.github/workflows/update-playlist.yml` is scheduled every 30 minutes and supports manual dispatch.
- The playlist uses `|Referer=...` syntax for configured referers; this is player-specific, not universal M3U syntax.
- The sample HLS URL was supplied by the operator. Its current availability and associated match are **not verified**.

## Not implemented
This project does **not yet** discover FawaNews matches, open match pages, click video players, or extract streams automatically. These features require site access, testing, and an authorized source. No GitHub Actions run has yet been confirmed.

## Playlist
https://raw.githubusercontent.com/ayaannm2007/LIVE-SPORTS/main/live_sports.m3u

## Test
Open GitHub → Actions → Update live sports playlist → Run workflow on `main`. Check logs and generated files. Do not commit credentials, session cookies, or DRM keys.
