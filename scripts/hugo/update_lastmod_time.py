"""Script to update the `lastmod` param for pages.

Iterates over content dir, compares each page's `lastmod` value with
git commit history, and updates if needed.
"""

from pathlib import Path
import subprocess
import re
import sys
from datetime import datetime, timezone
import logging

log = logging.getLogger(__name__)

## Path to content root
root: Path = Path(sys.argv[1] if len(sys.argv) > 1 else "content")

## Fallback date keys if lastmod frontmatter is missing
DATE_KEYS = ("lastmod", "date", "publishDate")


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


def format_utc(dt: datetime) -> str:
    """Convert a datetime to UTC timezone."""
    return (
        dt.astimezone(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def parse_iso(ts: str) -> datetime | None:
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        return dt.astimezone(timezone.utc)

    except ValueError:
        return None


def get_front_matter(text: str) -> tuple[str, str, str]:
    """Find Hugo frontmatter in file.

    Description:
        Each Hugo file has 'frontmatter' defined at the top, like:

        ```markdown
        ---
        title: "Page Title"
        draft: true
        weight: 0
        ---
        ```

        This function detects the start and end `---`.
    """
    if not text.startswith("---\n"):
        return None, None, None

    end = text.find("\n---\n", 4)

    if end == -1:
        return None, None, None

    fm = text[4:end]
    body = text[end + 5 :]

    return fm, body, text[: end + 5]


def get_fm_value(fm: str, key: str) -> str | None:
    """Find a specific value in frontmatter string."""
    m = re.search(rf"(?m)^{re.escape(key)}\s*:\s*([\"']?)(.+?)\1\s*$", fm)

    return m.group(2).strip() if m else None


def set_fm_value(fm: str, key: str, value: str) -> str:
    """Set value of a specific value in frontmatter string."""
    if re.search(rf"(?m)^{re.escape(key)}\s*:", fm):
        return re.sub(rf"(?m)^{re.escape(key)}\s*:\s*.*$", f'{key}: "{value}"', fm)

    return fm.rstrip() + f'\n{key}: "{value}"'


def current_page_time(fm: str) -> datetime | None:
    """Find a date key to use as a reference when determining if a file has changed."""

    ## Iterate over possible keys to find one that exists in frontmatter
    for key in DATE_KEYS:
        v = get_fm_value(fm, key)

        if v:
            dt = parse_iso(v)

            ## Return datetime from frontmatter
            if dt:
                return dt

    return None


def update_front_matter(text: str, ts: str) -> str:
    """Set/update lastModified frontmatter value for all content files.

    Description:
        Finds a date string in the file's frontmatter, checks git history to see
        if that file has changed, and bump the lastModified date in the frontmatter
        to match git history.
    """
    fm, body, _ = get_front_matter(text)

    if fm is None:
        return text

    new_dt = parse_iso(ts)

    if new_dt is None:
        return text

    existing_dt = current_page_time(fm)

    if existing_dt is not None and new_dt <= existing_dt:
        return text

    fm = set_fm_value(fm, "lastmod", format_utc(new_dt))

    return "---\n" + fm.strip() + "\n---\n" + body


def main():
    log.info(f"Scanning path for Markdown files: {root}")

    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".md", ".markdown"}:
            continue

        ts = git_last_commit_iso(path)
        log.debug(f"{path} timestamp: {ts}")

        if not ts:
            continue

        original = path.read_text(encoding="utf-8")
        updated = update_front_matter(original, ts)

        if updated != original:
            log.info(f"Updating lastmod value for file: {path}")
            path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    logging.basicConfig(
        level="INFO",
        format="%(asctime)s [%(levelname)s] :: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    main()
