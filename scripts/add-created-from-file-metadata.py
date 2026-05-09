from pathlib import Path
from datetime import datetime
import re
import os

CONTENT = Path("content")

def get_created_date(path: Path) -> str:
    stat = path.stat()

    # macOS supports st_birthtime = file creation time
    if hasattr(stat, "st_birthtime"):
        timestamp = stat.st_birthtime
    else:
        # fallback for systems without creation time
        timestamp = stat.st_mtime

    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

for path in CONTENT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")

    created = get_created_date(path)

    if text.startswith("---"):
        end = text.find("---", 3)
        frontmatter = text[3:end]

        if re.search(r"^created:", frontmatter, re.MULTILINE):
            print(f"already has created: {path}")
            continue

        new_text = text[:end] + f"created: {created}\n" + text[end:]
    else:
        new_text = f"---\ncreated: {created}\n---\n\n{text}"

    path.write_text(new_text, encoding="utf-8")
    print(f"added created {created}: {path}")