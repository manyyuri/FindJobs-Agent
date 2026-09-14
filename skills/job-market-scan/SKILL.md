---
name: job-market-scan
description: 扫描 AI Agent / AI 应用工程师方向岗位市场，产出目标公司分层清单、薪资带宽、技能差距分析，写入 targets.md。触发词：岗位扫描、市场扫描、有哪些公司在招、目标公司、agent 方向有哪些机会。
---

# Agent 方向岗位市场扫描

先读 `~/project/AI/job-hunt/PROFILE.md` 了解候选人资产，再按下面流程产出 `targets.md`。

## 公司池（分五层，逐层收录）

**T1 大厂 AI 业务线**（钱多+履历硬，风气看具体部门）：字节（豆包/Coze/TRAE）、阿里（通义/百炼/夸克）、腾讯（元宝/ima/混元）、百度（文心/Comate）、美团（LongCat）、快手（可灵）

**T2 AI 独角兽**（钱最多、技术最纯，节奏可能快）：DeepSeek、月之暗面 Kimi、智谱、MiniMax、阶跃星辰、面壁智能、百川

**T3 Agent/应用创业公司**（最对口、成长快，需查融资存活）：Manus、Dify、Monica、心流、问小白、硅基流动、无问芯穹

**T4 Coding/DevTool 方向**（前端背景天然加分）：通义灵码、CodeGeeX、Fitten Code 等 AI 编程工具团队

**T5 长沙本地兜底**（不换 base 的保底项）：华为长沙研究所、拓维信息、景嘉微、树根互联、马栏山 AI 文创

## 每家公司记录（targets.md 表格列）

公司 / 业务线 / 岗位名 / base / 薪资带宽 / 渠道（内推码·Boss·官网）/ 风气初筛 / 优先级 / 备注

薪资带宽信源：Boss 直聘岗位页 > offershow > 脉脉职言 > levels.fyi（外企）。

## 薪资参考线（社招，前端转 AI 应用/Agent）

- 北上深杭大厂：25-45K × 14-16 薪
- T2 独角兽核心团队：40K+ × 15+，可能有期权
- 长沙本地：15-25K × 13-14

**结论逻辑**：候选人接受换 base 且要求钱多 → 主攻 T1/T2/T3 一线岗位，T5 仅作过渡保底。

## JD 差距分析（每月一次）

1. 抓 20 条目标 JD（关键词：AI 应用工程师、Agent 工程师、LLM 应用、AI 全栈、AI 前端）
2. 提取技能词频，对照 PROFILE.md 技能资产
3. 输出缺口清单及补法，例如：
   - LangGraph / 多智能体编排 → 用 flue-workflow-console 经验迁移，写一个 demo
   - MCP server 开发 → 一天可上手，给 stylist-agent 写个 MCP server 当作品
   - 向量库（pgvector/Milvus）→ RAG side project
4. 差距只补「JD 高频出现且 1-2 周能拿下」的，不追新概念

## 工具（本项目即武器，命令可直接跑）

```bash
cd ~/project/AI/FindJobs-Agent
# 1. 爬目标公司（key 见 job_crawler_v2.py 的 CRAWLERS 注册表）
python3 job_crawler_v2.py -c tencent bytedance baidu -f crawled_jobs_raw.json
# 2. 爬取 + LLM 分析一体（llm_config.json 配好 key）
python3 pipeline.py -c tencent bytedance baidu
# 3. AI/Agent 岗位 → targets.md、投递看板 → applications.md（幂等）
python3 scripts/sync_to_jobhunt.py          # --deep 连岗位描述一起筛
```

- 新公司一行挂载：AI 独角兽多用飞书招聘，在 `CRAWLERS` 加 `create_feishu_crawler('<slug>', '公司名')`，slug 即 `<slug>.jobs.feishu.cn`
- sync 只重写 `<!-- FINDJOBS:* -->` 锚点内的自动区块，手写的薪资/内推码备注永不丢
- Boss/猎聘手查仅作补充源，记录在手写区

## 输出

追加/更新 `~/project/AI/job-hunt/targets.md`，新公司标记「待尽调」，提醒用户跑 `job-culture-vet`。
