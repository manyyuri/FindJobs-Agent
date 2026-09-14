---
name: job-pipeline
description: 管理投递管道——状态机跟踪、渠道策略（内推优先）、Boss 打招呼话术、跟进提醒与转化率复盘，维护 applications.md。触发词：投递记录、求职进度、今天投什么、跟进、记录投递。
---

# 投递管道管理

维护 `~/project/AI/job-hunt/applications.md`，一张表管全部流程。

## 表结构（Markdown 表格）

| 公司 | 岗位 | base | 薪资range | 渠道 | 投递日 | 状态 | 下一步 | 链接/备注 |

## 状态机

🎯target → 📨applied → 📞screening → 💻interview-1/2/3 → 🏆offer → ✅accepted / ❌rejected

- **💤stalled**：任何状态 7 天无进展自动标记，生成跟进任务
- 每次状态变更必须写日期；面试场次同步记 `interview-log.md`

## 渠道优先级（转化率从高到低）

1. **内推**：脉脉找目标公司员工 / 前同事 / 校友群；话术 = 定位一句话 + 最亮项目链接 + 「看到贵司在招 XX，方便内推吗」
2. **猎头**：薪资范围 upfront，让猎头去谈 base（详见 job-offer-negotiate）
3. **Boss 直聘**：打招呼必须定制（见话术模板）
4. **官网/邮箱**：大厂官网投递作为内推的补充（同一公司内推优先，勿双投同岗位）

## Boss 打招呼话术模板（3 句，禁止海投模板腔）

```
您好，我做 Agent 方向的全栈（React/Node/Python），个人作品有 [stylist-agent：Flue runtime + 规则引擎防幻觉的穿搭 Agent] 等 6 个已上线项目（github.com/manyyuri）。
贵司这个岗位的 [JD 里某条具体要求] 我在 [某项目] 里完整做过。
期待聊聊，可以发一份针对这个岗位的简历给您吗？
```

变量：第二句必须引用该 JD 的具体条目——这一句就是「不是海投」的证明。

## 节奏

- 每天 5-10 个高质量投递（有尽调、有定制话术），**禁止无差别海投**
- 每投一个立即记录 applications.md
- 原则：管道里永远 ≥3 个活进程（interview 及以后），这是谈薪的命根子

## 跟进脚本

一面后 3 天无消息：

> 您好，我是 X 日面试 XX 岗位的 XXX，非常感谢那天的交流。想问一下流程目前进展如何？如果需要补充材料（项目 demo/代码 walkthrough）我随时可以提供。

## 工具（看板即数据源）

```bash
cd ~/project/AI/FindJobs-Agent
python3 api_server.py                          # Web 看板（React 前端 + REST）
python3 scripts/sync_to_jobhunt.py            # 看板 → applications.md 自动区块（幂等）
```

- 状态也可直接 API 维护：`PUT /api/applications/<job_id>`，body `{"status": "applied", "note": "内推已投"}`
- 状态机：bookmarked → applied → replied → interview → offer / rejected
- 同步只改 `<!-- FINDJOBS:APPLICATIONS -->` 锚点内的表格，手写跟进记录写在锚点外永不丢

## 周度复盘（配合 job-hunt-pilot）

- 投递→已读/回复率 <20% → 简历或打招呼话术问题
- 回复→约面率低 → 定位与 JD 匹配度问题，重跑 job-market-scan 的差距分析
- 输出：本周数字 + 下周策略调整，写进 applications.md 顶部
