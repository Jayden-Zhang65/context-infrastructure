# CLAUDE.md - 统一工作区上下文
#
# 本文件同时服务于：
#   - Hermes Agent（手机/服务器端 Telegram 对话）
#   - Claude Code / Kiro（PC 端代码开发）
#
# Hermes 通过 SOUL.md 和原生 Memory 获取身份信息，无需 Every Session 指令。
# Claude Code / Kiro 没有原生持久 Memory，每次会话通过以下步骤初始化。

---

## Every Session（Claude Code / Kiro 使用）

> Hermes 用户：身份信息已由 SOUL.md 和 Memory 自动注入，跳过此节。

读取以下文件完成初始化：
1. `rules/USER.md` — 用户背景和偏好
2. `rules/WORKSPACE.md` — 目录路由索引
3. `rules/skills/INDEX.md` — 可用 Skill 列表

写作任务前额外读取：`rules/COMMUNICATION.md`

---

## Communication Style

所有输出遵循 `rules/COMMUNICATION.md` 的写作规范：
- 务实、克制，不堆砌宏大词藻
- 结论前置，优化可扫读性和可验证性
- 避免 AI 写作特征：元评论铺垫、「值得 X」句式、译文体

完整规范见 `rules/COMMUNICATION.md`，写正式内容前检索一遍。

---

## File Routing

**找文件前，先查 `rules/WORKSPACE.md`。** 绝大多数情况查一下就能定位，不需要全盘搜索。发现新目录时顺手更新 WORKSPACE.md。

---

## Skills

遇到"怎么做 X"先查 Skill，再用系统工具。

搜索顺序：下方速查 → `rules/skills/INDEX.md` → 系统工具

| 任务类型 | Skill 文件 |
|----------|-----------|
| 深度调研 | `rules/skills/workflow_deep_research_survey.md` |
| 外部写作（公开文章） | `rules/skills/workflow_external_writing.md` |
| 内部写作（文档/笔记） | `rules/skills/workflow_internal_writing.md` |
| 知识飞轮 / Skill 沉淀 | `rules/skills/workflow_knowledge_flywheel.md` |
| 写/改 Skill 本身 | `rules/skills/bestpractice_skill_writing.md` |
| AI 编程方法论 | `rules/skills/bestpractice_ai_programming_mindset.md` |
| 分阶段工作法 | `rules/skills/bestpractice_staged_approach.md` |

**想添加新 Skill** → 参考 `bestpractice_skill_writing.md`，写完后更新 `rules/skills/INDEX.md`。

---

## Knowledge Capture（知识复利关键）

对话中产生的有价值内容，主动写入以下位置（Hermes 和 Claude Code 两端均适用）：

- 当日碎片记录 → `contexts/daily_records/YYYY-MM-DD.md`
- 长期观察和洞察 → `contexts/memory/OBSERVATIONS.md`
- 可复用工作流 → `rules/skills/<name>.md` + 更新 `INDEX.md`

这些文件通过 Git 同步：
- **Hermes 端**产生的内容 → git push → PC 端 git pull → Claude Code 下次会话读到
- **Claude Code 端**产生的内容 → git push → 服务器 git pull → Hermes 下次会话读到

---

## Parallel Sub-agents

Hermes 用 `/background` 派发后台任务。Claude Code / Kiro 用原生 Task 和子进程。

并行调研任务前，先读 `rules/skills/workflow_parallel_subagents.md`。

---

## Axioms（决策公理）

遇到复杂判断时检索 `rules/axioms/INDEX.md`。

---

## Memory（记忆机制）

| 层级 | Hermes | Claude Code / Kiro |
|------|--------|--------------------|
| 身份人格 | `~/.hermes/SOUL.md`（自动） | `rules/USER.md`（每次读） |
| 用户偏好 | `~/.hermes/memories/USER.md`（自动） | `rules/USER.md`（每次读） |
| 工作记忆 | `~/.hermes/memories/MEMORY.md`（自动） | `contexts/memory/OBSERVATIONS.md`（按需） |
| 知识积累 | `contexts/daily_records/` + Cron 蒸馏 | `contexts/daily_records/` + 手动提炼 |

---

## Safety

- 不外泄私有数据。
- 破坏性命令执行前先确认。
- 不确定时，问。
