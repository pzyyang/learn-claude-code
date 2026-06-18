# agents/ — Harness 实现（s01-s12）+ 完整参考（s_full）
# 每个文件独立可运行：python agents/s01_agent_loop.py
# 「模型即 Agent」—— 模型本身是智能体，这些文件只是外壳（Harness），负责提供工具和循环

# 关键概念（面向 Java 开发者）：
# - Agent Loop: 类似 Java 中的 while 循环 + 事件分发，不断将工具结果反馈给 LLM
# - Harness: 类比 Java 的 Spring 容器，管理 Agent 的生命周期和工具依赖
# - Tool: 类似 Java 中给 AI 提供的 service bean，通过 JSON schema 描述接口
# - Subagent: 类似 Java 中 ForkJoinPool 的子任务，拥有独立的上下文（消息历史）

# Python 包标识文件（类似 Java 的 package-info.java，但必须存在才能被 import）
# __init__.py 是 Python 包的标志，目录下有此文件才能被 from agents import xxx
