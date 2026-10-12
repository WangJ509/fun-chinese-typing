#!/usr/bin/env python3
"""Embed the poems and prose of texts.tsv in index.html.

    python3 make_data.py
"""

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    rows = []
    counters = defaultdict(int)
    with open(ROOT / "texts.tsv", encoding="utf-8") as f:
        for line in f:
            if not line.strip() or line.startswith("#"):
                continue
            kind, era, title, author, text = line.rstrip("\n").split("\t")
            counters[kind] += 1
            rows.append([f"{kind}-{counters[kind]:03d}", kind, era, title, author, text])

    html_path = ROOT / "index.html"
    lines = html_path.read_text(encoding="utf-8").split("\n")
    prefix = "const TEXTS = "
    index = next(i for i, l in enumerate(lines) if l.startswith(prefix))
    lines[index] = prefix + json.dumps(rows, ensure_ascii=False, separators=(",", ":")) + ";"
    html_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {len(rows)} passages")


if __name__ == "__main__":
    main()
