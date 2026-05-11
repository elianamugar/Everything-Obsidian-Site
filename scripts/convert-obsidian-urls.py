from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote
import re

CONTENT = Path("content")

OBSIDIAN_URL_RE = re.compile(r"obsidian://open\?[^)\s>\"]+")

def quartz_path(file_value: str) -> str:
    file_path = unquote(file_value)

    # Remove .md if present
    if file_path.endswith(".md"):
        file_path = file_path[:-3]

    # Quartz URLs are usually lowercase-ish slugs preserving folders
    return "/" + file_path.replace(" ", "-")

for path in CONTENT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")

    def replace(match):
        url = match.group(0)
        parsed = urlparse(url)
        params = parse_qs(parsed.query)

        file_values = params.get("file")
        if not file_values:
            return url

        return quartz_path(file_values[0])

    new_text = OBSIDIAN_URL_RE.sub(replace, text)

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"updated {path}")