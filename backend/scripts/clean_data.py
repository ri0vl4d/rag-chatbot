"""Clean noisy markdown files in backend/data/ in-place.

Removes artifacts left over from PDF/PPTX-to-markdown conversion:
  - image placeholders like ![alt](Picture14.jpg)
  - HTML comments like <!-- Slide number: 3 -->
  - stray "Download Here" fragments
  - runs of 3+ blank lines collapsed to 2
  - trims trailing whitespace on every line

Also deletes any zero-byte .md files (they contribute nothing and confuse the loader).

Usage (from backend/):
    python scripts/clean_data.py
    python scripts/clean_data.py --dry-run
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# Order matters — image regex first, then comments, then whitespace normalization.
PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(r"!\[[^\]]*\]\([^)]*\)"), ""),           # ![alt](file.jpg)
    (re.compile(r"<!--\s*Slide number:\s*\d+\s*-->"), ""),  # slide markers
    (re.compile(r"<!--[\s\S]*?-->"), ""),                 # any other HTML comments
    (re.compile(r"^\s*Download Here\s*$", re.MULTILINE), ""),
    (re.compile(r"[ \t]+$", re.MULTILINE), ""),           # trailing whitespace
    (re.compile(r"\n{3,}"), "\n\n"),                       # collapse blank lines
]


def clean_text(text: str) -> str:
    for pat, repl in PATTERNS:
        text = pat.sub(repl, text)
    return text.strip() + "\n"


def process_file(path: Path, dry_run: bool) -> tuple[str, int, int]:
    """Returns (action, before_bytes, after_bytes)."""
    raw = path.read_text(encoding="utf-8", errors="ignore")
    before = len(raw)

    if before == 0:
        if not dry_run:
            path.unlink()
        return ("deleted (empty)", 0, 0)

    cleaned = clean_text(raw)
    after = len(cleaned)

    if cleaned == raw:
        return ("unchanged", before, after)

    if not dry_run:
        path.write_text(cleaned, encoding="utf-8")
    return ("cleaned", before, after)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    args = parser.parse_args()

    if not DATA_DIR.exists():
        print(f"ERROR: {DATA_DIR} does not exist", file=sys.stderr)
        return 1

    files = sorted(DATA_DIR.rglob("*.md"))
    if not files:
        print("No .md files found in data/.")
        return 0

    print(f"{'DRY RUN — ' if args.dry_run else ''}Processing {len(files)} file(s):\n")
    total_before = total_after = 0

    for f in files:
        action, before, after = process_file(f, args.dry_run)
        delta = after - before
        sign = "+" if delta >= 0 else ""
        print(f"  {action:20s}  {before:>7,} -> {after:>7,} B  ({sign}{delta:,})  {f.name}")
        total_before += before
        total_after += after

    print(f"\nTotal: {total_before:,} -> {total_after:,} bytes "
          f"({total_after - total_before:+,}, {(1 - total_after / max(total_before, 1)) * 100:.1f}% smaller)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
