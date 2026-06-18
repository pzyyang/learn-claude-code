#!/usr/bin/env python3
# Harness: the loop -- the model's first connection to the real world.
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
"""

# ── 导入（import）────────────────────────────────────────────
# Python 的 import 类似 Java 的 import，但可以导入整个模块而非特定类
# import os 相当于 Java 中导入 java.lang.System 下的所有静态方法
import os
# subprocess 模块类似 Java 的 ProcessBuilder，用于执行外部命令
import subprocess

# 条件导入：Python 支持 try/except 处理导入失败（Java 编译时就必须解决依赖）
try:
    import readline
    # #143 UTF-8 backspace fix for macOS libedit
    # Python 函数调用支持关键字参数，类似 Java Builder 模式的可读性
    readline.parse_and_bind('set bind-tty-special-chars off')
    readline.parse_and_bind('set input-meta on')
    readline.parse_and_bind('set output-meta on')
    readline.parse_and_bind('set convert-meta off')
    readline.parse_and_bind('set enable-meta-keybindings on')
except ImportError:
    pass  # pass 是空语句，相当于 Java 的空分号 ; 或空代码块 {}

# 从第三方包导入特定类（类似 Java: import com.anthropic.sdk.Anthropic;）
from anthropic import Anthropic
# dotenv: 从 .env 文件加载环境变量到 os.environ（Java 中通常用 Spring 的 @Value 或 dotenv-java）
from dotenv import load_dotenv

# 加载 .env 文件，override=True 表示覆盖已有的环境变量
load_dotenv(override=True)

# os.getenv() 读取环境变量（类似 Java 的 System.getenv()）
# 如果不存在返回 None（类似 Java 返回 null）
if os.getenv("ANTHROPIC_BASE_URL"):
    # os.environ 是 dict 类型（类似 Java HashMap），pop() 删除并返回值
    os.environ.pop("ANTHROPIC_AUTH_TOKEN", None)

# 创建 API 客户端（类似 Java 中初始化 HTTP client / SDK 实例）
client = Anthropic(base_url=os.getenv("ANTHROPIC_BASE_URL"))
# os.environ["KEY"] 直接取值（key 不存在会抛出 KeyError，类似 Map.get() 失败抛异常）
MODEL = os.environ["MODEL_ID"]

# f-string 格式化字符串（类似 Java 15+ 的 "text blocks" 或 String.format()）
# f"Hello {name}" 等价于 Java 的 "Hello " + name
SYSTEM = f"You are a coding agent at {os.getcwd()}. Use bash to solve tasks. Act, don't explain."

# ── 工具定义（类似 Java 中定义一个 REST API 的 JSON schema）────────────
# Python dict 字面量，用 {} 表示（类似 Java Map.of() 但更简洁）
# dict 的 key 可以是字符串，value 可以是任意类型
TOOLS = [{
    "name": "bash",
    "description": "Run a shell command.",
    "input_schema": {
        "type": "object",
        "properties": {"command": {"type": "string"}},
        "required": ["command"],
    },
}]

# ── 工具执行 ──────────────────────────────────────────────────
def run_bash(command: str) -> str:
    # Python 函数签名：def 函数名(参数: 类型注解) -> 返回类型注解:
    # 相当于 Java: public String runBash(String command)
    # 但类型注解只是提示，运行时不做校验（Java 是强制类型检查）

    dangerous = ["rm -rf /", "sudo", "shutdown", "reboot", "> /dev/"]
    # any(生成器表达式) — 类似 Java 的 stream.anyMatch()
    # "d in command" 是 Python 的子串判断（Java: command.contains(d)）
    if any(d in command for d in dangerous):
        return "Error: Dangerous command blocked"
    try:
        # subprocess.run() 类似 Java 的 ProcessBuilder.start() + 等待
        # shell=True: 通过 shell 执行（类似 Java 的 Runtime.exec("sh -c '...'")）
        # capture_output=True: 捕获 stdout/stderr
        # text=True: 输出转为字符串而非 bytes（Python 3.7+）
        # timeout=120: 120 秒超时
        r = subprocess.run(command, shell=True, cwd=os.getcwd(),
                           capture_output=True, text=True, timeout=120)
        # r.stdout 和 r.stderr 是字符串，用 + 拼接
        # .strip() 去除首尾空白（类似 Java 的 .trim()）
        out = (r.stdout + r.stderr).strip()
        # 切片语法 [:] — Python 独有！out[:50000] 表示取前 50000 个字符
        # 类似 Java 的 out.substring(0, Math.min(out.length(), 50000))
        # "if out else" 是条件表达式（类似 Java 的三元运算符 ? :）
        return out[:50000] if out else "(no output)"
    except subprocess.TimeoutExpired:
        # except 捕获特定异常（类似 Java 的 catch(TimeoutExpired e)）
        return "Error: Timeout (120s)"
    except (FileNotFoundError, OSError) as e:
        # 一次捕获多种异常（类似 Java 的 catch (FileNotFoundException | IOException e)）
        return f"Error: {e}"


# -- The core pattern: a while loop that calls tools until the model stops --
def agent_loop(messages: list):
    # messages: list 表示参数是列表类型（类似 Java 的 List<?> messages）
    # Python 的 list 是动态数组，类似 Java 的 ArrayList，但访问用 lst[i] 而非 list.get(i)

    while True:  # 无限循环（Java: while (true) {}）
        # Anthropic API 调用 —— 将消息历史 + 工具定义发送给模型
        response = client.messages.create(
            model=MODEL, system=SYSTEM, messages=messages,
            tools=TOOLS, max_tokens=8000,
        )
        # 把 AI 的回复追加到历史消息（类似 StringBuilder.append()）
        # list.append() 在末尾添加元素（Java: list.add()）
        # dict 字面量 {"key": value} 创建新字典
        messages.append({"role": "assistant", "content": response.content})

        # 如果模型没有调用工具（stop_reason != "tool_use"），说明它完成了任务
        if response.stop_reason != "tool_use":
            return  # Python 函数返回 None（类似 Java 的 void return）

        # 遍历模型的响应内容，执行每个工具调用
        results = []
        for block in response.content:
            # .type 是动态属性访问（类似 Java 的反射 getField()，但更简洁）
            if block.type == "tool_use":
                # ANSI 颜色码：\033[33m 黄色，\033[0m 重置
                print(f"\033[33m$ {block.input['command']}\033[0m")
                output = run_bash(block.input["command"])
                # 切片 [:200] 截取前 200 个字符显示
                print(output[:200])
                results.append({"type": "tool_result", "tool_use_id": block.id,
                                "content": output})
        # 把工具执行结果反馈给模型（这是 Agent Loop 的关键步骤）
        messages.append({"role": "user", "content": results})


# ── 程序入口 ──────────────────────────────────────────────────
# Python 等价于 Java 的 public static void main(String[] args)
# 当此 .py 文件被直接运行时（而非 import），__name__ 变量的值为 "__main__"
if __name__ == "__main__":
    history = []  # 空列表（类似 Java: List<Map> history = new ArrayList<>()）
    while True:
        try:
            # input() 读取用户输入（类似 Java 的 new Scanner(System.in).nextLine()）
            # \033[36m 青色 ANSI 颜色码
            query = input("\033[36ms01 >> \033[0m")
        except (EOFError, KeyboardInterrupt):
            # Ctrl+D 或 Ctrl+C 时退出（Java 中没有直接的 EOFError 对应）
            break
        # .strip().lower() 链式调用去除空白并转小写
        if query.strip().lower() in ("q", "exit", ""):
            break  # break 跳出循环（和 Java 一样）
        history.append({"role": "user", "content": query})
        agent_loop(history)
        # 获取模型最终文本回复
        response_content = history[-1]["content"]  # [-1] 取最后一个元素
        # isinstance() 类型检查（类似 Java 的 instanceof）
        if isinstance(response_content, list):
            for block in response_content:
                # hasattr() 检查对象是否有某属性（类似 Java 反射）
                if hasattr(block, "text"):
                    print(block.text)
        print()
