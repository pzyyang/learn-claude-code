#!/usr/bin/env python3
"""
s01_agent_loop.py - The Agent Loop

The entire secret of an AI coding agent in one pattern:

    while stop_reason == "tool_use":
        response = LLM(messages, tools)
        execute tools
        append results

    +----------+      +-------+      +---------+
    |   User   | ---> |  LLM  | ---> |  Tool   |
    |  prompt  |      |       |      | execute |
    +----------+      +---+---+      +----+----+
                          ^               |
                          |   tool_result |
                          +---------------+
                          (loop continues)

This is the core loop: feed tool results back to the model
until the model decides to stop. Production agents layer
policy, hooks, and lifecycle controls on top.

Usage:
    pip install anthropic python-dotenv
    ANTHROPIC_API_KEY=... python s01_agent_loop/code.py
"""

# ── 导入模块（import）─────────────────────────────────────────
# Python 的 import 类似 Java 的 import，但模块粒度更大（整个文件而非单个类）
import os
# subprocess 类似 Java ProcessBuilder，执行外部系统命令
import subprocess

# 条件导入：try/except 处理导入失败（Java 编译时就必须解决所有依赖）
try:
    import readline
    # macOS 的 libedit 在处理中文输入时有退格问题，这四行修复它
    readline.parse_and_bind('set bind-tty-special-chars off')
    readline.parse_and_bind('set input-meta on')
    readline.parse_and_bind('set output-meta on')
    readline.parse_and_bind('set convert-meta off')
except ImportError:
    pass  # pass 是空语句块（类似 Java 的空白代码块 { }）

# from X import Y：从模块导入特定类（类似 Java import com.xxx.SpecificClass）
from anthropic import Anthropic
from dotenv import load_dotenv

# load_dotenv() 加载 .env 文件的环境变量到 os.environ
# override=True 表示覆盖已有环境变量（类似 Java dotenv-java 库）
load_dotenv(override=True)

# os.getenv() 读取环境变量（类似 Java System.getenv()），不存在返回 None
if os.getenv("ANTHROPIC_BASE_URL"):
    # os.environ 是 dict 类型（类似 Map<String,String>），pop() 删除 key 并返回值
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

# 创建 API 客户端（类似 Java 中初始化 HTTP client / SDK 实例）
client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))
# os.environ["KEY"] 直接取值（key 不存在会抛 KeyError，类似 Map.get() 不传默认值）
MODEL = os.environ["MODEL_ID"]

# f-string 格式化：f"text {var}" 在字符串中嵌入变量（Java: "text " + var 或 String.format()）
SYSTEM = f"You are a coding agent at {os.getcwd()}. Use bash to solve tasks. Act, don't explain."

# ── 工具定义（类似定义 REST API 的 JSON Schema 接口描述）────────
# Python list 字面量用 []，dict（字典/映射）字面量用 {}
TOOLS = [{
    "name": "bash",
    "description": "Run a shell command.",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
    },
}]


# ── 工具实现 ────────────────────────────────────────────────
def run_bash(command: str) -> str:
    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    # any(生成器表达式) 类似 Java Stream.anyMatch()
    # (d in command for d in dangerous) 是生成器表达式（惰性求值，节省内存）
    # "in" 运算符用于判断子串（类似 Java String.contains()）
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        # subprocess.run() 类似 Java ProcessBuilder.start() + waitFor()
        # shell=True: 通过系统 shell 执行（Java: Runtime.exec("sh -c '...'")）
        # capture_output=True: 捕获 stdout 和 stderr
        # text=True: 输出转字符串（否则是 bytes，类似 Java 的 InputStream vs Reader）
        r = subprocess.run(command, shell=True, cwd=os.getcwd(),
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).strip()
        # 切片 [:50000] 取前 50000 字符（Python 切片越界不报错，自动截断）
        # 类似 Java: out.substring(0, Math.min(out.length(), 50000))
        # "A if condition else B" 是 Python 的三元表达式（Java: condition ? A : B）
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: Timeout (120s)"
    except (FileNotFoundError, OSError) as e:
        # 一次捕获多个异常类型（Java: catch (FileNotFoundException | IOException e)）
        return f"Error: {e}"


# ── 核心模式：Agent Loop — 循环调用 LLM + 执行工具，直到模型停止 ──
def agent_loop(messages: list):
    # messages: list 表示参数应为列表类型（类似 Java: List<?> messages）
    # 但 Python 类型注解只是提示，运行时不做检查

    while True:  # 无限循环（Java: while (true)）
        # 调用 Anthropic API，传入消息历史和工具列表
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )

        # list.append() 在末尾添加元素（Java: list.add()）
        messages.append({"role": "assistant", "content": response.content})

        # 模型决定不再调用工具 → 任务完成，退出循环
        if response.stop_reason != "tool_use":
            return

        # 遍历 LLM 响应的每个内容块（block），执行工具调用
        results = []
        for block in response.content:
            # 动态属性访问 block.type（类似 Java 反射 + getClass().getField()）
            if block.type == "tool_use":
                # ANSI 颜色码: \033[33m = 黄色, \033[0m = 重置
                print(f"\033[33m$ {block.input['command']}\033[0m")
                output = run_bash(block.input["command"])
                print(output[:200])  # 只显示前 200 字符
                results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                })

        # 关键步骤！将工具执行结果作为"user"消息追加回消息历史
        # 这样 LLM 就能看到工具的输出，决定下一步操作
        messages.append({"role": "user", "content": results})


# ── Entry point ──────────────────────────────────────────
if __name__ == "__main__":
    print("s01: Agent Loop")
    print("输入问题，回车发送。输入 q 退出。\n")

    history = []
    while True:
        try:
            query = input("\033[36ms01 >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            break
        if query.strip().lower() in ("q", "exit", ""):
            break
        history.append({"role": "user", "content": query})
        agent_loop(history)
        # Print the model's final text response
        response_content = history[-1]["content"]
        if isinstance(response_content, list):
            for block in response_content:
                if getattr(block, "type", None) == "text":
                    print(block.text)
        print()
