import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

import sync_to_jobhunt as sj  # noqa: E402
from storage import set_application_status, upsert_jobs  # noqa: E402


def _make_db(tmp_path):
    db = tmp_path / "jobs.db"
    upsert_jobs(db, [
        {
            "job_id": "a_1", "job_title": "AI应用工程师", "company_name": "某AI公司",
            "location": "上海", "apply_url": "https://example.com/1",
            "job_description": "Agent 方向",
        },
        {
            "job_id": "a_2", "job_title": "资深前端工程师", "company_name": "某大厂",
            "location": "杭州", "apply_url": "https://example.com/2",
            "job_description": "React 组件库",
        },
        {
            "job_id": "a_3", "job_title": "大模型应用开发", "company_name": "某AI公司",
            "location": "北京", "apply_url": "",
            "job_description": "RAG",
        },
    ])
    set_application_status(db, "a_1", "applied", "内推已投")
    set_application_status(db, "a_2", "interview", "下周三一面")
    return db


def test_is_agent_job_default_keywords():
    pat = sj.compile_keywords(sj.DEFAULT_KEYWORDS)
    assert sj.is_agent_job("AI应用工程师", "", pat)
    assert sj.is_agent_job("资深Agent平台工程师", "", pat)
    assert not sj.is_agent_job("资深前端工程师", "", pat)
    # deep only hits via description
    assert not sj.is_agent_job("Java后端", "", pat)
    assert sj.is_agent_job("Java后端", "负责大模型平台", pat)


def test_escape_md():
    assert sj.escape_md("a|b\nc") == "a\\|b c"
    assert sj.escape_md(None) == ""


def test_replace_anchor_preserves_manual_content():
    content = "# 手写标题\n\n我的笔记\n\n" + sj.TARGETS_START + "\n旧内容\n" + sj.TARGETS_END + "\n"
    out = sj.replace_anchor(content, sj.TARGETS_START, sj.TARGETS_END, "新内容")
    assert "我的笔记" in out and "旧内容" not in out and "新内容" in out
    # missing anchors -> appended
    out2 = sj.replace_anchor("只有手写", sj.TARGETS_START, sj.TARGETS_END, "块")
    assert sj.TARGETS_START in out2 and "块" in out2


def test_end_to_end_sync(tmp_path):
    db = _make_db(tmp_path)
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    pat = sj.compile_keywords(sj.DEFAULT_KEYWORDS)

    rows = [r for r in conn.execute(
        "SELECT company_name, job_title, location, apply_url, job_description FROM jobs"
    ) if sj.is_agent_job(r["job_title"], "", pat)]
    targets_md = sj.render_targets_table(sorted(rows, key=lambda r: r["job_title"]), deep=False, total=2)
    assert "AI应用工程师" in targets_md and "大模型应用开发" in targets_md
    assert "资深前端工程师" not in targets_md
    # unlinked job renders '-' instead of a broken link
    assert "| - |" in targets_md

    board = sj.fetch_board(conn)
    board_md = sj.render_board_table(board)
    assert "📨 applied" in board_md and "内推已投" in board_md
    assert "💻 interview" in board_md
    conn.close()
