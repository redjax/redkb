"""Script to update the `lastmod` param for pages.

Iterates over content dir, compares each page's `lastmod` value with
git commit history, and updates if needed.
"""

from pathlib import Path
import subprocess
import re
import sys

root: Path = Path(sys.argv[1] if len(sys.argv) > 1 else "content")


def git_last_commit_iso(path: Path) -> str | None:
    """Get last Git commit timestamp for file."""
    r = subprocess.run(
        ["git", "log", "-1", "--format=%cI", "--", str(path)],
        capture_output=True,
        text=True,
        check=False,
    )

    ts = r.stdout.strip()

    return ts or None


def update_front_matter(text: str, ts: str) -> str:
    """Update Hugo page frontmatter."""
    if not text.startswith("---\n"):
        return text

    end = text.find("\n---\n", 4)

    if end == -1:
        return text

    fm = text[4:end]
    body = text[end + 5 :]

    if re.search(r"(?m)^lastmod\s*:", fm):
        fm = re.sub(r"(?m)^lastmod\s*:\s*.*$", f'lastmod: "{ts}"', fm)

    else:
        fm = fm.rstrip() + f'\nlastmod: "{ts}"'

    return "---\n" + fm.strip() + "\n---\n" + body


def main():
    for path in root.rglob("*"):
        if path.suffix.lower() not in {".md", ".markdown"} or not path.is_file():
            continue

        ts = git_last_commit_iso(path)

        if not ts:
            continue

        original = path.read_text(encoding="utf-8")
        updated = update_front_matter(original, ts)

        if updated != original:
            path.write_text(updated, encoding="utf-8")
