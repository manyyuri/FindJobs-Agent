---
name: job-interview-drill
description: Agent 方向面试特训——知识地图、项目深挖问答、全真模拟面试、HR 面防坑与反问清单。触发词：模拟面试、面我、面试准备、练面试、明天面 XX。
---

# Agent 方向面试特训

先读 `~/project/AI/job-hunt/PROFILE.md`。有目标公司/JD 时优先针对性准备；无则按知识地图查漏。

## 知识地图（按面试出现频率排序）

1. **Agent 核心**：ReAct、plan-and-execute、multi-agent 协作、memory（短期/长期/工作记忆）、context 窗口管理、工具调用循环、失败重试与降级、agent 评估（成功率/成本/延迟）
2. **Function Calling 深度**（候选人有实战，要答出深度）：schema 设计原则、参数强校验（zod→JSON Schema）、工具结果回注、并行调用、幻觉参数防御、工具太多怎么办（路由/分组/检索式工具选择）
3. **RAG**：chunking 策略、embedding 选型、混合检索（BM25+向量）、rerank、评估（召回率/忠实度）、与长上下文的取舍
4. **MCP**：协议结构（server/tools/resources）、与 function calling 的关系、给现有应用加 MCP server 的步骤
5. **LLM 基础**：token、上下文窗口、温度、结构化输出（JSON mode/constrained decoding）、streaming 原理
6. **前端 × AI**（差异化王牌）：SSE 流式渲染、token 级打字机与重排、中断/取消生成、乐观更新、工具卡片 UI（antd x BubbleList/Sender）、长对话虚拟列表、错误重连
7. **工程化**：prompt 版本管理、评测集建设、可观测（trace/成本）、降级设计、多 provider 路由
8. **前端八股保底**：JS/TS、React 原理（fiber/并发/Hooks）、事件循环、网络、浏览器——别因转方向丢了基本功

## 项目深挖题库（面试前必练，答案全部从真实代码出发）

每个主推项目准备 10 问，示例（stylist-agent）：
- 为什么用 Flue runtime 而不是裸调 SDK？（答：持久化会话/工具调用/恢复与事件流是 runtime 级需求）
- 规则引擎和 LLM 的边界怎么划的？（结构合法性归代码，挑选与叙事归 LLM）
- LLM 幻觉出衣橱里没有的单品怎么办？（结构上不可能：候选集先由规则筛出）
- SSE 断线怎么处理？工具卡片渲染时机？
- 无 LLM key 的降级路径具体长什么样？

your-dance-teacher 必备：为什么不用 DTW（音乐即时间轴）、评分公式怎么定的（8 关节角+K_POSTURE，与离线评测同源）、浏览器端实时骨架的性能账（每帧 <20ms 怎么做到的）。

**面试前动作：重读对应 repo 的 README 和关键源码，每个数字都能现场复现来路。**

## 模拟面试模式（用户说「面我」）

1. 用户指定公司/JD（或从 applications.md 取最近的）
2. 按真实节奏三段：技术八股(20min) → 项目深挖(30min) → 反问环节(5min)
3. 一次一题，等用户答完再追问；不确定答案就说不知道（考察诚实度）
4. 每段结束打分（1-5）+ 逐条反馈：答对了什么、漏了什么、更好的答法
5. 结束写 `interview-log.md`：日期/公司/题目/失分点/下次要补的

## 行为面与 HR 面

- 离职原因话术：「现岗位业务收缩，我想全职投入 agent 方向，个人项目已经证明了这个方向的能力」——**不提前雇主任何负面**（包括风气事件）
- 薪资被问：先反问带宽；被逼报数→当前总包 +30% 且取带宽上沿（详见 job-offer-negotiate）

## 反问清单（面试官问「你有什么问题」时，兼风气探针）

- 「团队现在最大的技术挑战是什么？」（听具体还是画饼）
- 「团队一般几点下班？周末需要 on-call 吗？」（双休真实性）
- 「这个岗位最近一次 code review / 团队活动是什么样的？」（风气探针，听具体例子）
- 「我入职后前三个月的 success 长什么样？」
