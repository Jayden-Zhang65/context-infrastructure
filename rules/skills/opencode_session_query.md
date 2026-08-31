# OpenCode 多项目会话查询

## 元数据

- **类型**: API Guide
- **适用场景**: 每日复盘、跨项目回顾、查找历史对话
- **脚本位置**: `tools/query_opencode_sessions.py`
- **创建日期**: 2026-07-24

---

## 功能

从 `~/.local/share/opencode/opencode.db` 查询跨项目会话记录。OpenCode 用 SQLite 存储所有 session 数据（title、directory、message、user prompt），通过这个脚本可以一次性看到所有工作目录的今日活动。

## 使用方式

```bash
# 今天的所有会话
python tools/query_opencode_sessions.py

# 最近 N 天
python tools/query_opencode_sessions.py --days 3

# 指定日期
python tools/query_opencode_sessions.py --date 2026-07-24

# 按项目过滤
python tools/query_opencode_sessions.py --project LIMS

# 包含消息内容（用于深入复盘）
python tools/query_opencode_sessions.py --full
```

## 前置条件

Python 3 + sqlite3（标准库自带），无需额外安装。

## 数据库位置

- Linux/macOS: `~/.local/share/opencode/opencode.db`
- Windows: `%USERPROFILE%\.local\share\opencode\opencode.db`
