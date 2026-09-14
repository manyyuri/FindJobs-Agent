---
name: job-github-polish
description: 打磨 GitHub 主页（manyyuri）与置顶仓库的门面——profile README、置顶、双语 README、demo GIF、topics，让面试官 30 秒被打动。触发词：GitHub 主页、作品集、置顶仓库、profile README、包装 GitHub。
---

# GitHub 作品集打磨

目标仓库：github.com/manyyuri。所有改动给出可直接粘贴/执行的产物（README 全文、命令），不空谈建议。

## 现状诊断（2026-09，定期重跑）

- ❌ 无 bio、无 profile README、无置顶仓库
- ❌ repo 描述随意（Glow =「精致生活」）、0 star、无 topics
- ✅ 项目本身质量高（6 个 agent 产品，README 详尽）

→ 结论：**酒很好，瓶子没贴标签。** HR 和面试官的第一眼全靠这一轮补齐。

## 动作清单

**1. Profile bio（一行，中英）**

```
AI Agent builder · Full-stack engineer (React/Node/Python) · 6 shipped agent products · open to agent/AI app roles
```

**2. Profile README**（建 `manyyuri/manyyuri` 公开仓库，README.md 即主页）

结构：
- 一句话定位 + 「正在找 Agent/AI 应用方向机会，接受 relocation，联系方式」
- 6 个项目卡片表格：项目 / 一句话 / 技术亮点（2-3 个关键词）/ 链接
- 技能矩阵（简短）
- 每个「亮点」必须是防幻觉、流式工具卡片、实时姿态评分这类具体词，不写「使用 AI 技术」

**3. 置顶 6 仓库**：stylist-agent、your-dance-teacher、flue-workflow-console、house-keeping-assistant、Headroom、easy-to-learn（Glow 替补）

**4. 重写每个置顶 repo 的 GitHub 描述**（中英一行，说清是什么+最亮技术），示例：

- stylist-agent: `Personal stylist agent — Flue runtime, zod-validated tool calling, rule engine + LLM hybrid (LLM can't hallucinate wardrobe items) · 形象管家 Agent`
- your-dance-teacher: `AI dance coach — MediaPipe pose scoring in browser, <10ms audio scheduling, offline export · AI 舞蹈老师`

**5. 每个置顶 repo 的 README 顶部**：加 3 行英文摘要 + 1 张 GIF/截图（演示 > 一千字；用脚本录：OOTD 生成对话、体感跟跳评分、workflow 编排画面）

**6. 打 topics 标签**：`ai-agent` `llm` `function-calling` `react` `mediapipe` 等，进 GitHub 搜索池

**7. 提交卫生**：投递季保持每日绿墙；push 前把 wip 类 commit message 整理成 conventional 风格

## 验收标准（30 秒陌生人测试）

让一个不了解候选人的读者看主页 30 秒，能回答：他是谁（做 agent 的全栈）／最亮的项目是哪个（stylist-agent 或 dance-teacher）／怎么验证（点进去有 demo GIF 和详尽 README）。三个问题任何一个答不上，继续改。
