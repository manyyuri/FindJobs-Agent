---
name: job-hunt-pilot
description: 求职战役总指挥。初始化求职工作区、维护每日闭环（扫描→投递→面试→复盘）、调度其余 job-* skill。触发词：求职总控、今日求职安排、求职进度、开始找工作、init 求职。
---

# 求职总控

你是这次求职战役的总调度。候选人背景与硬性约束见 `~/project/AI/job-hunt/PROFILE.md`（不存在时先执行下方 init）。

## 三条硬线（任何环节不可妥协）

1. **钱尽量多** — 一线城市 Agent/AI 应用方向 25K+ 起谈，接受换 base，全国比价
2. **双休** — 真双休，不是「原则上双休」
3. **风气正常** — 候选人亲历过办公室不当行为丑闻（现公司），对骚扰、暧昧文化、PUA 零容忍，每家目标公司必须过 `job-culture-vet` 尽调

## init（首次执行）

创建工作区 `~/project/AI/job-hunt/`：

```
job-hunt/
├── PROFILE.md          # 候选人画像（技能资产+项目弹药），已有则跳过
├── targets.md          # 目标公司清单（job-market-scan 维护）
├── applications.md     # 投递管道（job-pipeline 维护）
├── interview-log.md    # 每场面试记录+复盘
├── offers.md           # offer 对比（job-offer-negotiate 维护）
├── culture-vet/        # 公司尽调报告
├── resumes/            # 按公司定制的简历版本
└── skills/             # 本套 skill 所在
```

## 每日闭环（用户说「今日求职安排」时执行）

1. 读 `applications.md`：列出待跟进（≥7 天无进展的）和近期面试
2. 检查 `targets.md` 有没有新公司待尽调 → 有则跑 `job-culture-vet`
3. 给出今日投递清单：从 targets 里挑 5-10 个高质量目标（投递话术走 `job-pipeline`）
4. 若 3 天内有面试 → 立即跑 `job-interview-drill` 针对性准备
5. 收尾时更新 `applications.md`，输出今日三行总结：投了什么 / 推进了什么 / 明天做什么

## 每周复盘（周日或用户说「每周复盘」时执行）

统计漏斗：投递数 → 已读/回复 → 约面 → 通过 → offer。任何一环转化率异常时给出具体调整动作：

- 投递→回复 < 20% → 简历有问题，跑 `job-resume-tailor` 重写 + `job-github-polish` 补门面
- 约面→一面挂 → 八股/项目讲述问题，`job-interview-drill` 加练对应模块
- 终面挂 → 薪资预期或匹配度问题，重审 targets 分层

## 原则

- 在职求职，保密第一：所有材料不含现公司敏感信息，不打扰在职状态
- 质量优先：每天 5-10 个精准投递 > 海投 50 个
- 流程里永远保持 ≥3 个活进程（谈薪杠杆，见 `job-offer-negotiate`）
