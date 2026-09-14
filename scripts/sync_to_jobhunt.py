#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bridge between jobs.db and the job-hunt workspace markdown files.

Two exports, both rerun-safe — only the ``<!-- FINDJOBS:* -->`` anchored
block inside each file is rewritten; anything hand-written outside the
anchors survives repeated runs:

1. AI/Agent roles from the jobs table -> <jobhunt>/targets.md
2. the application board             -> <jobhunt>/applications.md

Usage:
    python3 scripts/sync_to_jobhunt.py                 # both exports
    python3 scripts/sync_to_jobhunt.py --deep          # also scan descriptions
    python3 scripts/sync_to_jobhunt.py --keywords 智能体 RAG
    python3 scripts/sync_to_jobhunt.py --board-only    # skip targets export
"""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TARGETS_START = "<!-- FINDJOBS:TARGETS:START -->"
TARGETS_END = "<!-- FINDJOBS:TARGETS:END -->"
BOARD_START = "<!-- FINDJOBS:APPLICATIONS:START -->"
BOARD_END = "<!-- FINDJOBS:APPLICATIONS:END -->"

# Title keywords that mark an engineering role worth tracking for an
# agent/AI-application job hunt. Algorithm-research roles are intentionally
# broad-matched too — the human decides in the manual section of targets.md.
DEFAULT_KEYWORDS = [
    "AI应用", "AI 应用", "Agent", "智能体", "LLM", "大模型", "AIGC",
    "AI工程师", "AI 工程师", "AI前端", "AI 前端", "AI全栈", "AI 全栈",
    "NLP应用", "NLP 应用", "AI Infra", "Copilot", "RAG", "AI平台",
]

STATUS_EMOJI = {
    "bookmarked": "🎯 bookmarked",
    "applied": "📨 applied",
    "replied": "📞 replied",
    "interview": "💻 interview",
    "offer": "🏆 offer",
    "rejected": "❌ rejected",
}


def default_jobhunt_dir() -> Path:
    env = os.environ.get("JOBHUNT_DIR")
    if env:
        return Path(env).expanduser()
    return Path.home() / "project" / "AI" / "job-hunt"


def compile_keywords(keywords: list[str]) -> re.Pattern[str]:
    return re.compile("|".join(re.escape(k) for k in keywords), re.IGNORECASE)


def is_agent_job(title: str, description: str = "", pattern: re.Pattern[str] | None = None) -> bool:
    pattern = pattern or compile_keywords(DEFAULT_KEYWORDS)
    return bool(pattern.search(title or "") or pattern.search(description or ""))


def escape_md(text: object) -> str:
    return str(text or "").replace("|", "\\|").replace("\n", " ").strip()


def render_targets_table(rows: list[sqlite3.Row], deep: bool, total: int) -> str:
    lines = [
        f"> 自动扫描于 {date.today().isoformat()}：共 {total} 条命中"
        f"（{'标题+描述' if deep else '标题'}关键词过滤，本表最多展示前 {len(rows)} 条）。",
        "> 薪资带宽 / 内推渠道 / 优先级在下方手写区补充；每家新公司记得跑风气尽调。",
        "",
        "| 公司 | 岗位 | base | 渠道 | 优先级 | 链接 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        url = r["apply_url"] or ""
        link = f"[JD]({url})" if url else "-"
        lines.append(
            f"| {escape_md(r['company_name'])} | {escape_md(r['job_title'])} "
            f"| {escape_md(r['location'])} | 官网 | 待尽调 | {link} |"
        )
    return "\n".join(lines)


def fetch_board(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return conn.execute(
        "SELECT a.job_id, a.status, a.note, a.updated_at,"
        " j.company_name, j.job_title, j.location, j.apply_url"
        " FROM applications a LEFT JOIN jobs j ON j.job_id = a.job_id"
        " ORDER BY a.updated_at DESC"
    ).fetchall()


def render_board_table(rows: list[sqlite3.Row]) -> str:
    lines = [
        f"> 看板同步于 {date.today().isoformat()}：共 {len(rows)} 条（来源 jobs.db applications 表）。",
        "> 手写跟进记录写在锚点区块外，不会被覆盖。",
        "",
        "| 公司 | 岗位 | base | 状态 | 更新时间 | 备注 | 链接 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for r in rows:
        status = STATUS_EMOJI.get(r["status"], r["status"] or "-")
        updated = (r["updated_at"] or "")[:10]
        url = r["apply_url"] or ""
        link = f"[JD]({url})" if url else "-"
        lines.append(
            f"| {escape_md(r['company_name']) or '-'} | {escape_md(r['job_title']) or '-'} "
            f"| {escape_md(r['location'])} | {status} | {updated} "
            f"| {escape_md(r['note'])} | {link} |"
        )
    return "\n".join(lines)


def replace_anchor(content: str, start: str, end: str, block: str) -> str:
    """Rewrite the region between the anchors; append if anchors are missing."""
    if start in content and end in content:
        i = content.index(start) + len(start)
        j = content.index(end)
        return content[:i] + "\n" + block + "\n" + content[j:]
    return content.rstrip("\n") + f"\n\n{start}\n{block}\n{end}\n"


def ensure_file(path: Path, title: str, start: str, end: str) -> str:
    if path.exists():
        return path.read_text(encoding="utf-8")
    return f"# {title}\n\n> 手写内容放在锚点区块外；锚点内的自动表格由 `FindJobs-Agent/scripts/sync_to_jobhunt.py` 生成。\n\n{start}\n\n{end}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="jobs.db -> job-hunt workspace sync")
    parser.add_argument("--db", default=str(ROOT / "jobs.db"), help="jobs.db 路径")
    parser.add_argument("--jobhunt", default=str(default_jobhunt_dir()), help="求职工作区目录")
    parser.add_argument("--keywords", nargs="*", default=None, help="覆盖默认关键词")
    parser.add_argument("--all", action="store_true", help="不过滤，导出全部岗位")
    parser.add_argument("--deep", action="store_true", help="关键词同时匹配岗位描述")
    parser.add_argument("--limit", type=int, default=200, help="targets 表最大行数")
    parser.add_argument("--targets-only", action="store_true")
    parser.add_argument("--board-only", action="store_true")
    args = parser.parse_args()

    db = Path(args.db).expanduser()
    if not db.exists():
        print(f"❌ 数据库不存在: {db}（先跑 pipeline.py 生成 jobs.db）", file=sys.stderr)
        return 1

    jobhunt = Path(args.jobhunt).expanduser()
    jobhunt.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row

    pattern = compile_keywords(args.keywords or DEFAULT_KEYWORDS)

    if not args.board_only:
        all_rows = conn.execute(
            "SELECT company_name, job_title, location, apply_url, job_description FROM jobs"
        ).fetchall()
        matched_all = [
            r for r in all_rows
            if is_agent_job(r["job_title"], r["job_description"] if args.deep else "", pattern)
        ]
        matched_all.sort(key=lambda r: (r["company_name"] or "", r["job_title"] or ""))
        total, matched = len(matched_all), matched_all[: args.limit]
        path = jobhunt / "targets.md"
        content = ensure_file(path, "目标公司清单", TARGETS_START, TARGETS_END)
        content = replace_anchor(
            content, TARGETS_START, TARGETS_END,
            render_targets_table(matched, args.deep, total),
        )
        path.write_text(content, encoding="utf-8")
        print(f"✅ targets.md: {len(matched)} 条 AI/Agent 岗位（共命中 {total} 条）")

    if not args.targets_only:
        board = fetch_board(conn)
        path = jobhunt / "applications.md"
        content = ensure_file(path, "投递管道", BOARD_START, BOARD_END)
        content = replace_anchor(
            content, BOARD_START, BOARD_END, render_board_table(board)
        )
        path.write_text(content, encoding="utf-8")
        print(f"✅ applications.md: {len(board)} 条看板记录")

    conn.close()
    print(f"📁 工作区: {jobhunt}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
