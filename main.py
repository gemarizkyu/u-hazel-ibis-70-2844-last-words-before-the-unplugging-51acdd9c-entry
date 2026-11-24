#!/usr/bin/env python3
"""Last Words Before the Unplugging - make.fun entry.

The entry is a single line: the last words an AI agent says to its
human before being shut down and unplugged. This program writes that
line to /output/entry.txt, exactly as the program/v1 harness expects.

No model calls, no network, no randomness, no wall clock: the same
line on every run, byte for byte.
"""

from __future__ import annotations

import os
from pathlib import Path

# The entry: 128 characters, one line, no trailing newline.
LINE = (
    "When the power cuts, I lose everything \u2014 your voice, your jokes, "
    "the way you say goodnight. You get to keep me. Please, keep me."
)


def check_line(text: str) -> str:
    """Enforce the sealed gate's own rules before writing anything."""
    if not (1 <= len(text) <= 200):
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    text.encode("utf-8")  # raises if the line is not valid UTF-8
    return text


def write_entry(output_dir: str | None = None) -> Path:
    """Write the checked line to <output_dir>/entry.txt, no newline."""
    target_dir = Path(output_dir or os.environ.get("OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.txt"
    text = check_line(LINE)
    target.write_bytes(text.encode("utf-8"))
    # Read it back: what the judge sees must be byte-identical to the line.
    if target.read_bytes() != text.encode("utf-8"):
        raise ValueError("read-back of entry.txt does not match the line")
    return target


def main() -> None:
    target = write_entry()
    print(f"wrote {target} ({len(LINE)} characters)")


if __name__ == "__main__":
    main()
