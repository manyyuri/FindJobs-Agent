#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Upsert raw crawled jobs into jobs.db — no LLM, instant.

For when you only need the listing table (targets.md / 看板) and want to run
LLM enrichment later, incrementally, on the interesting subset only.

Usage:
    python3 scripts/ingest_raw.py crawled_jobs_raw.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from storage import JOB_COLUMNS, upsert_jobs  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="raw crawled JSON -> jobs.db")
    parser.add_argument("json_file", nargs="?", default="crawled_jobs_raw.json")
    parser.add_argument("--db", default=str(ROOT / "jobs.db"))
    args = parser.parse_args()

    src = Path(args.json_file)
    if not src.exists():
        print(f"❌ 文件不存在: {src}", file=sys.stderr)
        return 1

    raw = json.loads(src.read_text(encoding="utf-8"))
    seen: set[str] = set()
    rows = []
    for j in raw:
        row = {c: str(j.get(c, "") or "").strip() for c in JOB_COLUMNS}
        if row["job_id"] and row["job_id"] not in seen:
            seen.add(row["job_id"])
            rows.append(row)

    n = upsert_jobs(args.db, rows)
    print(f"✅ upsert {n} 条岗位 -> {args.db}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
