"""Generate an M3U playlist from operator-provided, authorized streams."""
import json
from datetime import datetime, timezone
from pathlib import Path

def main():
    entries = json.loads(Path("streams.json").read_text(encoding="utf-8"))
    if not isinstance(entries, dict):
        raise ValueError("streams.json must be a JSON object")
    playlist = ["#EXTM3U"]
    matches = []
    for title, item in sorted(entries.items()):
        stream = item.get("url", "") if isinstance(item, dict) else item
        referer = item.get("referer", "") if isinstance(item, dict) else ""
        if not isinstance(stream, str) or not stream.startswith(("https://", "http://")):
            continue
        if referer and (not isinstance(referer, str) or not referer.startswith(("https://", "http://"))):
            continue
        matches.append({"title": title, "stream_configured": True})
        playlist.append('#EXTINF:-1 group-title="Live Sports",' + title.replace(",", " "))
        # IPTV pipe-header syntax is player-specific; not part of standard M3U.
        playlist.append(stream + ("|Referer=" + referer if referer else ""))
    Path("live_sports.m3u").write_text("\n".join(playlist) + "\n", encoding="utf-8")
    Path("matches.json").write_text(
        json.dumps({"updated_at": datetime.now(timezone.utc).isoformat(), "matches": matches}, indent=2) + "\n",
        encoding="utf-8",
    )
    print("Configured streams:", len(matches))

if __name__ == "__main__":
    main()
