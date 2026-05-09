from pathlib import Path
import re

CONTENT = Path("content")
DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\s+\d{2}:\d{2}\b")

for path in CONTENT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")

    match = DATE_RE.search(text)
    if not match:
        print(f"no date found: {path}")
        continue

    created = match.group(1)

    if text.startswith("---"):
        end = text.find("---", 3)
        frontmatter = text[3:end].strip()

        if re.search(r"^created:", frontmatter, re.MULTILINE):
            print(f"already has created: {path}")
            continue

        new_text = text[:end] + f"created: {created}\n" + text[end:]
    else:
        new_text = f"---\ncreated: {created}\n---\n\n{text}"

    path.write_text(new_text, encoding="utf-8")
    print(f"added created {created}: {path}")