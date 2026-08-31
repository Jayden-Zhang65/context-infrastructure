# Memory Observations

这是三层记忆系统的 L1/L2 层。每日观察由 `periodic_jobs/ai_heartbeat/src/v0/observer.py` 自动写入，每周由 `reflector.py` 整理和蒸馏。

## 格式说明

每个日期条目格式如下：

```
Date: YYYY-MM-DD

🔴 High: [方法论/约束] 描述
🟡 Medium: [项目状态/决策] 描述
🟢 Low: [任务流水] 描述
```

### 优先级定义

- **🔴 High**：跨项目通用的经验教训、硬性约束、影响系统架构的重大决策。永久保留，候选晋升为 axiom 或 skill。
- **🟡 Medium**：活跃项目的关键进展、技术决策背景、未来几周仍需参考的信息。
- **🟢 Low**：日常任务流水、瞬时 debug 记录、临时上下文。定期垃圾回收。

## 如何加载记忆

不要全文加载这个文件（可能很大）。按需检索：

```bash
# 搜索特定主题
grep -n "关键词" contexts/memory/OBSERVATIONS.md

# 搜索最近 N 天
grep -A 20 "Date: $(date -v-7d +%Y-%m-%d)" contexts/memory/OBSERVATIONS.md
```

或使用语义搜索做跨日期语义检索（安装 [semantic-search-skill](https://github.com/grapeot/semantic-search-skill)）。

---

<!-- 以下是记录区域，由 observer.py 自动追加 -->

Date: 2026-07-24

🔴 High: [方法论] OpenCode 的 session 数据库（~/.local/share/opencode/opencode.db）是 SQLite 格式，可通过 Python 直接查询跨项目的所有会话（session 表含 title/directory/time_updated，message 表含 data JSON）。这意味着每日复盘不需要依赖 agent 记忆——写个脚本查当日所有 session 的 title + user message，就能覆盖全部工作。应纳入 workflow_daily_review.md 的 Phase 1 作为自动化数据采集步骤。
🟡 Medium: [架构] OpenCode 的 SKILL.md 包装器模式：每个 skill 只需 ~6 行（frontmatter + Read 指令指向原文件），即可将外部 skill 库接入 OpenCode 的发现机制。原文件仍集中维护在 context-infrastructure/rules/skills/，避免内容重复。这模式适用于接入任何已有的 markdown skill 库。
🟡 Medium: [架构] Knowledge Capture 段落是 agent 写 daily_records 的前提——CLAUDE.md 和 AGENTS.md 中必须有显式的「会话结束前主动问 + 写入」指令，agent 才会执行。光有 workflow 文件不够，指令必须在 system prompt 层级。这个结构性约束适用于所有 agent 编程框架：agent 只执行 system-level 明确要求的行为，不会主动做"对用户好"的事。
🟡 Medium: [项目] context-infrastructure 已接入 OpenCode 全局配置作为个人知识库。核心 rules（SOUL/USER/COMMUNICATION/WORKSPACE）通过 instructions 全量注入，skills 通过 SKILL.md 包装器懒加载，contexts 通过 references 按需引用。知识分层的 PC 端桥齐（daily_review + Knowledge Capture 指令）已完成。
🟢 Low: [工具] opencode_job.py 默认模型改为 deepseek-v4-flash，choices 保留 deepseek-v4-pro 作为备选。
