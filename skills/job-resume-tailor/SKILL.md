---
name: job-resume-tailor
description: 把候选人真实项目包装成 Agent 工程师简历，按具体 JD 定制生成中英文版本，存入 resumes/ 目录。触发词：改简历、写简历、定制简历、针对这个 JD 出简历。
---

# Agent 工程师简历定制

先读 `~/project/AI/job-hunt/PROFILE.md`（技能资产+项目弹药）。

## 定位宣言（简历灵魂）

不写「前端工程师想转 Agent 方向」（自我降级），写：

> **做过 6 个已上线个人 Agent 产品的全栈工程师，前端工程能力是我的超能力，不是我的天花板。**

证据链：每条技术主张都有仓库链接，面试可现场跑。

## 简历结构（一页）

1. 基本信息 + GitHub（github.com/manyyuri）
2. 核心技能（按 JD 关键词重排，分四组）：
   - **AI 应用**：Agent Runtime（Flue）、Function Calling、zod→JSON Schema 工具强校验、SSE 流式、规则引擎+LLM 混合编排、本地模型（Ollama）、RAG、MCP
   - **前端**：React 19、antd 6、@ant-design/x 2（BubbleList/Sender）、Vite、zustand、Web Audio、MediaPipe
   - **后端**：Node/Express 5、FastAPI、Flask、SQLite、Python
   - **工程化**：pnpm monorepo、node:test、Biome、CI
3. 项目经历（3 个精讲，按下文弹药库）
4. 工作经历（数字马力，写清业务和技术栈即可，不展开）
5. 教育背景

## 项目弹药库（全部来自真实仓库，量化数据不许改）

**stylist-agent（小PD · 形象管家 Agent）** — 主打项目
- Flue Agent Runtime：持久化会话、工具调用、恢复与事件流；9 个工具
- zod 4 定义参数 → `z.toJSONSchema()` 生成 function calling schema，强校验防幻觉参数
- **防幻觉架构（面试王牌）**：结构合法性（温度桶/正式度/色彩 HSL 色距/品类覆盖）由确定性规则引擎保证，LLM 只负责挑选与叙事——LLM 永远无法编造不存在的单品
- SSE 工具结果按类型渲染结构化卡片（ChatGPT Plugins 同款交互）；antd x 对话 UI
- 降级设计：无 LLM key 时全功能可用（规则引擎+模板兜底）；26 个 node:test 用例

**your-dance-teacher（AI 舞蹈老师）**
- MediaPipe Pose 33 关键点 + librosa 节拍检测，M1 Pro CPU 每帧 <20ms
- Web Audio 前瞻调度，口令人声误差 <10ms
- 体感跟跳：浏览器端实时骨架 + 逐拍判定（Perfect/Good/Miss+连击），评分公式与离线评测同源（无 DTW）
- 教师姿态流 8.2MB→183KB 紧凑传输；一键导出零依赖离线 HTML 包

**flue-workflow-console（Skill 工作流运行时）**
- 「工作流是数据不是代码」：DSL 只声明 skill 名，Runtime 动态发现并加载 SKILL.md 执行
- REST API 注册任意 DSL，步骤依赖编排 + 证据回写

**house-keeping-assistant（三格电）**
- 本地 Ollama 视觉（qwen3-vl）+ 云端 Agent 双通道可切换，照片可不出内网
- 断舍离评分由纯规则计算，LLM 自报分数无效——provider 无关的防幻觉

备选：Headroom（确定性领域策略+LLM 只做理解表达）、Glow（Flue 陪伴式 agent、skill 按需加载）、FindJobs-Agent（注明 fork+自己贡献：增量分析、投递看板、测试覆盖）。

## JD 定制流程

1. 读 JD，提取 top 5 硬性要求
2. 重排技能组顺序 + 换主推项目（如 JD 重 RAG 就把 house-keeping 的知识库部分前置）
3. 生成 `~/project/AI/job-hunt/resumes/<公司>-<岗位>.md`（+英文版如 JD 为英文）
4. 版本留档，面这家之前回读

## 反模式

- 不写「学习能力强/吃苦耐劳」类空话
- 不写不熟的技术（写了必被问穿）
- 每个动词后面跟数字或名词证据，删掉所有不可验证的形容
