# Job-Hunt Skill Suite

8 个互相调度的求职 skill，把 FindJobs-Agent 从「岗位数据工具」升级成「一次真实求职行动的指挥系统」——爬虫和投递看板负责数据，skill 负责决策与执行。

## 流水线

```
job-hunt-pilot（总控：每日闭环 / 每周复盘）
 ├─ job-market-scan    扫市场 → targets.md        ← scripts/sync_to_jobhunt.py 喂数据
 ├─ job-culture-vet    风气尽调（一票否决权，D 级剔除）
 ├─ job-resume-tailor  按 JD 定制简历 → resumes/
 ├─ job-github-polish  GitHub 门面（bio / README / 置顶 / demo GIF）
 ├─ job-pipeline       投递状态机 → applications.md ← scripts/sync_to_jobhunt.py 回写
 ├─ job-interview-drill 知识地图 + 项目深挖 + 模拟面试
 └─ job-offer-negotiate 总包拆解 + 多 offer 杠杆 → offers.md
```

## 数据分离设计（重要）

| 位置 | 内容 | 进 git？ |
| --- | --- | --- |
| 本仓库 `skills/` | 方法论（可公开，甚至是作品的一部分） | ✅ |
| 本仓库 `scripts/sync_to_jobhunt.py` | jobs.db ↔ 工作区的数据桥（幂等，只改锚点内区块） | ✅ |
| `~/project/AI/job-hunt/`（默认，`JOBHUNT_DIR` 可覆盖） | 候选人画像 PROFILE.md、targets.md、applications.md、resumes/、culture-vet/、interview-log.md、offers.md | ❌ 求职隐私，永不入库 |

## 快速开始

```bash
# 1. 初始化/更新求职工作区数据（先有 jobs.db：跑 pipeline.py）
python3 scripts/sync_to_jobhunt.py

# 2.（可选）让 AI 助手全局触发这些 skill：软链到你的 agent skills 目录
for d in skills/job-*; do ln -sfn "$(pwd)/$d" ~/.pi/agent/skills/"$(basename $d)"; done
```

然后对 AI 说触发词即可，例如「今日求职安排」（job-hunt-pilot）、「面我：字节 AI 应用」（job-interview-drill）、「尽调一下 MiniMax」（job-culture-vet）。

## 测试

```bash
python3 -m pytest tests/test_sync_jobhunt.py -q
```
