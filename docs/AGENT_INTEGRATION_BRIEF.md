# 多 Agent 知识共享设计输入 Briefing

> 本文档是给 PC 端 coding agent（antigravity / opencode / codex / kiro）做**接法设计**时的事实输入。
> 只陈述现状与约束，不预设方案——由 agent 基于这些事实给出设计。

---

## 0. 要解决的目标

一个用户，两个维度碎片化，希望所有 Agent「共享 + 共同迭代」：

- **工具碎片化**：antigravity、opencode、codex、kiro、Claude Code —— 各有一套配置格式、记忆机制、上下文文件。
- **环境碎片化**：PC（多个 Agent）、Telegram（手机端 Hermes）、VPS（Hermes 常驻服务端）。

目标：这些工具产生的**知识**能被抽离成工具无关、可共享、随时间增长的单一事实源，每个 Agent 只是该知识库的「客户端」。

---

## 1. 一个绕不开的前提事实

用户的「单一事实源候选」`context-infrastructure` 仓库**不是用户原创系统**，而是开源模板：

- 上游模板：`grapeot/context-infrastructure`（MIT，README 见仓库内）
- 用户 fork 后的私有仓库：`git@github.com:Jayden-Zhang65/context-infrastructure.git`（VPS 为 origin，仅此一个 remote，无 upstream）
- 模板定位原文：「这不是开箱即用的工具，而是 reference implementation（蓝图）。Clone 后能体验有/无 context 的差异，但要让 AI 真正变成自己的，需从头采集行为数据，没有捷径。」

含义：仓库的结构（rules/contexts/axioms/skills 层级）源自模板惯例，**其中打上用户烙印的部分**只有：`rules/USER.md`、`rules/SOUL.md`（改写过）、`contexts/daily_records/`（4 条真实日报）、`contexts/memory/OBSERVATIONS.md`、`git log` 里那条「merge AGENTS.md into CLAUDE.md for multi-tool support」的自定义提交。设计接法时**不要**把模板的「展示层」（43 条 axioms、25+ 个 skill 样本）当成用户真实积累——那是原作者视角，用户尚未用自己的数据填满。

## 2. context-infrastructure 仓库真实结构

```
context-infrastructure/   (VPS 上 /home/hermes/.hermes/context-infrastructure，git clean)
├── CLAUDE.md             # 统一入口上下文。已声明服务 Hermes + Claude Code/Kiro 两端，
│                         #   含 Every Session 初始化、技能表、知识捕获约定
├── README.md             # 模板原文，含目录结构、三层结构说明
├── setup_guide.md        # 模板配置指引
├── .env / .env.example / pyrightconfig.json
├── adhoc_jobs/           # 按需任务（空）
├── contexts/
│   ├── memory/OBSERVATIONS.md        # 长期观察（L1/L2 记忆层）
│   ├── daily_records/                # 日报：4 条真实记录（Agilent培训、智能制造AI、数字化会议）
│   ├── survey_sessions/  thought_review/    # 空（.gitkeep）
├── docs/
│   ├── CRONTAB.md        # 定时任务配置指南（模板）
│   ├── SKILL_ECOSYSTEM.md# 可单独安装的 public skill repo 目录（模板）
│   └── working.md        # 工作日志（模板）
├── periodic_jobs/ai_heartbeat/       # 模板的记忆系统代码
│   ├── docs/{PRD,KNOWLEDGE_BASE}.md
│   └── src/v0/{observer,reflector}.py   # 观察/反思脚本（需 cron，未实际启用）
├── rules/
│   ├── SOUL.md                      # 改写过（用户身份基调）
│   ├── USER.md                      # 改写过（用户真实背景/偏好）★最重要
│   ├── COMMUNICATION.md             # 沟通风格（可直接用）
│   ├── WORKSPACE.md                 # 目录路由索引（模板小改）
│   ├── axioms/                      # 43 条公理（模板展示层，非用户积累）
│   └── skills/                      # 25+ 个 skill（模板+部分用户）
│       ├── INDEX.md                 # 技能分类索引
│       ├── workflow_knowledge_flywheel.md   # 知识飞轮设计模式
│       ├── workflow_parallel_subagents.md   # 并行 subagent 工作流
│       ├── workflow_deep_research_survey.md # 深度调研工作流
│       └── ...（见 INDEX.md）
├── tools/
│   ├── semantic_search/             # 本地 embedding+cosine 语义检索（search/cli.py 等）
│   ├── opencode_job.py  ga4_metrics.py ...   # 各类脚本
└── （无独立 AGENTS.md —— 已被合并进 CLAUDE.md，见 git log 47bb504）
```

## 3. Hermes 侧真实架构（VPS，版本 0.20.6）

Hermes 是 **Nous Research 的开源项目**（非用户自写），本身记忆机制与仓库完全解耦、自洽：

- **原生记忆（自动注入，无需外部同步）**
  - 用户画像/偏好：`~/.hermes/memories/USER.md`（自动注入每轮）
  - 个人笔记/环境事实：`~/.hermes/memories/MEMORY.md`（自动注入）
  - 人格基调：`~/.hermes/SOUL.md`
  - 它们与 `context-infrastructure/rules/` 是**两套平行**的东西
- **Skills**：`~/.hermes/skills/<分类>/<skill>/SKILL.md`（markdown+frontmatter），Hermes 自动按目录递归发现。已有用户自建 skill：`agy-bridge-hermes`、`hermes-provider-setup`、`hermes-version-upgrade`、networking 系列等
- **会话历史**：`~/.hermes/sessions/` + state.db（SQLite, FTS5 全文索引），`session_search` 原生检索
- **知识复利链路（Hermes 原生闭环，当前不写仓库文件）** 已跑 2 个 cron：
  - `daily-summary`（每天 18:00，Telegram）：`session_search` 搜当天会话 → 提炼「讨论了什么/技能工具/值得记住」，**不写文件**，直接推 Telegram
  - `weekly-reflector`（每周一 00:00，Telegram）：`session_search` 搜过去一周 → 识别可固化为 skill 的模式 → 给晋升建议，**不自动创建文件**，等用户回「执行」
  - 这两个 job 的 `workdir` 都指向 context-infrastructure，但 **prompt 硬约束「不写仓库文件」**
- **备份 cron**：`Hermes Weekly Backup`（周日 03:00，no_agent 纯 shell）→ 推 `hermes-config-backup` + `context-infrastructure` 两个 GitHub 仓库

## 4. 用户已走过的决策与教训（避免重复踩坑）

1. **hub 仓库方案被否**：曾设计过独立 `agents-knowledge` hub + 软链接挂载到各 agent。结论是会造成**双数据源、漂移冲突**。Hermes 自己走原生闭环（memories/skills/session_search），**不再反向读写共享仓库**。
2. **共享仓库的角色定位**（当前共识）：context-infrastructure 是为「**PC 端多个 agent**」服务的共享知识层；Hermes 是它的**上游生产者/桥接者**（backup.sh 把 Hermes 沉淀单向推入仓库），不是它的消费者。
3. **provider drift 教训**：cron job pin 的 provider/model 漂移后会被 Hermes 防意外花费保护自动跳过 → backup job 已改 no_agent 兜底；但 daily-summary / weekly-reflector 当前因 `opencode/deepseek-v4-flash-free`「Model is unavailable」报 error（HTTP 400），未兜底。做知识链路设计时需注意：**依赖模型推理的自动任务有漂移风险**。
4. **格式兼容**：Hermes 与各 CLI agent 都认「markdown + YAML frontmatter」的 skill 格式，这是跨工具知识协议的基础。

## 5. 待设计的问题域（给 agent 的开放任务）

基于以上事实，请给出「PC 端多 agent 共享 + 与 Hermes 共存」的接法设计，边界与约束：

1. **中心层选型**：复用现有 `context-infrastructure` 仓库（推荐）还是新建？若复用，如何把 `rules/skills/`、`rules/axioms/` 从「模板展示层」过渡为「用户真实积累层」？
2. **各 Agent 适配方式**：antigravity（GEMINI.md/AGENTS.md + ~/.gemini/skills）、opencode（AGENTS.md + skills）、codex（AGENTS.md）、kiro（project rules）——各自如何安全引用中心仓库、如何回写，而不产生双数据源？
3. **Hermes 的桥接角色**：Hermes 不反向读仓库（决策 1）；如何让 Hermes 沉淀的 skill/观察单向进入仓库，并让 PC agent 消费？是否用 backup.sh 已是够，还是需要新的同步约定？
4. **git 同步机制**：VPS origin + PC clone 的双向同步约束；冲突处理、单一事实源保证。
5. **是否引入 MCP server**（方案 B）或向量库（方案 C）作为更进阶统一接口——给出**分阶段**判断标准，不默认上重方案。
6. **生产级注意**：cron 依赖模型的漂移风险；模板展示层与用户真实层的区分；GitHub 私有仓安全（密钥不进仓库）。

请给出：目录/文件组织约定、各 agent 客户端适配的最小可行方案、Hermes 桥接实现、分阶段演进路线（A→B→C 的触发条件），以及一份可执行的落地清单。