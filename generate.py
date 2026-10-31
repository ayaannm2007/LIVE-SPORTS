"""Build an M3U from operator-provided authorized streams and match metadata."""
import json
from pathlib import Path
from datetime import datetime, timezone

def main():
    entries = json.loads(Path("streams.json").read_text(encoding="utf-8"))
    if not isinstance(entries, dict):
        raise ValueError("streams.json must be a JSON object")
    playlist = ["#EXTM3U"]
    matches = []
    for title, stream in sorted(entries.items()):
        if not isinstance(stream, str) or not stream.startswith(("https://", "http://")):
            continue
        matches.append({"title": title, "stream_configured": True})
        playlist.append('#EXTINF:-1 group-title="Live Sports",' + title.replace(",", " "))
        playlist.append(stream)
    Path("live_sports.m3u").write_text("\n".join(playlist) + "\n", encoding="utf-8")
    Path("matches.json").write_text(json.dumps({"updated_at": datetime.now(timezone.utc).isoformat(), "matches": matches}, indent=2) + "\n", encoding="utf-8")
    print("Configured streams:", len(matches))

if __name__ == "__main__":
    main()
